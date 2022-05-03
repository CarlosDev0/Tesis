# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:26:33 2021

@author: Juan G Villegas
"""
import imp
from Entities import SynConPVRP  # Name of the class for the problem
from Entities import CompatibilityIndex
from Entities import Distance
from Entities import DistrictInProblem
from Entities import BasicUnit
from Entities import Adjacency
from Entities import District
from Entities import Solution
from Entities import RandomSolver
from Test import Test

if __name__ == "__main__":
    print("Execution on ")
    # Read Instance
    instance = SynConPVRP(
        "E:/CARLOS/Ude@/TESIS/Desarrollo/Python/instanciapr01 5-1-1-1-1.txt")
    instance.read_data()
    # print(instance.distances)

    requiredDistricts = 15
    randomSolver = RandomSolver(instance, requiredDistricts)
    solution_ = randomSolver.createRandomSolution()

    test = Test(solution_, instance, requiredDistricts)
    test.checkSolution()
