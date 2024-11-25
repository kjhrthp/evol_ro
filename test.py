import pyrosim.pyrosim as pyrosim
pyrosim.Start_SDF("boxes.sdf")
for i in range(5):
    for j in range(5):
        for k in range(10) :
            sizefactor = [0.8**k, 0.8**k, 0.8**k]
            pyrosim.Send_Cube(pos=[i-2.5, j-2.5, k+0.5], size=sizefactor)
pyrosim.End()