import pybullet as p
import pybullet_data
import pyrosim.pyrosim as pyrosim
import time
import numpy
import os

physicsClient = p.connect(p.GUI)
p.setRealTimeSimulation(1)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0, 0, -9.8)

p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSV = numpy.zeros(10000)


for i in range(500):
    p.stepSimulation()
    backLegSV[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("LLeg")

    time.sleep(1 / 60)

p.disconnect()
data_directory = "data"
os.makedirs(data_directory, exist_ok=True)
output_filename = os.path.join(data_directory, "backLegSensorValues.npy")
numpy.save(output_filename, backLegSV)
print(f"Sensor values saved to {output_filename}")