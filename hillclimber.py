from solution import SOLUTION
import random
from constants import numberOfGenerations

class HILL_CLIMBER:
    def __init__(self):
        self.parent = SOLUTION()

    def Evolve(self):
        self.parent.Evaluate("DIRECT")  # 초기 솔루션 평가
        for currentGeneration in range(numberOfGenerations):  # 여러 세대 반복
            self.Evolve_For_One_Generation()
        self.Show_Best()  # 최종 솔루션 GUI로 표시


    def Evolve_For_One_Generation(self):
        self.Spawn()  # 자식 생성
        self.Mutate()  # 자식 변이
        self.child.Evaluate("DIRECT")  # 자식 평가 (DIRECT 모드)
        self.Print()  # 부모와 자식 피트니스 출력
        self.Select()  # 부모 교체 여부 결정

    
    def Spawn(self):
        import copy
        self.child = copy.deepcopy(self.parent)  # parent의 깊은 복사


    def Mutate(self):
        self.child.Mutate()
        #print("Parent Weights:")
        #print(self.parent.weights)
        #print("Child Weights:")
        #print(self.child.weights)



    def Select(self):
        # 부모와 자식의 피트니스 출력
        #print(f"Parent Fitness: {self.parent.fitness}, Child Fitness: {self.child.fitness}")
        # 부모가 자식보다 나쁜 경우 교체
        if self.child.fitness > self.parent.fitness:
            self.parent = self.child

    def Print(self):
        print(f"Parent: {self.parent.fitness}, Child: {self.child.fitness}")

    def Show_Best(self):
        # 최적의 부모 솔루션 찾기
        bestParent = None
        bestFitness = float('inf')  # 초기값을 무한대로 설정

        for parent in self.parents.values():
            if parent.fitness < bestFitness:
                bestFitness = parent.fitness
                bestParent = parent

        # GUI 모드로 최적의 부모 솔루션 재시뮬레이션
        if bestParent:
            print(f"Re-simulating the best solution with fitness: {bestFitness}")
            bestParent.Start_Simulation("GUI")
