# import pybullet as p
# import pybullet_data
# import pyrosim.pyrosim as pyrosim
# import time
# import numpy
# import random
# import constants as c
#
# physicsClient = p.connect(p.GUI)
# p.setRealTimeSimulation(1)
# p.setAdditionalSearchPath(pybullet_data.getDataPath())
# p.setGravity(0, 0, -9.8)
#
# p.loadURDF("plane.urdf")
# robotId = p.loadURDF("body.urdf")
#
# pyrosim.Prepare_To_Simulate(robotId)
#
# backLegSV = numpy.zeros(10000)
# target_angles = numpy.load("motor_values.npy")
#
# # 수정된 target_angles
# back_leg_angles = target_angles + c.back_leg_phase_offset
# front_leg_angles = target_angles + c.front_leg_phase_offset
#
# for i in range(1000):
#     p.stepSimulation()
#     backLegSV[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("LLeg")
#     pyrosim.Set_Motor_For_Joint(
#         bodyIndex=robotId,
#         jointName="Torso_RLeg",
#         controlMode=p.POSITION_CONTROL,
#         targetPosition=back_leg_angles[i],
#         maxForce=c.max_F
#     )
#     pyrosim.Set_Motor_For_Joint(
#         bodyIndex=robotId,
#         jointName="Torso_LLeg",
#         controlMode=p.POSITION_CONTROL,
#         targetPosition=front_leg_angles[i],
#         maxForce=c.max_F
#     )
#     time.sleep(1 / 60)
#
# p.disconnect()
# #data_directory = "data"
# #os.makedirs(data_directory, exist_ok=True)
# #output_filename = os.path.join(data_directory, "backLegSensorValues.npy")
# #numpy.save(output_filename, backLegSV)
# #print(f"Sensor values saved to {output_filename}")
from world import World
from robot import ROBOT
import pybullet as p
import pybullet_data
import constants as c
import time

class Simulation:
    def __init__(self):
        self.physicsClient = p.connect(p.GUI)
        p.setRealTimeSimulation(1)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)

        self.world = World()
        self.robot = ROBOT()

    def run(self):
        for t in range(c.steps):
            p.stepSimulation()
            self.robot.sense(t)
            self.robot.act(t)
            time.sleep(c.time_step)

    def __del__(self):
        p.disconnect()