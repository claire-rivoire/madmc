
from tkinter import *
#import random
import numpy as np
#import math
#from threading import Timer

class CarData :
    
    def __init__(self): # TODO : tout est en minimisation, il faudra convertir les données à maximiser pour la minimisation
        self.points = np.array([["voiture1", 1, 7],
                                ["voiture2", 3, 7],
                                ["voiture3", 5, 6],
                                ["voiture4", 6, 4],
                                ["voiture5", 7, 2],
                                ["voiture6", 8, 2]])
        [self.nb_cars, self.nb_criteria] = self.points.shape
        self.nb_criteria = self.nb_criteria - 1


    def getParetoFront(self): #TODO
        return self.points
    
    def getIdealNadir(self):
        nadir = []
        ideal = []
        nadir.append("nadir")
        ideal.append("ideal")
        paretoFront = self.getParetoFront()
        for i in range(self.nb_criteria):
            nadir.append(max(p[i+1] for p in paretoFront))
            ideal.append(min(p[i+1] for p in paretoFront))
        return np.array([ideal, nadir])


    def reduceData(self, criterion, value):
        result = np.empty((0,3))
        if ((criterion >= 1) & (criterion <= self.nb_criteria)) :            
            for i in range(self.nb_cars):
                if (int(self.points[i,criterion]) <= value):
                    result = np.concatenate((result, [self.points[i,:]]), axis=0)
            self.points = result
            [self.nb_cars, self.nb_criteria] = self.points.shape
            self.nb_criteria = self.nb_criteria - 1
            return True
        else:
            return False # erreur
        

class Tchebycheff :
 
    def __init__(self, inputData):
        self.data = inputData
        self.epsilon = 0.01
        
    def updateData(self, inputData):
        self.data = inputData
        
    def getSolution(self):
        [ideal, nadir] = self.data.getIdealNadir()
        result = self.data.points[0,:]
        result_norm = self.getTchebycheffNorm(self.data.points[0,:], ideal, self.epsilon)
        for i in range(1,self.data.nb_cars):
            norm = self.getTchebycheffNorm(self.data.points[i,:], ideal, self.epsilon)
            if (norm < result_norm):
                result = self.data.points[i,:]
                result_norm = norm
        return result
    

    def getTchebycheffNorm(self, point, ideal, epsilon):
        temp =[]
        for i in range(self.data.nb_criteria):
            temp.append(abs(int(point[i+1]) - int(ideal[i+1])))
        return max(temp) + epsilon * sum(temp)

    
def main():
    #fenetre = Tk()
    #fenetre.title('MADMC - Mini projet')
    #fenetre.mainloop()

    car_data = CarData()
    selector = Tchebycheff(car_data)
    print("meilleur resultat trouvé:")
    print(selector.getSolution())
    print("amélioration sur le premier critère:")
    car_data.reduceData(1,5)
    selector.updateData(car_data)
    print(selector.getSolution())
   


main()



