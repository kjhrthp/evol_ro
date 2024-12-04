from sensor import SENSOR
from motor import MOTOR
import pyrosim.pyrosim as pyrosim
import pybullet as p
import numpy as np
class ROBOT:
    def __init__(self):
        self.robotId = p.loadURDF("body.urdf")  # 로봇 로드
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.sensors = {}
        self.motors = {}
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
        for motor in self.motors.values():
            motor.set_value(t, self.robotId)
