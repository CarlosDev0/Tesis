# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 10:40:22 2021

@author: Juan G Villegas & Juan Carlos Rivera

This class represents the problem structure and provided reading, writing, ploting and verification utilities

A SynConPVRP is composed of two elements:
    - Customers info: Coordinates, demands, frecuency 
    - Resource info: Presellers
                    Vehicles
    - A depot
    - A distance matrix from nodes: customers and depot

"""

# Package for regular expression reading (to read text with spaces and strings)
#from locale import DAY_1
from contextlib import nullcontext
import re
import numpy as np  # numpy for the calculation of the distances
from scipy.spatial import distance
import random
import itertools


class SynConPVRP:
    """Creates a new SynConPVRP instance with a given file name for data reading
      fname(str): name of the test instance  data file

    """
    basicUnits = []
    WL = int
    WL = 0

    def __init__(self, fname):

        self.distances = []     # Empty distance matrix
        self.dataFile = fname     # Name of the file to read the data
        self.basicUnits = []      # Empty list of basic Units
        self.compatibility = []          # Empty list of compatibility
        # Empty list of days with the duration of the route this day
        self.adjacencies = []   # Empty list of Adjacency
        # self.scenarios = []  # Empty list of scenarios
        # self.customers = []  # Empty list of customers

    def read_data(self):
        # Read the first line of the data file with the size of the problem:  N = Num customers, 	M = Num presellers, O = Num of delivery trucks T = Periods of the planning horizon, C = Num scenarios
        f_entrada = open(self.dataFile, "r")
        a = f_entrada.readline()
        b = a.split()
        aux = int(b[0])  # Auxiliary variable for data reading
        self.numDist = aux       # N Number of districts
        self.quantityOfDistricts = aux
        aux = int(b[1])
        self.numBasicUnits = aux       # M Number of basic Units
        aux = float(b[2])
        self.maxDistance = aux     # Maximum distance allowed
        aux = float(b[3])
        self.DeviationPermited = aux  # Maximum deviation permited

        # Impresión de datos:
        print("Datos Iniciales Distritos:% s UnidadesBásicas:% s DistanciaMáxima:% s DesviaciónMaxPermitida:% s" % (
            self.numDist, self.numBasicUnits, self.maxDistance, self.DeviationPermited))
        #district = District()
        # Resources section   This section reads the data of the two resources trucks and presellers
        # Basic Units section
        for i in range(self.numBasicUnits):
            a = f_entrada.readline()
            a = re.split("\t", a)
            ps = BasicUnit(int(a[0]), float(a[1]), float(
                a[2]), float(a[3]))  # id, la, lo, wl
            self.basicUnits.append(ps)
            self.WL += float(a[3])
            # district.addBasicUnits(ps)
        # Compatibility Index section
        for i in range(self.numBasicUnits):
            a = f_entrada.readline()
            a = re.split("\t", a)
            for j in range(self.numBasicUnits):
                t = CompatibilityIndex(i, j, a[j])
                self.compatibility.append(t)

        # print(self.compatibility)
        # Distance section
        n = self.numBasicUnits
        m = self.numBasicUnits
        dm = [0] * n
        for i in range(n):
            dm[i] = [0] * m

        aux = []
        for i in range(self.numBasicUnits):
            a = f_entrada.readline()
            b = re.split("\t", a)
            row = []
            # /////// SOL 2 /////////////
            # for j in range(self.numBasicUnits):
            #    t = Distance(i, j, a[j])
            # self.distances.append(t)
            # /////// SOL 3 /////////////
            for j in range(self.numBasicUnits):
                row.append(b[j])
            aux.append(row)
        self.distances = aux

        print("self.distances.shape", len(self.distances))

        # print(self.distances)
        # adjacency index section
        for i in range(self.numBasicUnits):
            a = f_entrada.readline()
            a = re.split("\t", a)
            for j in range(self.numBasicUnits):
                t = Adjacency(i, j, a[j])
                self.adjacencies.append(t)

    def distance(self, pair):
        # Distance: distance between a par of BU of the district
        result = 0
        # Version 2
        # result = float([x.dist for x in self.distances if x.row ==
        #               pair[0] and x.col == pair[1]][0])
        # version 3
        result = float(self.distances[pair[0]][pair[1]])
        # result = float(self.distances[pair[0]][pair[1]])
        # if (result == 0):
        #     p0 = pair[0]
        #     p1 = pair[1]
        #     print("distancia: 0: %s _ %s" % (p0, p1))
        #     raise Exception("Excepción")

        #print("result", result)
        #result = float(res[0])
        return result

    def getAdjacencyList(self, row):

        return ""

    def getAdjacencybyId(self, row_):
        # Returns the list of id adjacent to ONE BU received
        results = np.array([])
        m = []
        #print("row:", row_)
        res = [x for x in self.adjacencies if x.row == row_]

        for ad in res:
            m.append(ad.col)
        #print("res", m)
        results = np.array(m)
        #res = [x for x in self.adjacencies if x.row == row_ and x.adjac == 1]
        # for a in self.adjacencies:
        #     if (np.logical_and(a.row == row_, int(a.adjac) == 1)):
        #         results = np.append(results, a.col,  axis=None)
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


class BasicUnit:
    """
    id = Id of basic unit
    la = Latitude of patient
    lo = Longitude of patient
    wl = workload of the basic unit i
    """

    def __init__(self, id, la, lo, wl):
        self.id = id
        self.la = la
        self.lo = lo
        self.wl = wl

    def getId(self):
        return(self.id)


class District():
    quantity_BU = int
    wl = float  # District work load
    distance = float  # Distance of all BU of the District

    def __init__(self):
        self.setBasicUnits = []
        self.quantity_BU = 0
        self.wl = float(0)
        self.distance = float(0)
        # Carga de Trabajo   #Actualizar cuando se agrega o elimina una UB
        # Distancia máxima entre Unidades básicas (compacidad)  #Actualizar cuando se agrega o elimina una UB
        pass

    def addBasicUnits(self, basicUnit):
        self.setBasicUnits.append(basicUnit)
        self.quantity_BU += 1
        # self.updateDistrictAttributes()

    def updateDistrictAttributes(self):
        self.quantity_BU = self.setBasicUnits.count

    def removeBasicUnidLast(self):
        self.setBasicUnits.pop()
        self.quantity_BU -= 1

    def removeBasicUnidbyId(self, id):
        self.setBasicUnits.pop(id)

    def removeBasicUnitRandom(self):
        self.setBasicUnits.pop(random.randint(0, len(self.setBasicUnits)-1))

    def removeBasicUnitByBU(self, BasicUnit):
        if BasicUnit in self.setBasicUnits:
            self.setBasicUnits.remove(BasicUnit)
            self.quantity_BU -= 1

    def getListBUIndex(self):
        listBU = []
        for item in self.setBasicUnits:
            listBU.append(item.id)
        return listBU

    def printQuantity(self):
        return "Quantity of BU in district: % s " % (len(self.setBasicUnits))

    def workLoadBalance(self):
        wl = float
        wl = 0
        for bu in self.setBasicUnits:
            wl += float(bu.wl)
        return wl

    def setWorkLoad(self):
        self.wl = self.workLoadBalance()

    def updateWorkLoad(self, operant, bu):
        if(operant == "Add"):
            self.wl = float(self.wl) + float(bu.wl)
        else:
            self.wl = float(self.wl) - float(bu.wl)

    def pairsBU(self):
        # Returns the pairs of BU of the district (all combinations of pairs).
        # compactness measure i.e. the maximum distance between
        # two basic units assigned to the same district as follows:
        listBU = self.getListBUIndex()
        #print("listBU", listBU)
        pairs = self.all_pairs(listBU)
        return pairs

    def updatePairsBU(self, newBU):
        # Returns the pairs of BU of newBU with the former BU of the district.
        # compactness measure i.e. the maximum distance between
        # two basic units assigned to the same district as follows:
        result = False
        unique_combinations = []
        list_1 = []
        list_1.append(newBU.id)
        #print("newBU.id: ", newBU.id)

        #list1_permutations = itertools.permutations(list_1, 2)

        listBU = self.getListBUIndex()
        if(len(listBU) > 0):
            for var in itertools.product(list_1, listBU):
                unique_combinations.append((var[0], var[1]))
        # if(len(listBU) > 0):
        #     for a in listBU:
        #         if(newBU.id != a):  # avoid to repet the same BU
        #             unique_combinations.append((newBU.id, a))

            if(unique_combinations != []):
                result = unique_combinations
        return result

    def maxDistancesDistrict(self, instance):
        # Radio del distrito = Máxima distancia en un distrito
        distances = []
        pairs = self.pairsBU()
        maxDistance = 0
        for x in pairs:
            # print(x)
            distances.append(instance.distance(x))
            #print("self.instance.distance(x)", instance.distance(x))
        if(len(distances) > 0):
            maxDistance = max(distances)
            #print("Compactness ", maxDistance)

        return maxDistance

    def pairsBU_Ordered(self):
        # Returns the pairs of BU of the district in cardinally order.
        # two basic units assigned to the same district as follows:
        listBU = self.getListBUIndex()
        list_Combination = list()
        for i in range(len(listBU)):
            if(i < (len(listBU)-1)):
                list_Combination += list([listBU[i:i+2]])

        #print("list_Combination", list_Combination)
        return list_Combination

    def sumDistancesDistrict(self, instance):
        distances = []
        sumDitance = 0
        if (len(self.setBasicUnits) > 1):
            pairs = self.pairsBU()  # pairs = self.pairsBU_Ordered()

            for x in pairs:
                #print("xxxx: ", x)
                sumDitance += instance.distance(x)
        return sumDitance

    def updateMaxDistance(self, instance, newBU):
        # get the pares between the new BU and the current BU of the District
        pairs = self.updatePairsBU(newBU)
        if(pairs != False):
            #print("self.pairs: ", pairs)
            # pairs is False when there is less than 2 BU in the districts
            distances = []
            maxDistance = 0
            for x in pairs:
                # print(x)
                distances.append(instance.distance(x))
                # distances.append(5)
                #print("self.instance.distance(x)1", self.distance)

            if(len(distances) > 0):
                maxDistance = max(distances)
                #print("self.instance.distance(x)2", self.distance)

            # if new max distance is greater than current distance then replace distance of district
            if(self.distance < maxDistance):
                self.distance = maxDistance
                if(self.distance == 0):
                    raise Exception("Excepción distance = 0 (Max)")
                #print("maxDistance", maxDistance)
        else:
            self.distance = 0
            listBU = self.getListBUIndex()
            #print("distance=0: ", len(listBU), newBU)

    def updateSumDistance(self, instance, newBU):
        sumDistance = 0
        # get the pares between the new BU and the current BU of the District
        pairs = self.updatePairsBU(newBU)
        if(pairs != False):
            # pairs is False when there is less than 2 BU in the districts
            #distances = []
            for x in pairs:
                # print(x)
                # Get distance of ever pair:
                sumDistance += instance.distance(x)
                #print("self.instance.distance(x)", instance.distance(x))
            # if(len(distances) > 0):
            #     sumDistance = np.sum(distances)

            # Add sumDistance (of new BU) to the current distance of district
            self.distance += sumDistance
            #print("sumDistance", sumDistance)

    def getLastBU(self):
        return self.setBasicUnits[-1]

    def printDistrict(self):
        buIndex = []
        for bu in self.setBasicUnits:
            buIndex.append(bu.id)
        return buIndex

    def all_pairs(self, lst):
        # Get all pair of a list
        return list(itertools.combinations(lst, 2))

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

# Crear una solución (Objeto Solución) a mano usando estas operaciones
# 1. Crear el objeto solución (conjunto de distritos con atributos: compacidad y Desbalance (promedio o máximo))
# 2. Revisar artículo de BENZARTI
# 3. Prueba de Escritorio
# 4. Método para verificar que todo esté bien (todas las unidades básicas asignadas a un distrito, que no haya una unidad básica asignada a más de un distrito, verificar carga de W)


class DistrictInProblem(BasicUnit):
    """
    This class represent the input data of the DistrictInProblem
    M =  number of districts to design.
    N =  number of basic units considered.
    dmaxT = Maximum distance allowed between two basic units that can be assigned to the same district.
    τ =  Admissible percentage deviation of the workload associated to a given district in comparison with the average workload among all districts.


    adik = Adjacency index of the basic units i (i=1…N) and k (k=1…N).

    The next N lines contain, for each basic unit, the following information:

        id la lo np
    where    


    eik = Compatibility index. eik=1 if the basic units i and k are compatible, and 0 otherwise. The basic units i and k can be incompatible for several reasons: a) existence of geographical obstacles between them, b) difficulty or impossibility to travel from one basic unit to another by the means of transportation used by the caregivers (public transportation, private cars, etc.) or c) they do not belong to the same administrative district.
    The next N lines contain the Compatibility index (0,1) of each basic unit with the rest of basic units (NxN):

    dik:  The next N lines contain the Distance between each pair of the basic units (NxN):

    adik: The next N lines contain the adjacency index (0,1) of each basic uniClaset with the rest of basic units (NxN). Where 0 means not adjacence and 1 means adjacent:

    """

    def __init__(self, m, n, ):
        self.eik = []     # Compatibility index matrix
        # Distance between each pair of the basic units. Matrix (NxN)
        self.dik = []
        self.adik = []    # Adjacency matix
        self.m = m
        self.n = n


class CompatibilityIndex:
    """
    A class used that represent a day 

    Attributes:
        row (str): id of row
        col(int): id of col
        index (int): compatibility index for row and col
    """

    def __init__(self, row, col, index):
        self.row = row
        self.col = col
        self.index = index

    def __repr__(self):
        return "Compat row:% s col:% s Index:% s" % (self.row, self.col, self.index)


class Distance:
    """
    A class used that represent a day 

    Attributes:
        row (str): id of row
        col(int): id of col
        dist (int): distance between basic unit of row with basic unit of col
    """

    def __init__(self, row, col, dist):
        self.row = row
        self.col = col
        self.dist = dist

    def __repr__(self):
        return "Dist row:% s col:% s Dist:% s" % (self.row, self.col, self.dist)


class Adjacency:
    """


    Attributes:
        row (str): id of row
        col(int): id of col
        adjac (int): adjac Index
    """

    def __init__(self, row, col, adjac):
        self.row = row
        self.col = col
        self.adjac = adjac

    # def __repr__(self):
    #    return "Adjac row:% s col:% s Index:% s" % (self.row, self.col, self.adjac)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


class Solution:
    districtMatrix = []

    def averageWorkLoad(self):
        quantityOfDistricts = len(self.districtMatrix)
        avWorkLoad = self.WL/quantityOfDistricts  # Get WorkLoad Average
        return avWorkLoad
