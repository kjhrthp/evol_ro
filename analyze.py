import numpy as np
import matplotlib.pyplot as plt

# 데이터 로드
backLegSensorValues = np.load("data/backLegSensorValues.npy")

# 시뮬레이션 단계 수 (500)
simulation_steps = 500

# 사용된 센서 값만 선택 (전체 배열 중 앞의 500개)
backLegSensorValues = backLegSensorValues[:simulation_steps]

# 그래프 그리기 - 점으로 표시하기 위해 'o' 마커 사용, 선은 없앰
plt.plot(backLegSensorValues, 'o', markersize=1, label="Back Leg")

# x축 범위 설정 (0부터 500)
plt.xlim(0, simulation_steps)

# y축 범위 설정 (0부터 1.5)
plt.ylim(-1.5, 1.5)

# 축 레이블 추가
plt.xlabel("Simulation Step")
plt.ylabel("Touch Sensor Value")

# 그래프 제목 추가
plt.title("Back Leg Touch Sensor Values Over Time")

# 범례 추가
plt.legend()

# 그래프 표시
plt.show()
