import pybullet as p

class World:
    def __init__(self):
        p.loadURDF("plane.urdf")
