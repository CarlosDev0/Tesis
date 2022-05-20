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
#from Entities import RandomSolver
from Test import Test
from RandomSolver import RandomSolver
from MshSolver import MshSolver
from Dijkstra import Graph

if __name__ == "__main__":
    print("Execution on ")
    # Read Instance
    instance = SynConPVRP(
        "E:/CARLOS/Ude@/TESIS/Desarrollo/Python/instanciapr01 5-1-1-1-1.txt")
    instance.read_data()
    # print(instance.distances)

    requiredDistricts = 7
    randomSolver = RandomSolver(instance, requiredDistricts)
    solution_ = randomSolver.createRandomSolution()

    test = Test(solution_, instance, requiredDistricts)
    test.checkSolution()

    msh = MshSolver(instance, requiredDistricts)
    fulfill_WorkBalance = True
    fulfill_Compacity = True
    msh.createMSHSolution(fulfill_WorkBalance, fulfill_Compacity)

    # msh.gurobi()
    # msh.gurobiExample()

    # Driver program
    # g = Graph(9)
    # g.graph = [[0, 4, 0, 0, 0, 0, 0, 8, 0],
    #            [4, 0, 8, 0, 0, 0, 0, 11, 0],
    #            [0, 8, 0, 7, 0, 4, 0, 0, 2],
    #            [0, 0, 7, 0, 9, 14, 0, 0, 0],
    #            [0, 0, 0, 9, 0, 10, 0, 0, 0],
    #            [0, 0, 4, 14, 10, 0, 2, 0, 0],
    #            [0, 0, 0, 0, 0, 2, 0, 1, 6],
    #            [8, 11, 0, 0, 0, 0, 1, 0, 7],
    #            [0, 0, 2, 0, 0, 0, 6, 7, 0]
    #            ]
    # https://quescol.com/data-structure/dijkstras-algorithm

    # g = Graph(6)
    # g.graph = [[0, 7, 12, 0, 0, 0],
    #            [7, 0, 2, 9, 0, 0],
    #            [12, 2, 0, 0, 0, 0],
    #            [0, 9, 0, 0, 4, 1],
    #            [0, 0, 0, 4, 0, 5],
    #            [0, 0, 0, 1, 5, 0]
    #            ]
    # g.dijkstra(0)
