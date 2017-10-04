import numpy as np
from math import ceil
from random import expovariate as ex, randrange, choice, randint
from Tests import moduleOccupancy
 
def evaluateScore(assignmentMatrix, wishList,  fac):#calculates the current sore and standard deviation over each students score
    produktMatrix = assignmentMatrix*wishList
    return [np.sum(produktMatrix),np.std(produktMatrix.sum(axis=1))]

def innerPermutation(assignmentMatrix, moduleSize):#one random student swaps 

    while True:
        stud    = randrange(np.shape(assignmentMatrix)[0])
        module0 = choice(np.where(assignmentMatrix[stud] == 0)[0])
        module1 = choice(np.where(assignmentMatrix[stud] == 1)[0])
        
        assignmentMatrix[stud][module0], assignmentMatrix[stud][module1] = assignmentMatrix[stud][module1], assignmentMatrix[stud][module0]
        if moduleOccupancy(assignmentMatrix, moduleSize):
            return [assignmentMatrix, False]#Here is maybe a breaking criteria missing ....

def outerPermutation(assignmentMatrix):#two random students swap their modules
    studA   = randrange(np.shape(assignmentMatrix)[0])
    moduleA = choice(np.where(assignmentMatrix[studA] == 1)[0])
    
    while True:
        studB   = randrange(np.shape(assignmentMatrix)[0])
        moduleB = choice(np.where(assignmentMatrix[studB] == 1)[0])
        #Check whether one of the students is already in the module he will go in
        if assignmentMatrix[studB][moduleA] == 0 and assignmentMatrix[studA][moduleB] ==0:
            assignmentMatrix[studA][moduleA] = 0
            assignmentMatrix[studB][moduleB] = 0
            assignmentMatrix[studA][moduleB] = 1
            assignmentMatrix[studB][moduleA] = 1
            return [assignmentMatrix, [[studA, moduleA], [studB, moduleB]]]

def randPermutation(assignmentMatrix, wishList, studentGrades, moduleSize):#chooses to permutate inner or intra student
    if randint(1, 2) == 1:
        newAssignmentMatrix, gradeConflict = innerPermutation(assignmentMatrix, moduleSize)
    else:
        newAssignmentMatrix, gradeConflict = outerPermutation(assignmentMatrix)

    if gradeConflict:
        newIsBetterDueToMark = modulPrio(gradeConflict, wishList, studentGrades)
    else:
        newIsBetterDueToMark = False

    return [newAssignmentMatrix,newIsBetterDueToMark]

def modulPrio(auswahl, wishList, studentGrades):#estimates if one students get into a module due to a better grade
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

def RunOptimizer(values, ID=None, que=None):#Main running routine
    assignmentMatrix = values.assignmentMatrix
    innerCycleCount  = values.innerCycleCount
    outerCycleCount  = values.outerCycleCount
    sdtFactor        = values.sdtFactor
    breakThreshold   = values.breakThreshold
    wishList         = values.wishList
    studentGrades    = values.studentGrades
    moduleSize       = values.moduleSize
    plot             = values.plot
    rawWishList      = values.rawWishList
    optScore         = values.optScore
    worstScore       = values.worstScore
 
    scoreList        = []
    stdList          = []
    counter          = 0
    maxIterations    = str(innerCycleCount * outerCycleCount)

    for step in range(outerCycleCount):#outer-loop is the actual step-count 
        bestScore = evaluateScore(assignmentMatrix, wishList,  sdtFactor)
        tmpScore = bestScore
        for _ in range(innerCycleCount):#inner-loop determines locally the best step
            newAssignmentMatrix = np.copy(assignmentMatrix)
            
            for __ in range(int(ceil(ex(values.permutationStrength)))):#exponential distribution gives how many permutations should be done
                newAssignmentMatrix, newIsBetterDueToGrade = randPermutation(newAssignmentMatrix, wishList, studentGrades, moduleSize)

            newTmpScore = evaluateScore(newAssignmentMatrix, wishList, sdtFactor)

            if newTmpScore[0] < tmpScore[0]:
                assignmentMatrix = np.copy(newAssignmentMatrix)#not sure if deepcopy is correct ... was not before
            elif newTmpScore[0] == tmpScore[0]:
                #2.dary choice due to mark
                if newIsBetterDueToGrade:#students with better grades become their choice
                    assignmentMatrix = np.copy(newAssignmentMatrix)
                #2.dary Choice due to standarddeviaion
                #if newScore[1] < oldScore[1]:
                #    zuordungMatrix = newZuordungMatrix
        newScore = evaluateScore(assignmentMatrix, wishList, sdtFactor)
        values.assignmentMatrix = assignmentMatrix

        scoreList.append(bestScore[0])
        stdList.append(bestScore[1])
        if bestScore[0] - newScore[0] == 0 and bestScore[1] - newScore[1] == 0:
            counter += 1
        else:
            counter = 0
        if counter > breakThreshold:
            if que:
                que.put("Premature break because in the last " + str(breakThreshold) + " tries was no improvement achieved!")
            else:
                print "Premature break because in the last " + str(breakThreshold) + " tries was no improvement achieved!"
            break

        bestScore = newScore#maybe deepcopy
        
        if step % 50 == 0:
            if que:
                que.put(str(step * innerCycleCount).ljust(len(maxIterations)) + " Permutations of " + maxIterations + " done")
            else:
                print str(step * innerCycleCount).ljust(len(maxIterations)), "Permutations of", maxIterations, "done"
            plot.Draw(step, (newScore[0] - worstScore) /(optScore - worstScore) * 100, bestScore[1])
            plot.DrawHeat(assignmentMatrix,rawWishList)
    
    plot.Show()
    bestRelScore = str(round( (newScore[0] - worstScore) /(optScore - worstScore) * 100,2))
    if que:
        que.put(bestRelScore +"% of the optimal Score has been reached.")
    else:
        print bestRelScore +"% of the optimal Score has been reached." 
    return [assignmentMatrix, scoreList, stdList]
    