from sensor import SENSOR
from motor import MOTOR
import pyrosim.pyrosim as pyrosim
import pybullet as p
import numpy as np
from pyrosim.neuralNetwork import  NEURAL_NETWORK
import constants as c

class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")  # 로봇 로드
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.sensors = {}
        self.motors = {}
        self.nn = NEURAL_NETWORK("brain.nndf")  # Initialize the neural network
        self.prepare_to_sense()
        self.prepare_to_act()

    def prepare_to_sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def prepare_to_act(self):
        for jointName in pyrosim.jointNamesToIndices:
            # 각 모터에 서로 다른 위상 설정
            if "RLeg" in jointName:
                self.motors[jointName] = MOTOR(jointName, phaseOffset=0)  # 위상 0
            elif "LLeg" in jointName:
                self.motors[jointName] = MOTOR(jointName, phaseOffset=3/2*np.pi)  # 위상 π/2


    def sense(self, t):
        for sensor in self.sensors.values():
            sensor.get_value(t)

    def act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName)
                pyrosim.Set_Motor_For_Joint(
                    bodyIndex=self.robotId,
                    jointName=jointName,
                    controlMode=pyrosim.p.POSITION_CONTROL,
                    targetPosition=desiredAngle,
                    maxForce=c.max_F
                )
                print(f"Neuron: {neuronName}, Joint: {jointName}, Desired Angle: {desiredAngle}")
    def Think(self):
        self.nn.Update()
        self.nn.Print()  # Print neural network details for now
