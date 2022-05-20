import gurobipy as gp
import numpy as np
from gurobipy import GRB


class GurobiProc:

    m = gp.Model()
    capitals = []

    def gurobiSolver(self, districtMatix, instance, dv, quantityOfDistricts):

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

        print("A", A)
        Q = np.diag([1, 2, 3])
        b = np.ones(len(instance.basicUnits), dtype=int)
        c = np.ones(len(districtMatix), dtype=int)

        print("districtMatix", len(districtMatix))
        print("dv", len(dv))
        print("b", np.array(b))
        print("A", (A.shape))

        x = self.m.addMVar(len(districtMatix), ub=1.0,
                           vtype=GRB.INTEGER)  # Matricial variables, Integer

        self.m.update()

        self.m.setObjective(x @ np.array(dv))  # matricial

        # Each BU must be assigned to only one district
        self.m.addConstr(A@x == b)
        # Each BU must be assigned to only one district
        #self.m.addConstr(A@x <= b)

        # Quantity of District must math the required
        self.m.addConstr(c@x == quantityOfDistricts)
        #self.m.addConstr(c@x <= quantityOfDistricts)

        x.UB  # Query Gurobi attibute, gives ndarray
        x.obj  # Query array

        self.m.optimize()  # solve default optimization send is 'minimize'
        print("SOLUCIÓN: ", x.X)  # Get solution values as ndarray
        #print(districtMatix[x.X == 1])
        B = x.X.astype(int)
        A = districtMatix
        r = [a for a, b in zip(A, B) if b == 1]
        for o in r:
            print(o.getListBUIndex())
        #print(districtMatix[sol == 1])
