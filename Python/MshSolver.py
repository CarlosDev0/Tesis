import random
import gurobipy as gp
import numpy as np
import json
from gurobipy import GRB

from Entities import Solution
from Entities import SynConPVRP
from itertools import combinations
from Entities import District
from Dijkstra import Graph
from GurobiTool import GurobiProc

import math
from itertools import combinations


class MshSolver:
    # Create vector of adjacent BU  (starting on random BU)
    # Create list of Districts
    quantityOfDistricts = 0
    instance = 0
    quantityOfBU = 0

    def __init__(self, instance_, quantityOfDistricts_):
        self.quantityOfDistricts = quantityOfDistricts_
        self.instance = instance_
        quantityOfBU = len(self.instance.basicUnits)

    def createMSHSolution(self, fulfill_WorkBalance, fulfill_Compacity):
        adjacentList = self.createAdjacentList()
        print("Adjacent List: ", adjacentList)
        list_Combination = self.createArcList(adjacentList)

        districtMatix = self.combinationsToDistrict(list_Combination)

        if (fulfill_WorkBalance == True):
            list_Combination = self.workBalanceCriteria(districtMatix)

        if (fulfill_Compacity == True):
            list_Combination = self.compacityCriteria(districtMatix)

        for o in list_Combination:
            print("list_Combination", (o.getListBUIndex()))

        distanceVector = self.calculateDistances(districtMatix)

        # Gurobi:
        gu = GurobiProc()
        gu.gurobiSolver(districtMatix, self.instance,
                        distanceVector, self.quantityOfDistricts)

        #print("districtMatix", len(districtMatix))

        # Dijkstra
        costMatrix = self.omegaMatrix(adjacentList, list_Combination)
        g = Graph(len(adjacentList))
        g.graph = costMatrix
        # g.dijkstra(0)  # Resuelve con Dijkstra

    def createAdjacentList(self):
        # Order the list of BU in adjacent order starting from a random
        buIndexList = []
        while (len(buIndexList) < len(self.instance.basicUnits)):
            randomElement = random.choice(self.instance.basicUnits)

            buIndexList.append(int(randomElement.id))
            i = 0
            inside = True
            randomElement = randomElement.id
            while(inside):
                i += 1

                adjacentList1 = self.instance.getAdjacencybyId(randomElement)
                adjacentList = []
                adjacentList = [int(x) for x in adjacentList1]
                adjacentList = list(set(adjacentList).difference(buIndexList))

                if(len(adjacentList) > 0):
                    randomElement = random.choice(adjacentList)
                    buIndexList.append(int(randomElement))

                    if (len(adjacentList) == 0 and i > len(self.instance.basicUnits)):
                        # No AdjacentList was fully achieved
                        inside = False
                        buIndexList = []
                        print("No AdjacentList was fully achieved")
                    if (len(buIndexList) == len(self.instance.basicUnits)):
                        inside = False
                else:
                    inside = False
                    adjacentList = []
                    buIndexList = []
        buIndexList.append("T")  # validar si se requiere.
        return buIndexList

    def createArcList(self, adjacentList):
        # Build Arcs
        list_Combination = list()
        for i in range(len(adjacentList)):
            for j in range(i+1, len(adjacentList)+1):
                list_Combination += list([adjacentList[i:j]])

        print("list_Combination_length", len(list_Combination))
        #print("list_Combination", (list_Combination))

        return list_Combination

    def combinationsToDistrict(self, list_Combination_):
        districtMatrix = []
        for dis in list_Combination_:
            district = District()  # Empty District
            for item in dis:
                for x in self.instance.basicUnits:
                    if (x.id == item):
                        district.addBasicUnits(x)
                        district.updateWorkLoad("Add", x)
                        # district.setWorkLoad()  # Update workload of District (wl)
            districtMatrix.append(district)

        print("Districts: ", len(districtMatrix))
        return districtMatrix

    def workBalanceCriteria(self, districtMatix):
        # Calculate workload and remove ones with excess workload
        # districtMatix is a list of Districts

        list_Combination = districtMatix

        if(self.quantityOfDistricts > 0):
            avWorkLoad = self.instance.WL/self.quantityOfDistricts  # AverageWorkLoad
            for dis in districtMatix:
                #print("Interm1: ", dis.setBasicUnits)
                if(len(dis.setBasicUnits) > 1):
                    if(dis.wl > avWorkLoad):
                        list_Combination.remove(dis)
                else:
                    list_Combination.remove(dis)
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
                    if(dis.maxDistancesDistrict(self.instance) > maxDistance):
                        list_Combination.remove(dis)
                else:
                    list_Combination.remove(dis)
            print("Final2_With Compacity Criteria: ", len(list_Combination))
        return list_Combination

    def calculateDistances(self, districtMatix):
        distanceVector = []
        for dis in districtMatix:
            distanceVector.append(dis.sumDistancesDistrict(self.instance))
            # print("District Distance: ", dis.distance)
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

    m = gp.Model()
    capitals = []

    def gurobi(self):
        # https://colab.research.google.com/github/Gurobi/modeling-examples/blob/master/traveling_salesman/tsp_gcl.ipynb#scrollTo=zJS2HrRlU35i
        # m = gp.Model()
        # x = m.addVar()
        # m.AddConstr(x >= 42)

        # Read capital names and coordinates from json file
        try:
            capitals_json = json.load(open('capitals.json'))
        except:
            import urllib.request
            url = 'https://raw.githubusercontent.com/Gurobi/modeling-examples/master/traveling_salesman/capitals.json'
            data = urllib.request.urlopen(url).read()
            capitals_json = json.loads(data)

        coordinates = {}
        for state in capitals_json:
            if state not in ['AK', 'HI']:
                capital = capitals_json[state]['capital']
                self.capitals.append(capital)
                coordinates[capital] = (
                    float(capitals_json[state]['lat']), float(capitals_json[state]['long']))

        # Compute pairwise distance matrix
        import math
        from itertools import combinations

        # Compute pairwise distance matrix

        def distance(city1, city2):
            c1 = coordinates[city1]
            c2 = coordinates[city2]
            diff = (c1[0]-c2[0], c1[1]-c2[1])
            return math.sqrt(diff[0]*diff[0]+diff[1]*diff[1])

        dist = {(c1, c2): distance(c1, c2)
                for c1, c2 in combinations(self.capitals, 2)}

        # tested with Python 3.7 & Gurobi 9.0.0

        # Variables: is city 'i' adjacent to city 'j' on the tour?
        vars = self.m.addVars(dist.keys(), obj=dist,
                              vtype=GRB.BINARY, name='x')

        # Symmetric direction: Copy the object
        for i, j in vars.keys():
            vars[j, i] = vars[i, j]  # edge in opposite direction

        # Constraints: two edges incident to each city
        cons = self.m.addConstrs(vars.sum(c, '*') == 2 for c in self.capitals)

        # Callback - use lazy constraints to eliminate sub-tours
        self.m._vars = vars
        self.m.Params.lazyConstraints = 1
        # self.m.optimize(self.subtourelim)  #GENERA EXCEPCIÓN

    def subtourelim(self, model, where):
        if where == GRB.Callback.MIPSOL:
            # make a list of edges selected in the solution
            vals = model.cbGetSolution(model._vars)
            selected = gp.tuplelist((i, j) for i, j in model._vars.keys()
                                    if vals[i, j] > 0.5)
            # find the shortest cycle in the selected edge list
            tour = self.subtour(selected)
            if len(tour) < len(self.capitals):
                # add subtour elimination constr. for every pair of cities in subtour
                model.cbLazy(gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2))
                             <= len(tour)-1)

    # Given a tuplelist of edges, find the shortest subtour

    def subtour(self, edges):
        unvisited = self.capitals[:]
        cycle = self.capitals[:]  # Dummy - guaranteed to be replaced
        while unvisited:  # true if list is non-empty
            thiscycle = []
            neighbors = unvisited
            while neighbors:
                current = neighbors[0]
                thiscycle.append(current)
                unvisited.remove(current)
                neighbors = [j for i, j in edges.select(current, '*')
                             if j in unvisited]
            if len(thiscycle) <= len(cycle):
                cycle = thiscycle  # New shortest subtour
        return cycle

    def gurobiExample(self):
        #x = self.m.addVar(ub=1.0)
        #y = self.m.addVar(ub=1.0)
        #z = self.m.addVar(ub=1.0)
        Q = np.diag([1, 2, 3])
        A = np.array([[1, 2, 3], [1, 1, 0]])
        b = np.array([4, 1])

        x = self.m.addMVar(3, ub=1.0)  # Matricial 3 variables
        # self.m.addMVar((4,2), vtype=GRB.BINARY)  #Add a 4*2 matrix binary variable

        self.m.update()

        #self.m.setObjective(x*x + 2*y*y + 3*z*z)
        self.m.setObjective(x @ Q @ x)  # matricial

        #self.m.addConstr(x+2*y+3*z >= 4)
        #self.m.addConstr(x + y >= 1)

        self.m.addConstr(A@x >= b)

        x.UB  # Query Gurobi attibute, gives ndarray
        x.obj  # Query array

        self.m.optimize()  # solve default optimization send is 'minimize'
        x.X  # Get solution values as ndarray
