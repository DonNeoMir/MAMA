from random import shuffle
from random import randrange
from random import expovariate as ex
import numpy as np
import random
import math
import sys
import matplotlib.pyplot as plt

def give_testWishList():#TEST: creates a random wishlist
    Listmatrix = []
    for _ in range(40):
        wahlMoeglichkeit = []
        for n in range(1,16):
            wahlMoeglichkeit.append(n)
            shuffle(wahlMoeglichkeit)
        Listmatrix.append(wahlMoeglichkeit)

    return np.asarray(np.matrix(Listmatrix))

def give_testModuleSize():#TEST: creates a random module size list
    return np.array(randrange(7,15) for _ in range(15))

def test_moduleOccupancy(assignment):#checks if the assignment violates moduleSize constraints 
    return not len(np.where(moduleSize < assignment.sum(axis=0))[0]) > 0

def give_initAssignmentMatrix(wishList):#creates an initial assignment
    (n, m) = np.shape(wishList)
    
    while True:
        AssignmentMatrix = np.zeros((n,m), dtype=np.int)
        for studNr in range(n):
            initValues = []
            for _ in range(3):
                while len(initValues) < 3:
                    value = randrange(0, m)
                    if value not in initValues:
                        initValues.append(value)
            for value in initValues:
                AssignmentMatrix[studNr][value] = 1

        if test_moduleOccupancy(AssignmentMatrix):
            break

    print "Initial random assignment is created!"
    return AssignmentMatrix

def give_score(assignmentMatrix, fac):#calculates the current sore and standard deviation over each students score
    produktMatrix = assignmentMatrix*wishList
    return [np.sum(produktMatrix),np.std(produktMatrix.sum(axis=1))]

def give_innerPermuation(zuordungMatrix):
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

        if test_moduleOccupancy(newZuordungMatrix) == True:
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

def rand_permutation(innerZuordungMatrix):
    if random.randint(1, 2) == 1:
        newZuordungMatrixList = give_innerPermuation(innerZuordungMatrix)
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
    prioStudAModulA = wishList[studA,modulA]
    prioStudAModulB = wishList[studA, modulB]
    prioStudBModulA = wishList[studB, modulA]
    prioStudBModulB = wishList[studB, modulB]

    if prioStudAModulA < prioStudAModulB:
        studAChoice = modulA
    else:
        studAChoice = modulB

    if prioStudBModulA< prioStudBModulB:
        studBChoice = modulA
    else:
        studBChoice = modulB

    if studAChoice == studBChoice:
        if studentGrades[studA] > studentGrades[studB]:
            if studAChoice == modulA:
                #alt ist besser
                return False
            else:
                #new ist besser
                return True
        elif studentGrades[studA] < studentGrades[studB]:
            if studBChoice == modulB:
                # alt ist besser
                return False
            else:
                # new ist besser
                return True
        else:
            #sollte egal sein
            return True

def give_optAssignmentMatrix(assignmentMatrix):#main loop function

    plotlist = [[],[]]
    permutationStrength = .5
    counter = 0
    maxIterations = str(innerCycleCount * outerCycleCount)

    for step in range(outerCycleCount):#outer-loop is the actual step-count 
        bestScore = give_score(assignmentMatrix, sdtFactor)
        tmpScore = bestScore
        
        if step % 50 == 0:
            print str(step * innerCycleCount).ljust(len(maxIterations)+1), "Permutations of", maxIterations, "done"
        
        for _ in range(innerCycleCount):#inner-loop determines locally the best step 
            newAssignmentMatrix = np.copy(assignmentMatrix)
            
            for __ in range(int(math.ceil(ex(permutationStrength)))):#exponential distribution gives how many permutations should be done
                newAssignmentMatrix, newIsBetterDueToGrade =   rand_permutation(newAssignmentMatrix)

            newTmpScore = give_score(newAssignmentMatrix, sdtFactor)

            if newTmpScore[0] < tmpScore[0]:
                assignmentMatrix = np.copy(newAssignmentMatrix)#not sure if deepcopy is correct ... was not before
            #elif newTmpScore[0] == tmpScore[0]:
                #2.dary choice due to mark
             #   if newIsBetterDueToGrade:#students with better grades become their choice
              #      assignmentMatrix = np.copy(newAssignmentMatrix)

                #2.dary Choice due to standarddeviaion
                #if newScore[1] < oldScore[1]:
                #    zuordungMatrix = newZuordungMatrix
        newScore = give_score(assignmentMatrix, sdtFactor)
        

        plotlist[0].append(bestScore[0])
        plotlist[1].append(bestScore[1])
        if bestScore[0] - newScore[0] == 0 and bestScore[1] - newScore[1] == 0:
            counter += 1
        else:
            counter = 0
        if counter > breakThreshold:
            print "Premature break because in the last "+str(breakThreshold)+" tries was no improvement achieved!"
            break

        bestScore = newScore#maybe deepcopy


    print "Final score is: "+ str(newScore)
    return [assignmentMatrix,plotlist]

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

def read_initialTable(path):#Function to read the initial matrix

    with open(path) as f:
        ncols = len(f.readline().split(','))-1

    moduleNames   = np.loadtxt(path, delimiter=',', skiprows=0, dtype="str", usecols=range(1, ncols ))[0]
    moduleSize    = np.loadtxt(path, delimiter=',', skiprows=1, dtype="int", usecols=range(1, ncols ))[0]
    studentNames  = np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1))
    studentGrades = np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=[ncols])
    wishList      = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=range(1, ncols ))

    return [moduleNames, moduleSize, studentNames, studentGrades, wishList]

def write_finalTable(optZordungOutput):

    zuordungMatrix = optZordungOutput[0]
    zuordungMatrix =  zuordungMatrix*wishList
    allLines = []
    firstLine = []
    firstLine.append("")
    for name in moduleNames:
        firstLine.append(name)
    allLines.append(firstLine)
    for index,name in enumerate(studentNames):
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

#some weird constants that have to be described by Christoph--------------------
sdtFactor       = 0#has to incorporated ...
outerCycleCount = 1000
innerCycleCount = 10
breakThreshold  = 1000

#path to the initial student table, has to be done via GUI
path = r'ScoreTable _test.csv'
scoreTable = read_initialTable(path)

#list of modules, their maximum size, students, their grades and the wishmatrix
moduleNames    = scoreTable[0]
moduleSize     = scoreTable[1]
studentNames   = scoreTable[2]
studentGrades  = scoreTable[3]
wishList       = scoreTable[4]
#-------------------------------------------------------------------------------

#TEST---------------------------------
wishList = give_testWishList()#-------
moduleSize = give_testModuleSize()#---
#-------------------------------------

###MISSING METHOD## hier sollten noch alle werte der tabelle auf richtigkeit uberpruft werden ...

#creation of the initial (random) assignment
initAssignmentMatrix = give_initAssignmentMatrix(wishList)

#generating the best assignment
optZordungOutput = give_optAssignmentMatrix(initAssignmentMatrix)

write_finalTable(optZordungOutput)

give_plot(optZordungOutput)
end = timer()
print str(end - start) + " seconds elapsed!"







