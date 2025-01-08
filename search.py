import os
from hillclimber import HILL_CLIMBER
# for i in range(5):  # 5번 반복 실행
#     print(f"Simulation {i+1}")
#     os.system("python3 generate.py")
#     os.system("python3 simulate.py")
hc = HILL_CLIMBER()
hc.Evolve()