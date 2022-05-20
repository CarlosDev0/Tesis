from Entities import SynConPVRP  # Name of the class for the problem
from Entities import Solution
from Entities import District
import numpy as np

import random


class RandomSolver:
    pvr = SynConPVRP
    q = int
    solution = Solution
    quantityOfDistricts = int
    quantityOfDistricts = 0

    choosenBU = []  # Basic Units that are already choosen for the solution
    remainingBasicUnits = []  # Basic Units available to be assigned to a District

    def __init__(self, pro, quantityOfDistricts_):
        self.pvr = pro

        if(quantityOfDistricts_ > len(self.pvr.basicUnits) or (quantityOfDistricts_ == 0)):
            # Excepción e interrumpir ejecución
            raise Exception(
                "A solution could not be created. Please check that the quantity of Districts be lower than the quantity of Basic Units and greater than cero")
        else:
            self.quantityOfDistricts = quantityOfDistricts_

    def createEmptySolution(self):
        if (int(self.quantityOfDistricts) > 0):
            self.createRandomSolution()

    def createRandomSolution(self):
        if (int(self.quantityOfDistricts) > 0):
            for b in self.pvr.basicUnits:
                self.remainingBasicUnits.append(b)

            averageWorkLoad = (self.pvr.WL) / \
                self.quantityOfDistricts  # Get WorkLoad Average

            print("Total WorkLoad: ", self.pvr.WL)
            print("averageWorkLoad: ", averageWorkLoad)

            # Assign one BU to each District:
            for n in range(self.quantityOfDistricts):
                # create the quantity of Districts required
                # Assign BU to each District
                district = District()  # Empty District
                selectedBU = self.remainingBasicUnits.pop(
                    random.randrange(len(self.remainingBasicUnits)))
                district.addBasicUnits(selectedBU)

                # Update workload of District (wl) adding wl of new BU
                district.updateWorkLoad("Add", selectedBU)
                # district.setWorkLoad()  # Update workload of District (wl)
                self.choosenBU.append(selectedBU)
                # Insert District in matrix solution
                self.solution.districtMatrix.append(district)

            for newDistrict in self.solution.districtMatrix:

                if(len(self.choosenBU) < len(self.pvr.basicUnits)):
                    selectedBU = newDistrict.getLastBU()

                    print("BU Seleccionada: ", selectedBU.getId())

                    self.printListId(self.choosenBU, "choosenBU")

                    # While District wl is lower than average
                    goon = True
                    randomBU = 0
                    while(goon):
                        # There is still BU to be assigned?
                        if(len(self.choosenBU) >= len(self.pvr.basicUnits)):
                            goon = False
                        else:
                            # Workload limit (of current District) has been gotten?
                            if (newDistrict.wl >= averageWorkLoad):
                                goon = False
                            else:
                                # Add adyacent BU to the same district
                                # self.adjacencies  Determinar una de las BU adyacentes ala última y seleccionarla.

                                # Validar si todavía hay BU disponibles:
                                randomBU = self.randomBUAdjacent(
                                    selectedBU, newDistrict)

                                if (randomBU != False):
                                    print("Received: ", randomBU.id)
                                    newDistrict.addBasicUnits(
                                        randomBU)
                                    # Update workload of District (wl)
                                    newDistrict.updateWorkLoad("Add", randomBU)
                                    self.choosenBU.append(randomBU)
                                    self.printListId(
                                        self.remainingBasicUnits, "Before: self.remainingBasicUnits: ")

                                    print("BU to Remove:", randomBU.id)

                                    self.remainingBasicUnits.remove(randomBU)

                                    self.printListId(
                                        self.remainingBasicUnits, "After: self.remainingBasicUnits: ")
                                else:
                                    goon = False  # There is no adjacent BU available

                    # Insert District in matrix solution
                    print("Districts in Solution: ", len(
                        self.solution.districtMatrix))
                    print("Random District: ", newDistrict.printQuantity())
                else:
                    next_ = False

            ##########################################
            # Assign remaining BU into Districts randomly
            remain = True
            while (remain):
                print("cantidad de BU faltantes: ",
                      len(self.remainingBasicUnits))

                if(len(self.remainingBasicUnits) > 0):
                    # Validar adjacencia antes de asignarla a un distrito.
                    adjacentList = []
                    for d in self.solution.districtMatrix:  # Get adjacentList of each district
                        adjacentList.append(self.pvr.getAdjacencybyDistrict(d))

                    #print("remainingBasicUnits", self.remainingBasicUnits)

                    bu = self.remainingBasicUnits.pop()

                    i = 0
                    for d in self.solution.districtMatrix:
                        if hasattr(bu, 'id'):
                            if(bu.id in adjacentList[i]):
                                # print("adjacentList %s , list: %s" %
                                #      (i, adjacentList[i]))
                                d.addBasicUnits(bu)
                                d.updateWorkLoad("Add", bu)
                                bu = ""
                                # break
                        i += 1
                else:
                    remain = False

        self.printInfoSolution()
        return self.solution

    def randomBUAdjacent(self, rBU, newDistrict):
        # Generates a new random number not choosen before and adjacent to a BU

        # self.adjacencies  Determinar una de las BU adyacentes ala última y seleccionarla.
        inside_ = True
        randomBU = False

        # Choose a random BU between 0 and len(self.pvr.basicUnits)-1
        # Returns the list of Adjacent BU of a BU.
        adjacentList = []  # list of indexes of adjacent BU
        print("Received BU: ", rBU.id)

        # Function to get adjacency list by District
        adjacentList = self.getAdjacencybyDistrict(newDistrict)

        print("adjacentList_8: ", adjacentList)

        if(len(adjacentList) > 0):  # It has adjacents?
            # remains some adjacent BU that has not been choosen yet.

            intersect = []
            for bu in adjacentList:

                interm = (x for x in self.remainingBasicUnits if x.id == bu)
                for ob in interm:
                    intersect.append(ob)
                    #intersect.append(intersect, ob, axis=None)

            if ("[[]]" in intersect):
                intersect.remove("[[]]")
            self.printListId(intersect, "intersect:_9: ")
            intersect = [ele for ele in intersect if ele != []]
            self.printListId(intersect, "Intersect wihtout []_10: ")

            if (len(intersect) > 0):
                if (intersect != [[]]):
                    randomBU = np.random.choice(intersect)

        return randomBU

    def getAdjacencybyId(self, row_):
        # Returns the list of id adjacent to ONE BU received
        results = np.array([])
        for a in self.pvr.adjacencies:
            if (np.logical_and(a.row == row_, int(a.adjac) == 1)):

                results = np.append(results, a.col,  axis=None)
        return results

    def getAdjacencybyDistrict(self, district):
        # Returns the list of id adjacent to each BU of the District received

        results = np.array([])
        for d in district.setBasicUnits:
            row_ = d.id
            #print("row_: ", row_)
            listGotten = self.getAdjacencybyId(row_)
            listGotten = listGotten.astype(int)
            #print("listGotten: ", listGotten)
            for lg in listGotten:
                #print("itemGotten: ", int(lg))
                results = np.append(results, int(lg),  axis=None)

        results = list(dict.fromkeys(results))  # remove duplicates
        #print("results_Adjacenty_District: ", results)
        return results

    def printListId(self, listReceived, textToPrint):
        ichosen = []
        ichosen.append([x.id for x in listReceived])
        print(textToPrint, ichosen)

    def printInfoSolution(self):
        print("Solution Summary: ")
        print("Quantity of Basic Units:_", len(self.pvr.basicUnits))
        print("Quantity of Districts:_", len(self.solution.districtMatrix))

        i = 0
        for d in self.solution.districtMatrix:
            i += 1
            print("District %d: " % i, d.printQuantity())
        i = 0
        for d in self.solution.districtMatrix:
            i += 1
            print("District %d: " % i, d.printDistrict())
