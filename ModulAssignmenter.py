from random import shuffle
from random import randrange
import numpy as np
import random
import sys
import matplotlib.pyplot as plt
import os

def give_testScoreMatrix():
    #creat scorematrix for testing purpose
    Listmatrix = []
    for student in range(40):
        wahlMoeglichkeit = []
        for n in range(1,16):
            wahlMoeglichkeit.append(n)
            shuffle(wahlMoeglichkeit)
        Listmatrix.append(wahlMoeglichkeit)

    return np.asarray(np.matrix(Listmatrix))

def give_testSizeConstrains():
    list = []
    for n in range(15):
        list.append(randrange(7,15))
    return np.asarray(list)

def test_sizeConst(zuordnung, constrains):
    sum = zuordnung.sum(axis=0)
    delta = constrains-sum
    if  len(np.where(delta < 0)[0]) > 0:
        return False
    else:
        return True

def give_choosingList():
    liste = []
    for n in range(50):
        liste.append(1)
    for n in range(10):
        liste.append(2)
    for n in range(10):
        liste.append(4)
    for n in range(10):
        liste.append(8)
    for n in range(10):
        liste.append(16)
    for n in range(10):
        liste.append(32)
    return liste

def give_initZuordungMatrix(scoreMatrix):
    while True:
        ZuordungMatrix = np.zeros(np.shape(scoreMatrix), dtype=np.int)
        for studNr in range(np.shape(scoreMatrix)[0]):
            initValues = []
            for n in range(3):
                while len(initValues) < 3:
                    value = randrange(0, np.shape(scoreMatrix)[1])
                    if value not in initValues:
                        initValues.append(value)
            for value in initValues:
                ZuordungMatrix[studNr][value] = 1

        if test_sizeConst(ZuordungMatrix, constArray) == True:
            break


    print "Initial random assignment is created!"
    return np.asarray(ZuordungMatrix)

def give_score(zuordungMatrix,scoreMatrix,fac):
    produktMatrix = zuordungMatrix*scoreMatrix
    sum  = np.sum(produktMatrix)
    list = []
    for stud in range(np.shape(scoreMatrix)[0]):
        list.append(np.sum(produktMatrix[stud]))
    std = np.std(list)

    return [sum,std]

def give_innerPermuation(zuordungMatrix,constArray):
    #module innherhab eines studenten werden getauscht
    newZuordungMatrix = np.copy(zuordungMatrix)


    while True:
        stud = randrange(np.shape(newZuordungMatrix)[0])
        mod1 = randrange(np.shape(newZuordungMatrix)[1])
        mod2 = randrange(np.shape(newZuordungMatrix)[1])
        value1 = newZuordungMatrix[stud][mod1]
        value2 = newZuordungMatrix[stud][mod2]
        newZuordungMatrix[stud][mod1] = value2
        newZuordungMatrix[stud][mod2] = value1

        if test_sizeConst(newZuordungMatrix,constArray) == True:
            return [newZuordungMatrix,False]
            break

def give_outerPermutation(oldZuordungMatrix):
    #module zwischen studenten werden getauscht
    innerZuordungMatrix = np.copy(oldZuordungMatrix)
    einserCoord = np.where(innerZuordungMatrix==1)
    tulpIndexA = randrange(np.shape(einserCoord)[1])
    studA = einserCoord[0][tulpIndexA]
    modulA = einserCoord[1][tulpIndexA]

    while True:
        tulpIndexB = randrange(np.shape(einserCoord)[1])
        studB = einserCoord[0][tulpIndexB]
        modulB = einserCoord[1][tulpIndexB]
        #NullerCheck
        if innerZuordungMatrix[studB][modulA] == 0 and innerZuordungMatrix[studA][modulB] ==0:
            #return [innerZuordungMatrix,[[studA,modulA],[studB,modulB]]]
            break



    innerZuordungMatrix[studA][modulA] = 0
    innerZuordungMatrix[studB][modulB] = 0
    innerZuordungMatrix[studA][modulB] = 1
    innerZuordungMatrix[studB][modulA] = 1
    return [innerZuordungMatrix, [[studA, modulA], [studB, modulB]]]
    #return [innerZuordungMatrix,studA,studB,modulA,modulB]


    """
    print oldZuordungMatrix[studA][modulA], "<--- studA modul A"
    print oldZuordungMatrix[studA][modulB], "<--- studA modul B"
    print oldZuordungMatrix[studB][modulA], "<--- studB modul A"
    print oldZuordungMatrix[studB][modulB], "<--- studB modul B"
    print ""
    print innerZuordungMatrix[studA][modulA], "<--- studA modul A"
    print innerZuordungMatrix[studA][modulB], "<--- studA modul B"
    print innerZuordungMatrix[studB][modulA], "<--- studB modul A"
    print innerZuordungMatrix[studB][modulB], "<--- studB modul B"
    print np.array_equal(innerZuordungMatrix, zuordungMatrix)
    """

def rand_permutation(innerZuordungMatrix,constArray):
    if random.randint(1, 2) == 1:
        newZuordungMatrixList = give_innerPermuation(innerZuordungMatrix,constArray)
        studModAuswahl = newZuordungMatrixList[1]
        newZuordungMatrix = newZuordungMatrixList[0]
        if 120 != np.sum(np.sum(newZuordungMatrix, axis=1)):
            print "im innerpermutations ding is was schief gelaufen"
            print np.sum(newZuordungMatrix, axis=1)
            sys.exit()

    else:
        newZuordungMatrixList = give_outerPermutation(innerZuordungMatrix)
        studModAuswahl = newZuordungMatrixList[1]
        newZuordungMatrix = newZuordungMatrixList[0]
        if 120 != np.sum(np.sum(newZuordungMatrix, axis=1)):
            print "im outer permutations ding is was schief gelaufen"
            print np.sum(newZuordungMatrix, axis=1)
            sys.exit()

    if studModAuswahl != False:
        newIsBetterDueToMark = give_ModulPrio(studModAuswahl)
    else:
        newIsBetterDueToMark = True

    return [newZuordungMatrix,newIsBetterDueToMark]

def give_ModulPrio(auswahl):
    studA = auswahl[0][0]
    studB = auswahl[1][0]
    modulA= auswahl[0][1]
    modulB = auswahl[1][1]
    prioStudAModulA = scoreMatrix[studA,modulA]
    prioStudAModulB = scoreMatrix[studA, modulB]
    prioStudBModulA = scoreMatrix[studB, modulA]
    prioStudBModulB = scoreMatrix[studB, modulB]

    if prioStudAModulA < prioStudAModulB:
        studAChoice = modulA
    else:
        studAChoice = modulB

    if prioStudBModulA< prioStudBModulB:
        studBChoice = modulA
    else:
        studBChoice = modulB

    if studAChoice == studBChoice:
        if studMark[studA] > studMark[studB]:
            if studAChoice == modulA:
                #alt ist besser
                return False
            else:
                #new ist besser
                return True
        elif studMark[studA] < studMark[studB]:
            if studBChoice == modulB:
                # alt ist besser
                return False
            else:
                # new ist besser
                return True
        else:
            #sollte egal sein
            return True

#Function to read the inital matrix
def read_scoreTable(path):

    with open(path) as f:
        ncols = len(f.readline().split(','))-1

    moduleNames   = np.loadtxt(path, delimiter=',', skiprows=0, dtype="str", usecols=range(1, ncols ))[0]
    moduleSize    = np.loadtxt(path, delimiter=',', skiprows=1, dtype="int", usecols=range(1, ncols ))[0]
    studentNames  = np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1))
    studentGrades = np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=[ncols])
    wishList      = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=range(1, ncols ))

    return [moduleNames, moduleSize, studentNames, studentGrades, wishList]
#----------------------------------------------------------------------------------------------------

def give_optZuordnungsMatrix(zuordungMatrix,sdtFactor,outerCycleCount,innerCycleCount,breakThreshold):
    """
    sdtFactor = 0
    outerCycleCount = 100
    innerCycleCount = 100
    breakThreshold = 100
    """


    plotlist = [[],[]]
    counter = 0
    counter_b = 0

    print str(0).ljust(len(str(innerCycleCount * outerCycleCount) )+1), "Permutations of ", str(innerCycleCount * outerCycleCount)
    for x in range(outerCycleCount):  # erstellen der neuen zuordnungsmatrix
        oldouterscore = give_score(zuordungMatrix, scoreMatrix, sdtFactor)
        for n in range(innerCycleCount):
            newZuordungMatrix = np.copy(zuordungMatrix)
            for m in range(random.choice(choosingList)):
                newZuordungMatrixList = rand_permutation(newZuordungMatrix,constArray)
                newZuordungMatrix = newZuordungMatrixList[0]
                newIsBetterDueToMark = newZuordungMatrixList[1]
            oldScore = give_score(zuordungMatrix, scoreMatrix, sdtFactor)
            newScore = give_score(newZuordungMatrix, scoreMatrix, sdtFactor)

            if newScore[0] < oldScore[0]:
                zuordungMatrix = newZuordungMatrix
            elif newScore[0] == oldScore[0]:
                #2.dary choice due to mark
                if newIsBetterDueToMark == True:
                    zuordungMatrix = newZuordungMatrix

                #2.dary Choice due to standarddeviaion
                #if newScore[1] < oldScore[1]:
                #    zuordungMatrix = newZuordungMatrix
        newouterscore = give_score(zuordungMatrix, scoreMatrix, sdtFactor)

        # print str(oldouterscore).ljust(20), str(newouterscore).ljust(20), str(oldouterscore-newouterscore).ljust(20)
        counter_b += 1
        if counter_b % 50 == 0:
            print str(counter_b * innerCycleCount).ljust(len(str(innerCycleCount*outerCycleCount))+1), "Permutations of ", str(innerCycleCount*outerCycleCount)
        plotlist[0].append(newouterscore[0])
        plotlist[1].append(newouterscore[1])
        if oldouterscore[0] - newouterscore[0] == 0 and oldouterscore[1] - newouterscore[0] == 1:
            counter += 1
        else:
            counter = 0
        if counter > breakThreshold:
            print "Premature break because in the last "+str(breakThreshold)+" tries was no improvment achieved!"
            break

    print "Final score is: "+ str(newouterscore)
    return [zuordungMatrix,plotlist]

def give_plot(optZordungOutput):
    """
    plt.plot(range(0, len(optZordungOutput[1][0] * innerCycleCount), innerCycleCount), optZordungOutput[1][0])
    plt.axhline(y=6 * np.shape(optZordungOutput[0])[0], linewidth=1, color='r')
    plt.ylabel('Score Value')
    plt.ylabel('Count of Permuations')
    """
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(range(0, len(optZordungOutput[1][0] * innerCycleCount), innerCycleCount), optZordungOutput[1][0])
    axarr[0].axhline(y=6 * np.shape(optZordungOutput[0])[0], linewidth=1, color='r')
    axarr[1].plot(range(0, len(optZordungOutput[1][0] * innerCycleCount), innerCycleCount), optZordungOutput[1][1])
    axarr[1].set_xlabel("Trys of Permuations")
    axarr[0].set_ylabel("Score Value")
    axarr[1].set_ylabel("Standard Deviation")

    axarr[0].annotate('Final score of '+str(optZordungOutput[1][0][-1]), xy=(0.9, 0.9), xycoords='axes fraction', fontsize=16, horizontalalignment='right', verticalalignment='top')
    axarr[1].annotate('Final StadDev of '+str(optZordungOutput[1][1][-1])[:4], xy=(0.9, 0.9), xycoords='axes fraction', fontsize=16, horizontalalignment='right',verticalalignment='top')

    plt.show()

def write_table(optZordungOutput):
    zuordungMatrix = optZordungOutput[0]
    zuordungMatrix =  zuordungMatrix*scoreMatrix
    allLines = []
    firstLine = []
    firstLine.append("")
    for name in modName:
        firstLine.append(name)
    allLines.append(firstLine)
    for index,name in enumerate(studName):
        line = []
        line.append(name)
        for zuordnung in zuordungMatrix[index]:
            line.append(zuordnung)
        allLines.append(line)

    f = open('FinalAssigment.csv', 'w')
    for line in allLines:
        for index,zelle in enumerate(line):
            if index < len(line)-1:
                f.write(str(zelle)+",")  # python will convert \n to os.linesep
            else:
                f.write(str(zelle) + "\n")


    f.close()


################################################################################
################################ MAIN PROGRAM ##################################
################################################################################
from timeit import default_timer as timer
start = timer()

#some weird constants that have to be described by christoph--------------------
sdtFactor = 0
outerCycleCount = 1000
innerCycleCount = 100
breakThreshold = 100

#path to the inital student table, has to be done via GUI
path = r'ScoreTable _test.csv'
scoreTable = read_scoreTable(path)

#list of modules, their maximum size, students, their grades and the wishmatrix
moduleNames    = scoreTable[0]
moduleSize     = scoreTable[1]
studentNames   = scoreTable[2]
studentGrades  = scoreTable[3]
wishList       = scoreTable[4]
#-------------------------------------------------------------------------------
print wishList




end = timer()
print str(end - start) + " seconds elapsed!"


#choosingList = give_choosingList()

#zuordungMatrix = give_initZuordungMatrix(scoreMatrix)

#optZordungOutput = give_optZuordnungsMatrix(zuordungMatrix,sdtFactor,outerCycleCount,innerCycleCount,breakThreshold)

#write_table(optZordungOutput)

#give_plot(optZordungOutput)



"""
for n in range(np.shape(zuordungMatrix)[0]):
    print ""
    x = zuordungMatrix[n]
    print str(x[0]).ljust(3),str(x[1]).ljust(3),str(x[2]).ljust(3),str(x[3]).ljust(3),str(x[4]).ljust(3),str(x[5]).ljust(3),str(x[6]).ljust(3),str(x[7]).ljust(3),str(x[8]).ljust(3),str(x[9]).ljust(3),str(x[10]).ljust(3),str(x[11]).ljust(3),str(x[12]).ljust(3),str(x[13]).ljust(3),str(x[14]).ljust(3)

    x = scoreMatrix[n]
    print str(x[0]).ljust(3),str(x[1]).ljust(3),str(x[2]).ljust(3),str(x[3]).ljust(3),str(x[4]).ljust(3),str(x[5]).ljust(3),str(x[6]).ljust(3),str(x[7]).ljust(3),str(x[8]).ljust(3),str(x[9]).ljust(3),str(x[10]).ljust(3),str(x[11]).ljust(3),str(x[12]).ljust(3),str(x[13]).ljust(3),str(x[14]).ljust(3)

"""










