import pyrosim.pyrosim as pyrosim
# sdf 파일에는 조인트가 없고 링크만 있다.
def create_robot():
    # make the robot
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 2], size=[1, 1, 1])
    # should be named "Parent_Child"
    pyrosim.Send_Joint(name = "Torso_FLeg", parent="Torso",
                       child="FLeg", type="revolute", position=[0.5,0,1.5])
    # child로 지정된 Leg는 joint의 상대위치이다.
    pyrosim.Send_Cube(name="FLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])
    pyrosim.Send_Joint(name = "Torso_BLeg", parent="Torso",
                       child="BLeg", type="revolute", position=[-0.5,0,1.5])
    pyrosim.Send_Cube(name="BLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])

    # make the sensor

    pyrosim.End()

create_robot()