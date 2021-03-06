import glob_var
import numpy as np
def moveExactCounter(PokemonsList):
    """
    Count the number of pokemon that have X number of knowable attacks (until 36)
    :param PokemonsList: List of Pokemon to run through
    :return: Array containing the amount of pokemons that can learn X amount of moves
    """
    numberofmoves = []
    i_s = []
    i = 0
    while(i < 36):
        quantPok = 0
        for pok in PokemonsList:
            quantMoves = pok.knowableMoves.__len__()
            if(quantMoves == i):
                quantPok = quantPok + 1
        numberofmoves.append(quantPok)
        i_s.append(i)
        i = i + 1
    print(i_s)
    return numberofmoves

def moveTotalCounter(PokemonsList):
    """
    Count the number of pokemon that have at least X number of knowable attacks (until 36)
    :param PokemonsList: List of Pokemon to run through
    :return: Array containing the amount of pokemon that can learn at least X amount of moves
    """
    numberofmoves = []
    i_s = []
    tempmove = None
    i = 0
    while(tempmove != 1):
        quantPok = 0
        for pok in PokemonsList:
            quantMoves = pok.knowableMoves.__len__()
            if(quantMoves >= i):
                quantPok = quantPok + 1
        numberofmoves.append(quantPok)
        i_s.append(i)
        i = i + 1
        tempmove = quantPok
    print(i_s)
    return numberofmoves

def currentPower(pok, learnedMoves):
    """
    Calculates the current power of the pokemon based on Stats, Attacks, and Type
    :return: Returns total power of the learned moves
    """
    currentPower = 0
    for learnedMove in learnedMoves:
        moveType = learnedMove.type
        movePower = learnedMove.power
        moveDamageClass = learnedMove.damageClass
        moveAccuracy = learnedMove.accuracy
        stab = 1.5 if (moveType == pok.type1 or moveType == pok.type2) else 1
        split = pok.att if (moveDamageClass == "physical") else pok.spatt
        expectedPower = (stab * movePower) * split * moveAccuracy
        currentPower += expectedPower
    return currentPower

def getLearnedMoves(pokPreFilter, pok, ids):
    #TODO Handle -1 in ids because it has no attack (Like Ditto)
    temp = []
    for id in ids:
        if id != -1:
            temp.append(pokPreFilter[pok[0]].knowableMoves[id])
    return temp

def getWeakness(pok):
    typeChart = glob_var.typeChart
    typeOrder = glob_var.typeOrder
    weakness = typeChart[:,typeOrder.index(pok.type1)]
    try:
        weakness2 = typeChart[:,typeOrder.index(pok.type2)]
        weakness = np.multiply(weakness, weakness2)
    except:
        pass

    return weakness

def hoyerSparseness(x):
    k = x.__len__()
    value = (np.sqrt(k) - ((np.linalg.norm(x,1))/(np.linalg.norm(x,2))))/(np.sqrt(k)-1)
    return value

def getTeamNames(team):
    for pok in team:
        print(pokPreFilter[pok[0]].name)

def colonyCooperation(candSets, objFuns):
    totalCandSet = []
    candSetObjs=[]
    for i in candSets:
        totalCandSet += i

    for j in objFuns:
        candSetObjsTemp = np.array(list(map(j, totalCandSet)))
        candSetObjs += [candSetObjsTemp/(candSetObjsTemp.max())]

    dominanceVector = np.ones(totalCandSet.__len__())

    for x in candSetObjs: dominanceVector = np.multiply(dominanceVector, x)

    dominatedCandSet = [x for _, x in sorted(zip(dominanceVector, totalCandSet), key=lambda pair: pair[0], reverse= True)][0:int(dominanceVector.__len__()/candSets.__len__())]

    return dominatedCandSet