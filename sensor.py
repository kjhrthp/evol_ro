import numpy
import pyrosim.pyrosim as pyrosim
from constants import steps
class SENSOR:
    def __init__(self, linkName):
        self.linkName = linkName
        self.values = numpy.zeros(steps)  # 1000 스텝 동안의 데이터 저장

    def get_value(self, t):
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
        #print(self.values[t]) Removed print(self.values[t])