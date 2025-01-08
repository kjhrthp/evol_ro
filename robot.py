from sensor import SENSOR
from motor import MOTOR
import pyrosim.pyrosim as pyrosim
import pybullet as p  # pybullet 모듈 임포트
import numpy as np
from pyrosim.neuralNetwork import NEURAL_NETWORK
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
            linkName_str = linkName.decode('utf-8') if isinstance(linkName, bytes) else linkName
            self.sensors[linkName_str] = SENSOR(linkName_str)

    def prepare_to_act(self):
        for jointName in pyrosim.jointNamesToIndices:
            jointName_str = jointName.decode('utf-8') if isinstance(jointName, bytes) else jointName
            if "RLeg" in jointName_str:
                self.motors[jointName_str] = MOTOR(jointName_str, phaseOffset=0)  # 위상 0
            elif "LLeg" in jointName_str:
                self.motors[jointName_str] = MOTOR(jointName_str, phaseOffset=np.pi/2)  # 위상 π/2

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
                #print(f"Neuron: {neuronName}, Joint: {jointName}, Desired Angle: {desiredAngle}")

    def Think(self):
        #self.nn.Print() # 이걸 주석처리 해제해야만 값이 프린트됨
        self.nn.Update()
 # Print neural network details for now

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotId, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]

        # fitness.txt에 저장
        with open("fitness.txt", "w") as f:
            f.write(str(xCoordinateOfLinkZero))
