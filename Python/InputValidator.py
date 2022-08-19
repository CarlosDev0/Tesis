"""
Created on Fri June 12 09:40:22 2021

@author: Carlos Alberto Sánchez

"""

from Entities import SynConPVRP


class InputValidator:
    instance = 0

    def __init__(self, instance_):
        self.instance = instance_

    def checkInput(self):
        # num of Districts Validation:
        if (self.instance.numDist <= 0):
            print(
                "There is a problem, the input data must have a Number of Districts greater than 0.")
            raise Exception(
                "There is a problem, the input data must have a Number of Districts greater than 0.")
        if (self.instance.numDist >= self.instance.numBasicUnits):
            print(
                "There is a problem, the input data must have a Number of Districts lower than the quantity of BU.")
            raise Exception(
                "There is a problem, the input data must have a Number of Districts lower than the quantity of BU.")
        if (self.instance.numBasicUnits <= 0):
            print(
                "There is a problem, the input data must have a Number of Basic Units greater than 0.")
            raise Exception(
                "There is a problem, the input data must have a Number of Basic Units greater than 0.")
        if (self.instance.maxDistance <= 0):
            print(
                "There is a problem, the input data must have a maxDistance parameter greater than 0.")
            raise Exception(
                "There is a problem, the input data must have a maxDistance parameter greater than 0.")
        if (self.instance.DeviationPermited <= 0):
            print(
                "There is a problem, the input data must have a DeviationPermited parameter greater than 0.")
            raise Exception(
                "There is a problem, the input data must have a DeviationPermited parameter greater than 0.")
        if (int(len(self.instance.basicUnits)) != int(self.instance.numBasicUnits)):
            print(
                "There is a problem, the input data must have a quantity of Basic Units %s and the quantity found was %s" % (self.instance.numBasicUnits, len(self.instance.basicUnits)))
            raise Exception(
                "There is a problem, the input data don't have the quantity of Basic Units required.")
        if (len(self.instance.compatibility) != self.instance.numBasicUnits*self.instance.numBasicUnits):
            print(
                "There is a problem, the input data must have a quantity of compatibility %s and the quantity found was %s" % (self.instance.numBasicUnits, len(self.instance.compatibility)))
            raise Exception(
                "There is a problem, the input data don't have the quantity of compatibility required.")
        if (len(self.instance.distances) != self.instance.numBasicUnits):
            print(
                "There is a problem, the input data must have a quantity of distances %s and the quantity found was %s" % (self.instance.numBasicUnits, len(self.instance.distances)))
            raise Exception(
                "There is a problem, the input data don't have the quantity of distances required.")
