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
    pyrosim.Send_Joint(name="Torso_R_Leg",
                       parent="Torso", child="R_Leg",
                       type="fixed",
                       position=[0.5, 0, 1.5]
                       )

    # Leg 추가 - Joint 기준 상대 좌표
    pyrosim.Send_Cube(name="R_Leg",
                      pos=[0.5, 0, 0],
                      size=[1, 1, 1])

    # Torso와 Leg을 연결하는 Joint 추가 - 절대 좌표
    pyrosim.Send_Joint(name="Torso_L_Leg",
                       parent="Torso",
                       child="L_Leg",
                       type="fixed",
                       position=[-0.5, 0, 1.5])

    # Leg 추가 - Joint 기준 상대 좌표
    pyrosim.Send_Cube(name="L_Leg",
                      pos=[-0.5, 0, 0],
                      size=[1, 1, 1])

    # URDF 파일 저장 종료
    pyrosim.End()



create_world()
create_robot()