import itertools
import random
import gurobipy as gp
import numpy as np
import json
import time
from gurobipy import GRB

from Entities import Solution
from Entities import SynConPVRP
from itertools import combinations, groupby
from Entities import District
from Dijkstra import Graph
from GurobiTool import GurobiProc
from Test import Test

import math
from itertools import combinations


class MshSolver:
    # Create vector of adjacent BU  (starting on random BU)
    # Create list of Districts
    quantityOfDistricts = 0
    instance = 0
    quantityOfBU = 0
    solutionLibrary = []  # Library of solutions
    solution = Solution

    def __init__(self, instance_, quantityOfDistricts_):
        self.quantityOfDistricts = quantityOfDistricts_
        self.instance = instance_
        quantityOfBU = len(self.instance.basicUnits)

    def createMSHSolution(self, fulfill_WorkBalance, fulfill_Compacity, iterations, solveIterations):
        # fulfill_WorkBalance: Flag to force the workBalance rule
        # fulfill_Compacity: Flag to force the Compacity rule
        # iterations: int. Quantity of iterations to perform
        # solveIterations: Flag to approve to solve by Gurobi each iteration (when true). When False only solved with the full library of solutions.

        districtMatrixGeneral = []
        bestFOIteration = 0
        bestDistrictsIterations = []

        start = time.time()
        id = 0
        gu = GurobiProc()
        for it in range(iterations):
            id += 1

            # if(solveIterations == True):
            #    print("Iteration: %s of %s" % (id, iterations))

            adjacentList = self.createAdjacentList()
            #print("Adjacent List: ", adjacentList)

            # print("createArcList")
            list_Combination = self.createArcList(adjacentList)

            #print("RemoveDuplicates: ")
            #print("Initial Length: ", len(list_Combination))
            list_Combination = self.removeDuplicates(list_Combination)
            #print("Final Length: ", len(list_Combination))

            # print("combinationsToDistrict")
            districtMatix = self.combinationsToDistrict(list_Combination)

            if (fulfill_WorkBalance == True):
                # print("self.instance.DeviationPermited: ",
                #      self.instance.DeviationPermited)
                districtMatix = self.workBalanceCriteria(
                    districtMatix, self.instance.DeviationPermited)

            if (fulfill_Compacity == True):
                # Must be optimized
                districtMatix = self.compacityCriteria(districtMatix)
                # print("New length of list_Combination after compacityCriteria: ", len(
                #    districtMatix))

            # for o in list_Combination:
                #print("list_Combination", (o.getListBUIndex()))

            # print("districtMatrixGeneral:")
            for ve in districtMatix:
                districtMatrixGeneral.append(ve)

            # print("Gurobi_1")
            # Gurobi:
            #gu = GurobiProc()

            # With The flag: solveIterations It is possible to choose one versión of algorithm or another.
            if(solveIterations == True):
                print("*** Iteration: ***", id)
                print("calculating Distances:")
                distanceVector = self.calculateDistances(districtMatix)
                print("distanceVector in Iterations:", len(distanceVector))
                sol = gu.gurobiSolver(districtMatix, self.instance,
                                      distanceVector, self.quantityOfDistricts)
                if (sol != []):
                    # Keep every solution with its districts
                    self.solutionLibrary.append(sol)

                    # Save the best solution between Iterations
                    if (bestFOIteration == 0):
                        bestFOIteration = round(sol[1], 2)
                        bestDistrictsIterations = sol[0]
                    else:
                        if(round(sol[1], 2) < bestFOIteration):
                            bestFOIteration = round(sol[1], 2)
                            bestDistrictsIterations = sol[0]
                end = time.time()

                print("/////////////////////// ITERATIONS ///////////////////////")
                print("bestFOIteration", bestFOIteration)
                print("Excecution Time of Iterations: ", end-start)

        distanceVectorGeneral = []

        # PRINTING DISTRICT MATRIX:
        # print("Printing District Matrix:")
        # z = 0
        # for g in districtMatrixGeneral:
        #     print("District %s: %s" % (z, g.printDistrict()))
        #     z = z+1

        print("Calculate Distances2:")
        # calculateDistances must be optimized
        distanceVectorGeneral = self.calculateDistances(districtMatrixGeneral)
        print("/////////////////////// distanceVectorGeneral ///////////////////////")
        #print("distanceVectorGeneral:", distanceVectorGeneral)

        print("Gurobi_General:")
        start = time.time()
        # Solve for all districts of previous solutions
        solG = gu.gurobiSolver(districtMatrixGeneral, self.instance,
                               distanceVectorGeneral, self.quantityOfDistricts)
        end = time.time()

        print("/////////////////////// GENERAL ///////////////////////")
        bestDistricts = []
        if (solG != []):
            print("sol_General: ", solG[1], 2)
            print("sol_General: ", round(solG[1], 2))
            print("Excecution Time of General: ", end-start)

            if((round(solG[1], 2) < bestFOIteration) or bestFOIteration == 0):
                print("The best solution was gotten with General (all districts): %s",
                      round(solG[1], 2))

                if (bestFOIteration > 0):
                    print("The general Solution (All Districts) has an improvement of:",
                          "{0:.1%}".format((bestFOIteration-round(solG[1], 2))/bestFOIteration))
                self.solution.districtMatrix = solG[0]
                bestDistricts = solG[0]
            else:
                self.solution.districtMatrix = bestDistrictsIterations
                bestDistricts = bestDistrictsIterations
                print("The best solution was gotten withing the iterations: ",
                      bestFOIteration)
        i = 1
        for bd in bestDistricts:
            print("District %s: %s" % (i, bd.getListBUIndex()))
            i += 1

        self.solution.districtMatrix = bestDistricts

        # Validate te solution
        # print("///////////////////////////////// SOLUTION VALIDATION  ////////////////"),
        # test = Test(self.solution, self.instance, self.quantityOfDistricts)
        # test.checkSolution()

        # Dijkstra
        #costMatrix = self.omegaMatrix(adjacentList, list_Combination)
        #g = Graph(len(adjacentList))
        #g.graph = costMatrix
        # g.dijkstra(0)  # Resuelve con Dijkstra
        return self.solution

    def createAdjacentList(self):
        # Order the list of BU in adjacent order starting from a random
        buIndexList = []
        #print("len(buIndexList)", len(buIndexList))
        #print("len(self.instance.basicUnits)", len(self.instance.basicUnits))
        cycles = 0  # Measure the quantity of times it is excecuted unsusscessfuly becaus of the lack of adjacents

        while (len(buIndexList) < len(self.instance.basicUnits)):
            randomElement = random.choice(self.instance.basicUnits)

            buIndexList.append(int(randomElement.id))
            i = 0
            inside = True
            randomElement = randomElement.id
            while(inside):
                i += 1
                #print("i", i)
                adjacentList1 = self.instance.getAdjacencybyId(randomElement)
                adjacentList = []
                adjacentList = [int(x) for x in adjacentList1]
                adjacentList = list(set(adjacentList).difference(buIndexList))

                #print("len(adjacentList)", len(adjacentList))

                if(len(adjacentList) > 0):
                    randomElement = random.choice(adjacentList)
                    buIndexList.append(int(randomElement))

                    # print("len(self.instance.basicUnits)",
                    #      len(self.instance.basicUnits))

                    #print("len(buIndexList)", len(buIndexList))

                    if (len(adjacentList) == 0 and i > len(self.instance.basicUnits)):
                        # No AdjacentList was fully achieved
                        inside = False
                        buIndexList = []
                        print("No AdjacentList was fully achieved")
                        raise Exception("There 1")

                    if (len(buIndexList) == len(self.instance.basicUnits)):
                        inside = False
                else:
                    inside = False
                    adjacentList = []
                    buIndexList = []
                    cycles += 1
                    print("cycles: ", cycles)
                    # When there isn't enough adjacents in input data, it repeats itself
                    if (cycles > len(self.instance.basicUnits)):
                        raise Exception(
                            "There isn't enough adjacency in the dataset.")
        buIndexList.append("T")  # validar si se requiere.
        return buIndexList

    def createArcList(self, adjacentList):
        # Build Arcs
        list_Combination = list()
        for i in range(len(adjacentList)):
            for j in range(i+1, len(adjacentList)+1):
                list_Combination += list([adjacentList[i:j]])

        #print("list_Combination_length", len(list_Combination))
        #print("list_Combination", (list_Combination))

        return list_Combination

    def removeDuplicates(self, Ks):
        result = []
        [result.append(x) for x in Ks if x not in result]

        return result

    def combinationsToDistrict(self, list_Combination_):
        districtMatrix = []
        # optimize: add a lot of BU in one step to every district and then update
        for dis in list_Combination_:
            district = District()  # Empty District
            for item in dis:
                # Chose the BU according to the index:
                w = [y for y in self.instance.basicUnits if y.id == item]
                if (w != []):
                    #print("w", w)
                    x = w[0]
                    # for x in self.instance.basicUnits:
                    #     if (x.id == item):

                    # /////////////// INCREMENTAL SOLUTION FOR DISTANCE//////////////
                    # print("updateDistance")
                    #district.updateMaxDistance(self.instance, x)
                    district.updateSumDistance(self.instance, x)
                    # //////////////////////////////////////////////////
                    # print("addBasicUnits")
                    district.addBasicUnits(x)
                    # print("updateWorkLoad")
                    district.updateWorkLoad("Add", x)
                    # district.setWorkLoad()  # Update workload of District (wl)
            districtMatrix.append(district)

        #print("Districts: ", len(districtMatrix))
        return districtMatrix

    def workBalanceCriteria(self, districtMatix, Tao):
        # Calculate workload and remove ones with excess workload
        # districtMatix is a list of Districts

        list_Combination = districtMatix

        if(self.quantityOfDistricts > 0):
            avWorkLoad = self.instance.WL/self.quantityOfDistricts  # AverageWorkLoad
            if Tao > 0:
                workLoadLimit = (1+Tao)*avWorkLoad
            for dis in districtMatix:
                #print("Interm1: ", workLoadLimit)
                if(len(dis.setBasicUnits) > 1):
                    if(dis.wl > workLoadLimit):
                        list_Combination.remove(dis)
                # else:
                #    list_Combination.remove(dis)
            print("Final1_With WorkBalance Criteria: ", len(list_Combination))
        return list_Combination

    def compacityCriteria(self, districtMatix):
        # Calculate Distances and remove ones with excess Distance
        list_Combination = districtMatix

        if(self.quantityOfDistricts > 0):
            maxDistance = self.instance.maxDistance  # maxDistance
            for dis in districtMatix:
                #print("Interm1: ", dis.setBasicUnits)
                if(len(dis.setBasicUnits) > 1):
                    if(dis.distance > maxDistance):
                        # if(dis.maxDistancesDistrict(self.instance) > maxDistance):
                        list_Combination.remove(dis)
                else:
                    list_Combination.remove(dis)
            #print("Final2_With Compacity Criteria: ", len(list_Combination))
        return list_Combination

    def calculateDistances(self, districtMatix):
        distanceVector = []

        print("len(districtMatix)", len(districtMatix))

        for dis in districtMatix:
            # distanceVector.append(dis.sumDistancesDistrict(self.instance))
            # distanceVector.append(dis.maxDistancesDistrict(self.instance))
            # When it has been previously calculated
            distanceVector.append(dis.distance)
            # updateMaxDistance
            #print("District Distance: ", distanceVector)
        return distanceVector

    def omegaMatrix(self, adjacentList, list_Combination):
        # Calculate the Matrix cost
        vertex = len(adjacentList)
        self.graph = [[0 for column in range(vertex)]
                      for row in range(vertex)]
        for dist in list_Combination:
            if (len(dist.setBasicUnits) > 0):
                first = (dist.setBasicUnits[0]).id
                if (first == 'T'):
                    first = len(adjacentList)
                #print("first", first)
                last = (dist.getLastBU()).id
                if (last == 'T'):
                    next = len(adjacentList)-1
                    #print("last", last)
                else:
                    next = self.getNextBU(last, adjacentList)
                #print("next", next)
                if (next == 'T'):
                    next = len(adjacentList)-1
                self.graph[first][next] = dist.workLoadBalance()
                self.graph[next][first] = dist.workLoadBalance()
        print(self.graph)
        return self.graph

    def getNextBU(self, last, adjacentList):
        return adjacentList[adjacentList.index(last)+1]
