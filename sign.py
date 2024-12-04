import numpy
import matplotlib.pyplot as plt

# 설정값 정의
num_steps = 1000  # 시뮬레이션 스텝 수
amplitude = numpy.pi /6  # 진폭: -π/4 ~ +π/4
frequency = 20  # 주파수
phase_offset = 0  # 초기 위상 오프셋

# 사인파 생성
t = numpy.linspace(0, 2 * numpy.pi * frequency, num_steps)  # 0에서 2π까지 선형 분포 생성
target_angles = amplitude * numpy.sin(t + phase_offset)  # 사인파 계산 및 스케일링

# 생성된 벡터 저장 및 그래프 출력
numpy.save("motor_values.npy", target_angles)  # 파일 저장
plt.plot(t, target_angles)  # 그래프 출력
plt.xlabel("Time Step")
plt.ylabel("Target Angle (radians)")
plt.title("Sinusoidal Motor Command")
plt.show()