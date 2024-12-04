import numpy
import pyrosim.pyrosim as pyrosim
import constants as c

class MOTOR:
    def __init__(self, jointName, phaseOffset):
        self.jointName = jointName
        self.amplitude = c.amp # 진폭
        self.frequency = c.freq  # 주파수
        self.offset = phaseOffset     # 고유 위상 설정
        self.motorValues = numpy.zeros(c.steps)  # 모터 값 저장 배열
        self.prepare_to_act()

    def prepare_to_act(self):
        t = numpy.linspace(0, 2 * numpy.pi, c.steps)  # 시간 값 생성
        self.motorValues = self.amplitude * numpy.sin(self.frequency * t + self.offset)  # 위상 적용

    def set_value(self, t, robotId):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName=self.jointName,
            controlMode=pyrosim.p.POSITION_CONTROL,
            targetPosition=self.motorValues[t],
            maxForce=c.max_F
        )
