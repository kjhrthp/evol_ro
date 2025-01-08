import sys
from simulation import SIMULATION
# main 코드에서 실행 방식 확인
directOrGUI = sys.argv[1]  # DIRECT 또는 GUI
simulation = SIMULATION(directOrGUI)
simulation.run()
simulation.Get_Fitness()