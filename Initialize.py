import os
import numpy as np
from random import randrange
from Tests import moduleOccupancy, correctModuleSize, correctStudentGrades, correctWishList, randomModuleSize, randomWishList, correctPath
from Output import Plot

def read_initialTable(path, que=None):#Function to read the initial matrix

    with open(path) as f:
        ncols = len(f.readline().split(','))-1

    moduleNames   = np.loadtxt(path, delimiter=',', skiprows=0, dtype="str", usecols=range(1, ncols ))[0]
    studentNames  = np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1))

    try:
        moduleSize = np.loadtxt(path, delimiter=',', skiprows=1, dtype="int", usecols=range(1, ncols ))[0]
    finally:
        correctModuleSize(np.loadtxt(path, delimiter=',', skiprows=1, dtype="str", usecols=range(1, ncols ))[0],moduleNames, que)
    

    try:
        studentGrades = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=[ncols])
    finally:
        correctStudentGrades(np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=[ncols]),studentNames, que)
        
    try:
        wishList = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=range(1, ncols ))
    finally:
        correctWishList(np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1, ncols )),studentNames, que)


    return [moduleNames, moduleSize, studentNames, studentGrades, wishList]

def initialAssignmentMatrix(wishList, moduleSize, que=None):#creates an initial assignment
    (n, m) = np.shape(wishList)
    assignmentMatrix = np.zeros((n,m), dtype=np.int)
        
    for studNr in range(n):
        while True:
            initValues = []
            for _ in range(3):
                while len(initValues) < 3:
                    value = randrange(0, m)
                    if value not in initValues:
                        initValues.append(value)
            for value in initValues:
                assignmentMatrix[studNr][value] = 1

            if moduleOccupancy(assignmentMatrix, moduleSize):
                break
            else:
                for value in initValues:
                    assignmentMatrix[studNr][value] = 0               
    return assignmentMatrix

class Initialize():
    
    def __init__(self, gui=None, que=None, path = None):
        #Constants that describe the optimization process---------------------------
        self.sdtFactor           = 0        #Factor how strong the standard deviation should influence the score
        self.outerCycleCount     = 1000     #Count of permutations
        self.innerCycleCount     = 100      #Count of permutation to find the next best permutation
        self.breakThreshold      = 100      #Count of how often the outer cycle should run without a change in score.
        self.permutationStrength = .5       #Factor of the exponentialdistribution
        
        #path to the initial student table, has to be done via GUI
        if path:
            pathToTable = path
            #pathToTable = r'ScoreTable_test.csv'
            correctPath(pathToTable, que)
        else:
            pathToTable = r'MMLS Enrollment 2017_wish list for program check.csv'
            pathToTable = r"ScoreTable_test.csv"
            pathToTable = r"MMLSHandCheck.csv"
            correctPath(pathToTable, que)
            
        self.ospath = os.path.abspath(pathToTable)    
        scoreTable = read_initialTable(self.ospath, que)

        
        #list of modules, their maximum size, students, their grades and the wishmatrix-
        self.moduleNames    = scoreTable[0]
        self.moduleSize     = scoreTable[1]
        self.studentNames   = scoreTable[2]
        self.studentGrades  = scoreTable[3]
        wishList            = scoreTable[4]

        #TEST---------------------------------
        #wishList = randomWishList()#-------
        #self.moduleSize = randomModuleSize()#---
        #-------------------------------------

        #Weighting of the wishList with a different function (best and worst get more weight)
        self.func = np.vectorize(lambda x: (5. - x)/(x*(x-16.)))
        self.rawWishList = wishList
        self.wishList = self.func(wishList)

        #best and worst score possible
        self.optScore   = len(self.studentNames)*( self.func(1) +  self.func(2) +  self.func(3))
        self.worstScore = len(self.studentNames)*(self.func(15) + self.func(14) + self.func(13))

        #Plot--------------------------------
        if gui:
            self.plot = Plot(gui)
        else:
            self.plot = Plot()
        print "BLUB"
        #creation of the initial (random) assignment------------------------------------
        self.assignmentMatrix = initialAssignmentMatrix(wishList, self.moduleSize, que)
        print "BLUB"
        
    def __str__(self):
        out = "\n"
        out +=  str(len(self.moduleNames)) + " Modules were found (Module : maxSeats): \n"
        
        maxLenModul = len(max(self.moduleNames, key=lambda x: len(x)))
        maxLenSize  = len(str(max(self.moduleSize)))
        
        for i in range(len(self.moduleNames)):
            out += "(" + self.moduleNames[i].ljust(maxLenModul) + " : " + str(self.moduleSize[i]).ljust(maxLenSize) + ")\n"
        
        out += "\n" + str(len(self.studentNames)) + " Students were found (Student : Grade): \n"
            
        maxLenStudent = len(max(self.studentNames, key=lambda x: len(x)))
        maxLenGrade   = len(str(max(self.studentGrades)))    
            
        for i in range(len(self.studentNames)):
            out += "(" + self.studentNames[i].ljust(maxLenStudent) + " : " + str(self.studentGrades[i]).ljust(maxLenGrade) + ")\n"
            
        return out