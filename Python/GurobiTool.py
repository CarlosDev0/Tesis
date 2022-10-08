import gurobipy as gp
import numpy as np
from gurobipy import GRB


class GurobiProc:

    m = gp.Model()
    capitals = []

    def gurobiSolver(self, districtMatix, instance, dv, quantityOfDistricts):
        self.m.Params.LogToConsole = 0  # To disable print solution into console
        self.m.Params.outputflag = 1
        self.m.Params.CSClientLog = 3
        A = np.zeros((len(instance.basicUnits), len(dv)))
        di = 0
        bi = 0
        for d in districtMatix:
            buList = d.getListBUIndex()
            #print("buList", buList)
            bi = 0
            for b in instance.basicUnits:
                if(b.id in buList):
                    A[bi, di] = 1
                bi += 1
            di += 1

        #print("A", A)
        Q = np.diag([1, 2, 3])
        b = np.ones(len(instance.basicUnits), dtype=int)
        c = np.ones(len(districtMatix), dtype=int)

        #print("districtMatix", len(districtMatix))
        #print("dv", len(dv))
        #print("b", np.array(b))
        #print("A", (A.shape))

        x = self.m.addMVar(len(districtMatix), ub=1.0,
                           vtype=GRB.BINARY)  # Matricial variables, BINARY

        self.m.update()

        self.m.setObjective(x @ np.array(dv))  # matricial

        # Each BU must be assigned to only one district
        self.m.addConstr(A@x == b)
        # Each BU must be assigned to only one district
        #self.m.addConstr(A@x <= b)

        # self.m.setParam("OutputFlag", 1)  # Set the maximum Output from Gurobi

        # Quantity of District must math the required
        self.m.addConstr(c@x == quantityOfDistricts)
        #self.m.addConstr(c@x <= quantityOfDistricts)

        x.UB  # Query Gurobi attibute, gives ndarray
        x.obj  # Query array

        self.m.optimize()  # solve default optimization send is 'minimize'
        # print("SOLUCIÓN: ", x.X)  # Get solution values as ndarray
        #print(districtMatix[x.X == 1])
        solution = []
        if self.m.status != GRB.OPTIMAL:
            return solution
        B = x.X.astype(int)
        A = districtMatix
        r = [a for a, b in zip(A, B) if b == 1]

        librarySolution = []
        for o in r:
            librarySolution.append(o)
            # print(o.getListBUIndex())
        #print(districtMatix[sol == 1])
        solution.append(librarySolution)
        print("x.obj.getValue()", round(self.m.objVal, 2))
        solution.append(round(self.m.objVal, 2))
        return solution
