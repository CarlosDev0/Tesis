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
                a[2]), int(a[3]))  # id, la, lo, wl
            self.basicUnits.append(ps)
            self.WL += int(a[3])
            # district.addBasicUnits(ps)
        # Compatibility Index section
        for i in range(self.numBasicUnits):
            a = f_entrada.readline()
            a = re.split("\t", a)
            for j in range(self.numBasicUnits):
                t = CompatibilityIndex(i, j, a[j])
                self.compatibility.append(t)

        print(self.compatibility)
        # Distance section
        for i in range(self.numBasicUnits):
            a = f_entrada.readline()
            a = re.split("\t", a)
            for j in range(self.numBasicUnits):
                t = Distance(i, j, a[j])
                self.distances.append(t)

        print(self.distances)
        # adjacency index section
        for i in range(self.numBasicUnits):
            a = f_entrada.readline()
            a = re.split("\t", a)
            for j in range(self.numBasicUnits):
                t = Adjacency(i, j, a[j])
                self.adjacencies.append(t)

    def distance(self, pair):
        # Distance: distance between a par of BU of the district
        row_ = pair[0]
        col_ = pair[1]
        result = 0
        for a in self.distances:
            if (np.logical_and(a.row == row_, a.col == col_)):
                result = float(a.dist)
        return result

    def findAdjacent(self, basicUnit):
        return ""

    def getAdjacencybyId(self, row_):
        # Returns the list of id adjacent to ONE BU received
        results = np.array([])
        for a in self.adjacencies:
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

    #     for i in range(self.numDays):
    #         a = f_entrada.readline()
    #         a = re.split("\t", a)
    #         aux = ""
    #         # the name of the days are not of the same lenght so we have to join the name into a string before creating the day
    #         aux = aux.join(a[0])
    #         d = Day(aux, i, int(a[1]))
    #         # TODO: the name of the days are not of the same lenght!!!
    #         self.days.append(d)
    #     # Scenario section
    #     for i in range(self.numScen):
    #         a = f_entrada.readline()
    #         a = re.split("\t", a)
    #         name = a[0]
    #         num = int(a[1])
    #         s = Scenario(name, num)  # Customer section
    #         self.scenarios.append(s)
    #   # Depot section
    #     coords = []
    #     a = f_entrada.readline()
    #     a = re.split("\t", a)
    #     d = Depot(float(a[1]), float(a[2]))
    #     self.depot = d
    #     coordsAux = []
    #     coordsAux.append(float(a[1]))
    #     coordsAux.append(float(a[2]))
    #     # print(tuple(coordsAux))
    #     coords.append(tuple(coordsAux))
    #     # Customer section
    #     for i in range(self.numCus):
    #         a = f_entrada.readline()
    #         a = re.split("\t", a)
    #         name = a[0]
    #         x = float(a[1])
    #         y = float(a[2])
    #         dem = int(a[3])
    #         stPres = int(a[4])
    #         stTruck = int(a[5])
    #         freq = int(a[6])
    #         numPaterns = int(a[7])
    #         auxL = []
    #         cu = Customer(name, i, x, y, dem, stPres, stTruck, freq)
    #         for j in range(numPaterns):
    #             auxL.append(int(a[7+j+1]))
    #         cu.visitpaterns = auxL
    #         self.customers.append(cu)
    #         # Coordinates matrix
    #         coordsAux = []
    #         coordsAux.append(float(a[1]))
    #         coordsAux.append(float(a[2]))
    #         coords.append(tuple(coordsAux))
    #     # Distance calculation
    #     #self.distances=np.empty((self.numCus+1, self.numCus+1))
    #     # print(coords)
    #     self.distances = distance.cdist(coords, coords, 'euclidean')


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

    def __init__(self):
        self.setBasicUnits = []
        self.quantity_BU = 0
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
        #print("Quantity of BU in district: ", len(self.setBasicUnits))

    def workLoadBalance(self):
        wl = int
        wl = 0
        for bu in self.setBasicUnits:
            wl += int(bu.wl)
        return wl

    def pairsBU(self):
        # compactness measure i.e. the maximum distance between
        # two basic units assigned to the same district as follows:
        listBU = self.getListBUIndex()
        #print("listBU", listBU)
        pairs = self.all_pairs(listBU)
        return pairs

    def noAdjacency(self):
        print("")

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


# class Customer:
#     """
#    A class used that represent a customer

#     Attributes:
#         id (str): Name of the customer
#         pos (int): position in the set of customers
#         x (float): x coordinate of the customer/also can used as the latitude
#         y (float): y coordinade of the cstomer /also can used as the longitude
#         demand (int): demand to be served during the week / drop size of the customer
#         stPres (int): service time of the preseller
#         stTruck(int): service time of the truck
#         freq (int): number of times that a customer need to be visited
#         visitPaterns(list of int): feasible visit paterns for the customer

#     """

#     def __init__(self, id, ord, x=0, y=0, demand=0, stp=0, stt=0, freq=1):
#         self.id = id
#         self.pos = ord
#         self.x = x
#         self.y = y
#         self.demand = demand
#         self.stPres = stp
#         self.stTruck = stt
#         self.freq = freq
#         self.visitpaterns = []


# class Depot:
#     """
#     Attributes:
#     x (float): x coordinate of the depot/also can used as the latitude
#     y (float): y coordinade of the depot/also can used as the longitude
#     """

#     def __init__(self, x=0, y=0):
#         self.x = x
#         self.y = y


# class Resource:
#     """
#     A super class to extend with the reources
#     name (str): name of the preseller
#     pos(int): number of the preseller used for indexing
#     cap (int): capacity of the preseller
#     """

#     def __init__(self, name, pos, cap, cf, cv):
#         self.name = name
#         self.pos = pos
#         self.cap = cap
#         self.cf = cf
#         self.cv = cv


# class Preseller(Resource):
#     """
#     A class used that represent a preseller

#     Attributes:
#         name (str): name of the preseller
#         pos(int): number of the preseller used for indexing
#         cap (int): capacity of the preseller
#         cfs (float): fixed cost of the preseller if used in a given period
#         cs(float):per distance cost
#     """

#     def __init__(self, name, pos, cap, cfs, cs=1):
#         self.name = name
#         self.pos = pos
#         self.cap = cap
#         self.cf = cfs
#         self.cv = cs


# class Truck(Resource):
#     """
#     A class used that represent a depot

#     Attributes:
#         name (str): name of the preseller
#         pos(int): number of the preseller used for indexing
#         cap (int): capacity of the preseller
#         cfs (float): fixed cost of the preseller if used in a given period
#         cs(float):per nit distance cost
#     """

#     def __init__(self, name, pos, cap, cft, ct=1):
#         self.name = name
#         self.pos = pos
#         self.cap = cap
#         self.cf = cft
#         self.cv = ct


# class Day:
#     """
#     A class used that represent a day

#     Attributes:
#         name (str): name of the day
#         pos(int): number of the day in the planning horizon
#         dur (int): maximm dration of a route this day
#     """

#     def __init__(self, name, pos, dur):
#         self.name = name
#         self.pos = pos
#         self.dur = dur


# class Scenario:
#     """
#     A class to store the information of  a given scenario: visiting pattern for the days of the planning horizon
#     Attributes:
#         name (str): the name of the scenario
#         num (int): an integer number that describes the scenario in binary code
#         visit (binary): a binary number representing  the binary number that indicates the days that the scenario visits a customer

#     """

#     def __init__(self, name, num):
#         self.name = name
#         self.num = num
#         self.visit = bin(num)


# class myRoute:
#     """
#     A class used to represent a route

#     Attributes:
#         resource (A truck or a preseller): that performs the route
#         day (Day): the day in which the route is performed
#         name (str): name of the route  (mnemonic: created by concatenating the name of the reource that performs the route and the they it is performed )
#         depot (depot): the depot from which the route departs and its the seed of the seqnece
#         sequence (list of customers and the depot): a list of nodes in the sequence they are visited by the resource
#         load (float): the load of the route (sum of the demand of the customers added to the route)
#         distance (float): the distance travelled by the resuorce  in the sequence
#         fixCost(float): cost of using te resource
#         varCost (float): cost of travelling the route
#         cost (float): the cost of the route calculated with the fixed resource cost and the distance cost


#     Methods: TODO
#         Constructor
#         INSERT A CUSTOMER IN THE FIRST OR LAST POSITION  OF THE ROUTE
#         INSERT A CUSTOMER IN A GIVEN POSITION  OF THE ROUTE
#         INSERT A CUSTOMER IN A RANDOM POSITION  OF THE ROUTE
#         REMOVE A SPECIFIC CUSTOMER
#         REMOVE A CUSTOMER IN A GIVEN POSITION
#         REMOVE A RAMDOM CUSTOMER

#     """
#     # Route constructor  with a problem resource and day

#     def __init__(self, problem: SynConPVRP, res: Resource, day: Day):
#         self.resource = res
#         self.day = day
#         # create the name of the route
#         self.name = res.name + "-"+day.name
#         # set the type of the route
#         self.tp = ''
#         if(isinstance(res, Truck)):
#             self.tp = 'DelivRoute'
#         else:
#             self.tp = 'PreselRoute'

#         # Initialize what can be assigned: depot, load, distance, fixed cost  and cost
#         self.depot = problem.depot
#         self.load = 0
#         self.distance = 0
#         self.fixCost = res.cf
#         self.varCost = 0
#         self.cost = res.cf
#         # And finally the sueqence
#         self.sequence = []
#         self.sequence.append(problem.depot)
#         self.sequence.append(problem.depot)

#     # Inserting a customer in the first  position of the route
#     def insertCusIni(self, problem: SynConPVRP, cus: Customer):
#         # Insert the customer in the sequence
#         self.sequence.insert(1, cus)
#         # Update the variables
#         # Demand accounts only for the part of the customer demand of a given day (drop size)
#         self.load += cus.demand/cus.freq
#         # distance update takes into account the customer position in the array of distances
#         self.distance += problem.distances[0][cus.pos+1]
#         self.varCost += self.distance*self.resource.cv
#         self.cost += self.distance*self.resource.cv
