import numpy as np
import pickle
import random
import time
from copy import deepcopy
###Ant Colony Optimization Algorithm

#User Defined Variables
Q = 10
rho = 0.2
alpha = 1
beta = 1

#General functions
numeratorFun = lambda c, n: (c ** alpha) + (n ** beta)

def ACO(filter=None):
    tic = time.time()
    #import pokemon DB
    with open("Pok.pkl", "rb") as f:
        pokPreFilter = pickle.load(f)

    #Filter Pokemon (now not filtering)
    poks = pokPreFilter


    #Create Decision Space of Pokemon
    DS_Pok = np.arange(poks.__len__())

    #Create Decision Space of Attacks
    DS_Att = []
    for pok in poks:
        size = pok.knowableMoves.__len__()
        DS_Att.append(np.arange(size))

    #Create Pheromone of Attacks
    Ph_Att = []
    for pok in poks:
        size = pok.knowableMoves.__len__()
        if(size == 0):
            size = 1
        Ph_Att.append(np.zeros(size))

    #Create Heuristic Value of Pokemon
    H_Poks = np.zeros(poks.__len__())
    i = 0
    for i in range(0, H_Poks.__len__()):
        H_Poks[i] = heuristicPokFun(poks, i)

    #Create Heuristic Value of Attack
    H_Att = []
    for pok in poks:
        size = pok.knowableMoves.__len__()
        if(size == 0):
            size = 1
        H_Att.append(np.zeros(size))

    #Create Population
    pop_size = 100
    Pop = np.empty([pop_size,6,5])

    #Assign Population
    for ant in Pop:
        for pokemon in ant:
            selectedPok = False
            id = 0
            tempSum = 0
            randPok = random.randrange(0,100001,1)/100001
            #Get Pokemon such that ph_(n)< rand <ph(n+1)
            while(not selectedPok):
                tempPh = Ph_Pok[id]
                if(randPok>tempSum+tempPh):
                    id = id + 1
                    tempSum = tempSum + tempPh
                elif(randPok<tempSum+tempPh):
                    selectedPok = True

            pokemon[0] = id

            #Get Knowable Moves
            PhAtt_Temp = Ph_Att[id]
            for i in range(1,5):
                if((PhAtt_Temp.size - (i))>0):
                    randAtt = PhAtt_Temp.sum()*random.randrange(0,100001,1)/100001
                    attId = 0
                    tempSum = 0
                    selectedAttack = False
                    while(not selectedAttack):
                        tempPh = PhAtt_Temp[attId]
                        if(randAtt>tempSum+tempPh):
                            attId = attId + 1
                            tempSum = tempSum + tempPh
                        elif(randAtt<=tempSum+tempPh):
                            pokemon[i] = poks[id].knowableMoves[attId].id
                            PhAtt_Temp[attId] = 0
                            selectedAttack = True
                else:
                    pokemon[i] = -1

    toc = time.time()
    print(toc-tic)
    print("Stop")


def fitness(ant):
    fitnessValue = 1

    return fitnessValue

def calculatePheromone(ph_vect):
    pass

def heuristicPokFun(poks, pokIndex):
    #TODO Scale the heuristic value after getting Pheromone Values
    heuristicValue = poks[pokIndex].overallStats()/500
    return heuristicValue

if __name__ == "__main__":
    ACO()