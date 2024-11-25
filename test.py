import pybullet as p
import pybullet_data
import time

# 1. PyBullet GUI 모드로 연결
physicsClient = p.connect(p.GUI)

# 2. PyBullet 기본 데이터 경로 설정
p.setAdditionalSearchPath(pybullet_data.getDataPath())

# 3. 디버그 비주얼라이저 설정 (물리 서버 연결 후 호출 가능)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 1)  # GUI 활성화

# 4. 샘플 SDF 파일 로드
p.loadSDF("stadium.sdf")

# 5. 무한 루프를 통해 시뮬레이션 실행 상태 유지
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    p.disconnect()  # 물리 서버 연결 해제
