from solution import SOLUTION
from constants import numberOfGenerations, populationSize
import copy
import os
import subprocess

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        self.parents = {}
        self.nextAvailableID = 0  # 고유 ID 초기화
        for i in range(populationSize):
            self.parents[i] = SOLUTION(self.nextAvailableID)  # 각 솔루션에 ID 할당
            self.nextAvailableID += 1

    def Evolve(self):
        for parent in self.parents.values():
            parent.Evaluate("DIRECT")  # 초기 솔루션 평가 (GUI로 확인 가능)
        for currentGeneration in range(numberOfGenerations):
            self.Evolve_For_One_Generation()
        self.Show_Best()

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate_Children()
        self.Select()

    def Spawn(self):
        self.children = {}
        for i in self.parents.keys():
            self.children[i] = copy.deepcopy(self.parents[i])  # 부모 솔루션 복사
            self.children[i].Set_ID(self.nextAvailableID)  # 자식에게 새로운 ID 할당
            self.nextAvailableID += 1

    def Mutate(self):
        for child in self.children.values():
            child.Mutate()  # 각 자식 솔루션 변이

    def Evaluate_Children(self):
        processes = []

        # 1) 자식 파일 생성
        for child in self.children.values():
            child.create_world()
            child.Generate_Body()
            child.Generate_Brain()

        # 2) 병렬 시뮬레이션 실행
        for child in self.children.values():
            command = f"python simulate.py DIRECT {child.myID}"
            processes.append(subprocess.Popen(command, shell=True))

        # 3) subprocess 대기
        for process in processes:
            process.wait()

        # 4) fitness 파일 읽기
        for child in self.children.values():
            fitnessFileName = os.path.join(os.getcwd(), f"fitness{child.myID}.txt")
            if not os.path.exists(fitnessFileName):
                raise FileNotFoundError(f"Fitness file {fitnessFileName} not found for child {child.myID}")
            with open(fitnessFileName, "r") as f:
                child.fitness = float(f.read())
            print(f"[DEBUG] Child {child.myID} Fitness: {child.fitness}")

    def Select(self):
        for i in self.parents.keys():
            parentFitness = self.parents[i].fitness
            childFitness = self.children[i].fitness
            print(f"Parent Fitness: {parentFitness}, Child Fitness: {childFitness}")
            if childFitness > parentFitness:
                self.parents[i] = self.children[i]  # 더 나은 자식을 부모로 교체

    def Show_Best(self):
        # 1) 현재 부모들 중 최적 솔루션 찾기
        bestParent = None
        for parent in self.parents.values():
            if (bestParent is None) or (parent.fitness > bestParent.fitness):
                bestParent = parent

        # 2) 최고 성능 해만 GUI로 시뮬레이션
        bestParent.Evaluate("GUI")

