import random

import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c
# PyBullet 물리 엔진 GUI 모드로 연결
physicsClient = p.connect(p.GUI)

# URDF 파일 검색 경로 추가
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 중력 설정
p.setGravity(0, 0, -9.81)

# URDF 모델 불러오기
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
# 필요한 링크 인덱스
num_joints = p.getNumJoints(robotId)
# 링크 이름과 인덱스 매핑을 위한 딕셔너리 생성
link_name_to_index = {}
link_name_to_index["Torso"] = -1
for joint_index in range(num_joints):
    info = p.getJointInfo(robotId, joint_index)
    # jointInfo[12]는 자식 링크의 이름을 포함합니다.
    child_link_name = info[12].decode('utf-8')
    link_name_to_index[child_link_name] = joint_index

colors = {
    "Torso": [1, 0, 0, 1],   # 빨강색
    "FLeg":  [0, 1, 0, 1],   # 초록색
    "BLeg":  [0.25, 0.8, 0.25, 1]    # 진한 초록
    # 추가 링크가 있다면 여기에 색상 지정
}
for link_name, color in colors.items():
    if link_name in link_name_to_index:
        index = link_name_to_index[link_name]
        p.changeVisualShape(robotId, linkIndex=index, rgbaColor=color)
    else:
        print(f"Link {link_name} not found!")


# 실시간 시뮬레이션 켜기
p.setRealTimeSimulation(1)
pyrosim.Prepare_To_Simulate(robotId)


backLegSensorValues = np.zeros(c.num_steps)
frontLegSensorValues = np.zeros(c.num_steps)
while p.isConnected() and c.step_index < c.num_steps:
    # 실시간 시뮬레이션을 사용하므로 별도의 p.stepSimulation() 호출 불필요
    # 센서 값을 읽어서 배열에 저장
    backLegSensorValues[c.step_index] = pyrosim.Get_Touch_Sensor_Value_For_Link("BLeg")
    frontLegSensorValues[c.step_index] = pyrosim.Get_Touch_Sensor_Value_For_Link("FLeg")
    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName=b"Torso_BLeg",

        controlMode=p.POSITION_CONTROL,

        targetPosition=c.targetAngles[c.step_index]+np.pi/10,

        maxForce=c.maxforce)
    pyrosim.Set_Motor_For_Joint(

        bodyIndex=robotId,

        jointName=b"Torso_FLeg",

        controlMode=p.POSITION_CONTROL,

        targetPosition=c.targetAngles[c.step_index],

        maxForce=c.maxforce)
    print(backLegSensorValues[c.step_index])
    c.step_index += 1
    time.sleep(1/240)  # CPU 점유율을 낮추기 위해 잠시 대기

# 시뮬레이션 종료
p.disconnect()
