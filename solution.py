import numpy as np
import os
import random
import pyrosim.pyrosim as pyrosim
import subprocess
import time
class SOLUTION:
    def __init__(self, myID):
        self.myID = myID  # 고유 ID 저장
        self.weights = np.random.rand(3, 2) * 2 - 1  # [-1, 1] 범위의 랜덤 가중치 생성

    def create_world(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(pos=[0, 0, 0], size=[1, 1, 1])
        pyrosim.End()

    def Generate_Body(self):
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_RLeg", parent="Torso", child="RLeg",
                           type="revolute", position=[0.5, 0, 1.0])
        pyrosim.Send_Cube(name="RLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.Send_Cube(name="LLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])
        pyrosim.Send_Joint(name="Torso_LLeg", parent="Torso", child="LLeg",
                           type="revolute", position=[-0.5, 0, 1.0])
        pyrosim.End()

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork(f"brain{self.myID}.nndf")
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="RLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LLeg")
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_RLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_LLeg")

        for sensor in range(3):  # 센서 뉴런
            for motor in range(2):  # 모터 뉴런
                weight = self.weights[sensor, motor]
                pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor + 3, weight=weight)
        pyrosim.End()

    def Evaluate(self, mode):
        self.create_world()
        self.Generate_Body()
        self.Generate_Brain()

        # subprocess로 동기화
        command = f"python simulate.py {mode} {self.myID}"
        process = subprocess.Popen(command, shell=True)
        process.wait()  # 시뮬레이션 완료 대기

        # fitness 파일 확인 및 대기
        fitnessFileName = os.path.join(os.getcwd(), f"fitness{self.myID}.txt")
        for _ in range(10):  # 최대 10초 대기
            if os.path.exists(fitnessFileName):
                break
            time.sleep(1)
        else:
            raise FileNotFoundError(f"{fitnessFileName} not found after simulation!")

        # fitness 파일 읽기
        with open(fitnessFileName, "r") as f:
            self.fitness = float(f.read())
        print(f"[DEBUG] Fitness for ID {self.myID}: {self.fitness}")

    def Mutate(self):
        randomRow = random.randint(0, 2)  # 0~2 중 랜덤 선택
        randomColumn = random.randint(0, 1)  # 0~1 중 랜덤 선택
        self.weights[randomRow, randomColumn] = random.uniform(-1, 1)  # [-1, 1] 범위의 새로운 값

    def Set_ID(self, newID):
        self.myID = newID
