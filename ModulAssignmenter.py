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

def give_innerPermutation(assignmentMatrix):#one random student swaps 

    while True:
        stud    = randrange(np.shape(assignmentMatrix)[0])
        module0 = random.choice(np.where(assignmentMatrix[stud] == 0)[0])
        module1 = random.choice(np.where(assignmentMatrix[stud] == 1)[0])
        
        assignmentMatrix[stud][module0], assignmentMatrix[stud][module1] = assignmentMatrix[stud][module1], assignmentMatrix[stud][module0]
        
        if test_moduleOccupancy(assignmentMatrix):
            return [assignmentMatrix, False]#Here is maybe a breaking criteria missing ....

def give_outerPermutation(assignmentMatrix):#two random students swap their modules
    studA   = randrange(np.shape(assignmentMatrix)[0])
    moduleA = random.choice(np.where(assignmentMatrix[studA] == 1)[0])
    
    while True:
        studB   = randrange(np.shape(assignmentMatrix)[0])
        moduleB = random.choice(np.where(assignmentMatrix[studB] == 1)[0])
        #Check whether one of the students is already in the module he will go in
        if assignmentMatrix[studB][moduleA] == 0 and assignmentMatrix[studA][moduleB] ==0:
            assignmentMatrix[studA][moduleA] = 0
            assignmentMatrix[studB][moduleB] = 0
            assignmentMatrix[studA][moduleB] = 1
            assignmentMatrix[studB][moduleA] = 1
            return [assignmentMatrix, [[studA, moduleA], [studB, moduleB]]]

def give_randPermutation(assignmentMatrix):#chooses to permutate inner or intra student
    if random.randint(1, 2) == 1:
        newAssignmentMatrix, gradeConflict = give_innerPermutation(assignmentMatrix)

    else:
        newAssignmentMatrix, gradeConflict = give_outerPermutation(assignmentMatrix)

    if gradeConflict:
        newIsBetterDueToMark = give_modulPrio(gradeConflict)
    else:
        newIsBetterDueToMark = False

    return [newAssignmentMatrix,newIsBetterDueToMark]

def give_modulPrio(auswahl):#estimates if one students get into a module due to a better grade
    [[studA, moduleA], [studB, moduleB]] = auswahl
    
    prioStudAModulA = wishList[studA][moduleA]
    prioStudAModulB = wishList[studA][moduleB]
    prioStudBModulA = wishList[studB][moduleA]
    prioStudBModulB = wishList[studB][moduleB]
    
    studAChoice = [moduleB, moduleA][prioStudAModulA < prioStudAModulB]
    studBChoice = [moduleB, moduleA][prioStudBModulA < prioStudBModulB]

    if studAChoice == studBChoice:
        if studentGrades[studA] > studentGrades[studB]:
            if studAChoice == moduleA:
                #old module A is better for studA
                return False
            else:
                #new module B is better for studA
                return True
        elif studentGrades[studA] < studentGrades[studB]:
            if studBChoice == moduleB:
                #old module B is better for studB
                return False
            else:
                #new module A is better for studB
                return True
        else:
            #does not matter which assignment to take
            return True

def give_optAssignmentMatrix(assignmentMatrix):#main loop function

    scoreList = []
    stdList = []
    permutationStrength = .5
    counter = 0
    maxIterations = str(innerCycleCount * outerCycleCount)

    for step in range(outerCycleCount):#outer-loop is the actual step-count 
        bestScore = give_score(assignmentMatrix, sdtFactor)
        tmpScore = bestScore
        
        if step % 50 == 0:
            print str(step * innerCycleCount).ljust(len(maxIterations)), "Permutations of", maxIterations, "done"
        
        for _ in range(innerCycleCount):#inner-loop determines locally the best step 
            newAssignmentMatrix = np.copy(assignmentMatrix)
            
            for __ in range(int(math.ceil(ex(permutationStrength)))):#exponential distribution gives how many permutations should be done
                newAssignmentMatrix, newIsBetterDueToGrade = give_randPermutation(newAssignmentMatrix)

            newTmpScore = give_score(newAssignmentMatrix, sdtFactor)

            if newTmpScore[0] < tmpScore[0]:
                assignmentMatrix = np.copy(newAssignmentMatrix)#not sure if deepcopy is correct ... was not before
            elif newTmpScore[0] == tmpScore[0]:
                #2.dary choice due to mark
                if newIsBetterDueToGrade:#students with better grades become their choice
                    assignmentMatrix = np.copy(newAssignmentMatrix)

                #2.dary Choice due to standarddeviaion
                #if newScore[1] < oldScore[1]:
                #    zuordungMatrix = newZuordungMatrix
        newScore = give_score(assignmentMatrix, sdtFactor)
        

        scoreList.append(bestScore[0])
        stdList.append(bestScore[1])
        if bestScore[0] - newScore[0] == 0 and bestScore[1] - newScore[1] == 0:
            counter += 1
        else:
            counter = 0
        if counter > breakThreshold:
            print "Premature break because in the last "+str(breakThreshold)+" tries was no improvement achieved!"
            break

        bestScore = newScore#maybe deepcopy


    print "Final score is: "+ str(newScore)
    return [assignmentMatrix, scoreList, stdList]

def give_plot(optZordungOutput):
    """
    plt.plot(range(0, len(optZordungOutput[1][0] * innerCycleCount), innerCycleCount), optZordungOutput[1][0])
    plt.axhline(y=6 * np.shape(optZordungOutput[0])[0], linewidth=1, color='r')
    plt.ylabel('Score Value')
    plt.ylabel('Count of Permuations')
    """
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(range(0, len(optZordungOutput[1][0] * innerCycleCount), innerCycleCount), optZordungOutput[1][0])
#    axarr[0].axhline(y=6 * np.shape(optZordungOutput[0])[0], linewidth=1, color='r')
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
    studentNames  = np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1))

    try:
    	moduleSize    = np.loadtxt(path, delimiter=',', skiprows=1, dtype="int", usecols=range(1, ncols ))[0]
    finally:
    	check_moduleSize(np.loadtxt(path, delimiter=',', skiprows=1, dtype="str", usecols=range(1, ncols ))[0],moduleNames)
    

    try:
    	studentGrades = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=[ncols])
    finally:
    	check_studentGrades(np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=[ncols]),studentNames)
    	
    try:
    	wishList      = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=range(1, ncols ))
    finally:
    	check_wishList(np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1, ncols )),studentNames)

    return [moduleNames, moduleSize, studentNames, studentGrades, wishList]

def write_finalTable(assignmentMatrix):

    assignmentMatrix *= rawWishList

    f = open('FinalAssigment.csv', 'w')
    
    f.write("," + ",".join(moduleNames) + "\n")

    for index,name in enumerate(studentNames):
        f.write(name + "," + ",".join(map(str,assignmentMatrix[index])) + "\n")

    f.close()


def check_studentGrades(studentGrades,studentNames):
	for index,grad in enumerate(studentGrades):
		try:
			int(grad)
		except ValueError:
			print "At least Student ",studentNames[index], " does not have a intiger as a Grad assignt to him."
			print "The Value assignt to him is >>",grad,"<<. (For help look at example)!" 
			sys.exit()
		else:
			if float(grad)>= 0 and float(grad)<=100:
				pass
			else:
				print "At least Student ",studentNames[index], " does not have a Number between 0 and 100 as a Grad assignt to him." 
				print "The Value assignt to him is >>",grad,"<<. (For help look at example)!" 
				sys.exit()

def check_moduleSize(moduleSize, moduleNames):
	for index,size in enumerate(moduleSize):
		try:
			int(size)
		except ValueError:
			print "At least Module ",moduleNames[index], " does not have a integer as a max. size assignt to it."
			print "The Value assignt to it is >>",size,"<<. (For help look at example)!" 
			sys.exit() 
		else:
			if  set(range(1,len(moduleSize)+1)) == set(map(int, moduleSize)):
				print "The modulesize inlcudes every number from 1 to 15 so i guess this is a priority list of a student, so i better stopt here."
				print "(For help look at example)!"
				sys.exit() 

def check_wishList(wishList,studentNames):
	prioSum = 0
	for  n in range(wishList.shape[1]+1):
		prioSum += n

	for index,n in enumerate(np.sum(wishList.astype(np.int), axis=1)):
		if prioSum != n:
			print "At least Student >>",studentNames[n],"<< has not used all prioritie."
			print "The Sum of his priorites is >>",n,"<< insteat of >>",prioSum,"<< which would be expected for >>",wishList.shape[1],"<< modules"
			sys.exit() 

				

################################################################################
################################ MAIN PROGRAM ##################################
################################################################################


from timeit import default_timer as timer
start = timer()

#Constants that describe the optimization process-------------------------------
sdtFactor       = 0#has to incorporated ...
outerCycleCount = 1000
innerCycleCount = 10
breakThreshold  = 1000

#path to the initial student table, has to be done via GUI----------------------
path = r'ScoreTable _test.csv'
scoreTable = read_initialTable(path)

#list of modules, their maximum size, students, their grades and the wishmatrix-
moduleNames    = scoreTable[0]
moduleSize     = scoreTable[1]
studentNames   = scoreTable[2]
studentGrades  = scoreTable[3]
wishList       = scoreTable[4]

#TEST---------------------------------
ishList = give_testWishList()#-------
moduleSize = give_testModuleSize()#---
#-------------------------------------

#Weighting of the wishList with a different function (best and worst get more weight)
func = np.vectorize(lambda x: (5. - x)/(x*(x-16.)))
rawWishList = wishList
wishList = func(wishList)

#creation of the initial (random) assignment------------------------------------
initAssignmentMatrix = give_initAssignmentMatrix(wishList)

#finding the best assignment----------------------------------------------------
optimalAssignmentMatrix, scoreList, stdList = give_optAssignmentMatrix(initAssignmentMatrix)

#OUTPUT-------------------------------------------------------------------------
write_finalTable(optimalAssignmentMatrix)
give_plot(scoreList, stdList)


end = timer()
print str(end - start) + " seconds elapsed!"


