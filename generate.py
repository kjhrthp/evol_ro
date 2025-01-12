import pyrosim.pyrosim as pyrosim

def create_robot():
    pyrosim.Start_URDF("body.urdf")
    pyrosim.Send_Cube(name="Torso", pos=[0, 0, 0.5], size=[1, 1, 1])
    # should be named "Parent_Child"
    pyrosim.Send_Joint(name = "Torso_Leg", parent="Torso",
                       child="Leg", type="revolute", position=[0.5,0,1])
    # child로 지정된 Leg는 joint의 상대위치이다.
    pyrosim.Send_Cube(name="Leg", pos=[0.5, 0, 0.5], size=[1, 1, 1])
    pyrosim.End()

create_robot()