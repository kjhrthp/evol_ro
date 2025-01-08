import numpy as np
import os, random
import pyrosim.pyrosim as pyrosim
class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3,2) *2 - 1

    def create_world(self):
        pyrosim.Start_SDF("world.sdf")  # SDF 파일 생성 시작
        pyrosim.Send_Cube(pos=[0, 0, 0], size=[1, 1, 1])  # 단일 블록 추가
        pyrosim.End()  # SDF 파일 저장

    def Generate_Body(self):
        # URDF 파일 생성 시작
        pyrosim.Start_URDF("body.urdf")

        # Torso (루트 링크) 추가 - 절대 좌표
        pyrosim.Send_Cube(name="Torso",
                        pos=[0, 0, 1.5],
                        size=[1, 1, 1])

        # Torso와 Leg을 연결하는 Joint 추가 - 절대 좌표
        pyrosim.Send_Joint(name="Torso_RLeg",
                        parent="Torso", child="RLeg",
                        type="revolute",
                        position=[0.5, 0, 1.0]
                        )

        # Leg 추가 - Joint 기준 상대 좌표
        pyrosim.Send_Cube(name="RLeg",
                        pos=[0.5, 0, -0.5],
                        size=[1, 1, 1])
        # Leg 추가 - Joint 기준 상대 좌표
        pyrosim.Send_Cube(name="LLeg",
                        pos=[-0.5, 0, -0.5],
                        size=[1, 1, 1])
        # Torso와 Leg을 연결하는 Joint 추가 - 절대 좌표
        pyrosim.Send_Joint(name="Torso_LLeg",
                        parent="Torso",
                        child="LLeg",
                        type="revolute",
                        position=[-0.5, 0, 1.0])



        # URDF 파일 저장 종료
        pyrosim.End()
    # 랜덤 값을 생성하기 위해 추가

    def Generate_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")

        # 센서 뉴런 추가
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="RLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="LLeg")

        # 모터 뉴런 추가
        pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_RLeg")
        pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_LLeg")

        # Fully Connected Neural Network 생성
        sensorNeuronNames = [0, 1, 2]  # 센서 뉴런 이름
        motorNeuronNames = [3, 4]      # 모터 뉴런 이름

        for sensor in sensorNeuronNames:
            for motor in motorNeuronNames:
                # 가중치를 [0, 1] 범위로 설정
                weight = random.uniform(-1, 1)
                pyrosim.Send_Synapse(sourceNeuronName=sensor, targetNeuronName=motor, weight=weight)
                                    #<synapse sourceNeuronName = "' + str(sourceNeuronName) + '" targetNeuronName = 
                                    # "' + str(targetNeuronName) + '" weight = "' + str(weight) + '" />\n')

        pyrosim.End()
    
    def Evaluate(self, mode):
        self.create_world()
        self.Generate_Body()
        self.Generate_Brain()
        os.system(f"python3 simulate.py {mode}")  # mode 전달

        # 피트니스 값 읽기
        with open("fitness.txt", "r") as fitnessFile:
            self.fitness = float(fitnessFile.read())
        print("Fitness Value:", self.fitness)

    def Calculate_Fitness(self):
        # Fitness 계산 로직 구현 (예: 파일 읽기 등)
        pass

    def Mutate(self):
        import random
        # 3x2 가중치 행렬에서 랜덤한 행과 열 선택
        randomRow = random.randint(0, 2)  # 0, 1, 2 중 하나 선택
        randomColumn = random.randint(0, 1)  # 0, 1 중 하나 선택

        # 가중치 값을 [-1, 1] 범위의 새로운 랜덤 값으로 설정
        self.weights[randomRow, randomColumn] = random.uniform(-5, 5)
