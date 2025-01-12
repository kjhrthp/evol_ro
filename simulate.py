import sys
from simulation import SIMULATION

directOrGUI = sys.argv[1]  # DIRECT 또는 GUI
solutionID = sys.argv[2]  # 솔루션 ID

simulation = SIMULATION(directOrGUI, int(solutionID))
simulation.run()
simulation.Get_Fitness()
