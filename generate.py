import pyrosim.pyrosim as pyrosim

def create_world():
    pyrosim.Start_SDF("world.sdf")  # SDF 파일 생성 시작
    pyrosim.Send_Cube(pos=[0, 0, 0], size=[1, 1, 1])  # 단일 블록 추가
    pyrosim.End()  # SDF 파일 저장



def create_robot():
    # URDF 파일 생성 시작
    pyrosim.Start_URDF("body.urdf")

    # Torso (루트 링크) 추가 - 절대 좌표
    pyrosim.Send_Cube(name="Torso",
                      pos=[0, 0, 0.5],
                      size=[1, 1, 1])

    # Torso와 Leg을 연결하는 Joint 추가 - 절대 좌표
    pyrosim.Send_Joint(name="Torso_RLeg",
                       parent="Torso", child="RLeg",
                       type="fixed",
                       position=[0.5, 0, 1.0]
                       )

    # Leg 추가 - Joint 기준 상대 좌표
    pyrosim.Send_Cube(name="RLeg",
                      pos=[0.5, 0, 0],
                      size=[1, 1, 1])

    # Torso와 Leg을 연결하는 Joint 추가 - 절대 좌표
    pyrosim.Send_Joint(name="Torso_LLeg",
                       parent="Torso",
                       child="LLeg",
                       type="fixed",
                       position=[-0.5, 0, 1.0])

    # Leg 추가 - Joint 기준 상대 좌표
    pyrosim.Send_Cube(name="LLeg",
                      pos=[-0.5, 0, 0],
                      size=[1, 1, 1])

    # URDF 파일 저장 종료
    pyrosim.End()



create_world()
create_robot()