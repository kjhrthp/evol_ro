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