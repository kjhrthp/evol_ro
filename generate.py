import pyrosim.pyrosim as pyrosim

def create_world():
    pyrosim.Start_SDF("world.sdf")  # SDF 파일 생성 시작
    pyrosim.Send_Cube(pos=[0, 0, 0], size=[1, 1, 1])  # 단일 블록 추가
    pyrosim.End()  # SDF 파일 저장



def Generate_Body():
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

import random  # 랜덤 값을 생성하기 위해 추가

def Generate_Brain():
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
create_world()
Generate_Body()
Generate_Brain()