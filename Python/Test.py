"""
Created on Fri April 29 09:40:22 2021

@author: Carlos Alberto Sánchez

"""

from Entities import Solution
from Entities import SynConPVRP
from Entities import BasicUnit
from Entities import District


class Test:
    solution = Solution
    instance = 0
    requiredDistricts = 0

    def __init__(self, solution_, instance_, requiredDistricts_):
        self.solution = solution_
        self.instance = instance_
        self.requiredDistricts = requiredDistricts_

    def checkSolution(self):
        print("Test Results: ")
        # self.instance.basicUnits.append(
        #    BasicUnit(17, 5, 5, 5))  # To validate test
        sameSetAnswer = self.validateSameSet(
            self.instance.basicUnits, self.solution.districtMatrix)
        if (sameSetAnswer == True):
            print("Test of solution set completed: O.K")

        # self.solution.districtMatrix.append(District())
        quantityOfDistrictAnswer = self.validateQuantityOfDistricts(
            self.solution.districtMatrix, self.requiredDistricts)
        if (quantityOfDistrictAnswer == True):
            print("Test of quantity of Districts in solution: O.K")

        emptyDistrictAnswer = self.validateEmptyDistricts(
            self.solution.districtMatrix)
        if (emptyDistrictAnswer == True):
            print("Test of empty Districts in solution: O.K")

        averageWorkLoadAnswer = self.validateAverageWorkLoadDistricts(
            self.solution.districtMatrix)
        if (averageWorkLoadAnswer == True):
            print("Test of Average Work Load Districts in solution: O.K")
        else:
            print("Test of Average Work Load Districts in solution: FAILED")

        maxCompactnessAnswer = self.validateMaxCompactness(
            self.solution.districtMatrix, self.instance.maxDistance)
        if(maxCompactnessAnswer == True):
            print("Test of Max Compactness in solution: O.K")
        else:
            print("Test of Max Compactness in solution: FAILED")

        adjacencyValidationAnswer = self.validateAdjacency(
            self.instance, self.solution.districtMatrix)
        if(adjacencyValidationAnswer == True):
            print("Test of Adjacency in solution: O.K")
        else:
            print("Test of Adjacency in solution: FAILED")

    def validateSameSet(self, originalBUSet_, assignedBUSet_):
        # Validate that every BU is assigned in the solution
        answer = False

        originalBUSet = []
        assignedBUSet = []

        for item in originalBUSet_:
            originalBUSet.append(item.id)
        originalBUSet.sort()

        for dist in assignedBUSet_:
            for item1 in dist.setBasicUnits:
                assignedBUSet.append(item1.id)
        assignedBUSet.sort()

        if (originalBUSet == assignedBUSet):
            answer = True
        else:
            print(
                "There is a problem, the solution set does not contains all the BU. Original set is: %s, assigned Set is: %s" % (originalBUSet, assignedBUSet))
            raise Exception(
                "There is a problem, the solution set does not contains all the BU.")
        return answer

    def validateQuantityOfDistricts(self, districtMatrix, requiredDistricts):
        # validate that quantity of Districts in solution match required quantity
        answer = False
        if (len(districtMatrix) == requiredDistricts):
            answer = True
        else:
            print(
                "There is a problem, the solution has a different quantity of Districts. Required number is: %s, Districts in the solution: %s" % (requiredDistricts, len(districtMatrix)))
            raise Exception(
                "There is a problem, the solution has a different quantity of Districts than requested.")
        return answer

    def validateEmptyDistricts(self, districtMatrix):
        answer = True
        for item in districtMatrix:
            if (len(item.setBasicUnits) == 0):
                answer = False
                print(
                    "There is a problem, the solution has an empty District.")
                raise Exception(
                    "There is a problem, the solution has an empty District.")
        return answer

    def validateAverageWorkLoadDistricts(self, districtMatrix):
        # Validate that each district has a workload below average
        answer = True
        notInAverage = []
        if (len(districtMatrix) > 0):
            averageWorkLoad = (self.instance.WL) / \
                len(districtMatrix)  # Get WorkLoad Average

            for item in districtMatrix:
                if (item.wl > averageWorkLoad):
                    answer = False
                    for obj in item.setBasicUnits:
                        notInAverage.append(obj.id)
                    if (len(notInAverage) > 0):
                        print(
                            "There is a problem, these District has a workload (%s) upper than average(%s)." % (round(item.wl, 2), round(averageWorkLoad, 2)), notInAverage)
                    notInAverage = []
        else:
            answer = False

        return answer

    def validateMaxCompactness(self, districtMatrix, distMax):
        # Validate that max distance between BU is lower than the read parameter
        i = 0
        answer = True
        listMaxDistance = []
        for di in districtMatrix:
            distances = []
            pairs = di.pairsBU()
            for x in pairs:
                # print(x)
                distances.append(self.instance.distance(x))
                # print(self.instance.distance(x))
            if(len(distances) > 0):
                listMaxDistance.append(max(distances))
                #print("Compactness ", i, " ", max(distances))
            i += 1
        maxDitance = max(listMaxDistance)
        if(maxDitance > float(distMax)):
            answer = False
            print("Max Compactness expected was %s, but gotten %s" %
                  (distMax, maxDitance))
        return answer

    def validateAdjacency(self, inst, matrixDistrict_):
        answer = True
        # Choose every BU and Check that be adjacent to at least one BU in each District (checking the adjacency vector of each district):
        # If not then there is a problem of adjacenty in such District
        districtNumber = 0
        for dis in matrixDistrict_:
            districtNumber = districtNumber+1
            if(len(dis.setBasicUnits) > 1):
                adjList = inst.getAdjacencybyDistrict(dis)
                for bu in dis.setBasicUnits:
                    if (float(bu.id) not in adjList):
                        answer = False
                        print("%s Basic Unit is not in adjacency of District %s" %
                              (bu.id, districtNumber,))
                        raise Exception(
                            "A Basic Unit is not adjacenty to the other in a District")
        return answer
