# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 09:26:33 2021

@author: Carlos Alberto Sánchez
"""
import imp
from itertools import combinations
from Entities import SynConPVRP  # Name of the class for the problem
from Entities import CompatibilityIndex
from Entities import Distance
from Entities import DistrictInProblem
from Entities import BasicUnit
from Entities import Adjacency
from Entities import District
from Entities import Solution
# from Entities import RandomSolver
from Test import Test
from RandomSolver import RandomSolver
from MshSolver import MshSolver
from Dijkstra import Graph
from InputValidator import InputValidator
import time
import itertools

if __name__ == "__main__":
    print("Execution on ")
    start = time.time()
    # Read Instance

    # vowel(3)

    # instance = SynConPVRP(
    #     "E:/CARLOS/Ude@/TESIS/Desarrollo/Python/Instancias/instancia_16UBMedellin.txt")

    # instance = SynConPVRP(
    #     "E:/CARLOS/Ude@/TESIS/Desarrollo/Python/Instancias/instancia_29UBCopacabana.txt")

    # instance = SynConPVRP(
    #     "E:/CARLOS/Ude@/TESIS/Desarrollo/Python/Instancias/instancia_44UBEnvigado.txt")

    # instance = SynConPVRP(
    #     "E:/CARLOS/Ude@/TESIS/Desarrollo/Python/Instancias/instancia_60UB_Itagui.txt")

    # instance = SynConPVRP(
    #     "E:/CARLOS/Ude@/TESIS/Desarrollo/Python/Instancias/instancia_78UB_Bello.txt")

    # instance = SynConPVRP(
    #     "E:/CARLOS/Ude@/TESIS/Desarrollo/Python/Instancias/instancia_104UB_Envi_Itagui.txt")

    # instance = SynConPVRP(
    #     "E:/CARLOS/Ude@/TESIS/Desarrollo/Python/Instancias/instancia_107UB_Bello.txt")

    instance = SynConPVRP(
        "E:/CARLOS/Ude@/TESIS/Desarrollo/Python/Instancias/instancia_270UB_Medellin.txt")

    instance.read_data()
    ip = InputValidator(instance)
    ip.checkInput()
    # print(instance.distances)

    # requiredDistricts = 7
    iterations = 100

    #print("/////// Random Solution: /////")
    #randomSolver = RandomSolver(instance, instance.numDist)
    #solution_ = randomSolver.createRandomSolution()

    #print("/////// Validation of Random Solution /////")
    #test = Test(solution_, instance, instance.numDist)
    # test.checkSolution()

    print("/////// MSH Solution: /////")
    msh = MshSolver(instance, instance.numDist)
    fulfill_WorkBalance = False
    fulfill_Compacity = True
    solveIterations = False  # Version 2: False
    mshSolution = msh.createMSHSolution(
        fulfill_WorkBalance, fulfill_Compacity, iterations, solveIterations)

    #print("/////// Validation of MSH Solution /////")
    #test = Test(mshSolution, instance, instance.quantityOfDistricts)
    # test.checkSolution()

    finish = time.time()
    print("Total Time: ", finish-start)
