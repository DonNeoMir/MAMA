import os
import numpy as np
from random import randrange
from Tests import moduleOccupancy, correctModuleSize, correctStudentGrades, correctWishList, randomModuleSize, randomWishList
from Output import Plot

def read_initialTable(path):#Function to read the initial matrix

    with open(path) as f:
        ncols = len(f.readline().split(','))-1

    moduleNames   = np.loadtxt(path, delimiter=',', skiprows=0, dtype="str", usecols=range(1, ncols ))[0]
    studentNames  = np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1))

    try:
        moduleSize    = np.loadtxt(path, delimiter=',', skiprows=1, dtype="int", usecols=range(1, ncols ))[0]
    finally:
        correctModuleSize(np.loadtxt(path, delimiter=',', skiprows=1, dtype="str", usecols=range(1, ncols ))[0],moduleNames)
    

    try:
        studentGrades = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=[ncols])
    finally:
        correctStudentGrades(np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=[ncols]),studentNames)
        
    try:
        wishList      = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=range(1, ncols ))
    finally:
        correctWishList(np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1, ncols )),studentNames)

    return [moduleNames, moduleSize, studentNames, studentGrades, wishList]

def initialAssignmentMatrix(wishList, moduleSize):#creates an initial assignment
    (n, m) = np.shape(wishList)
    
    while True:
        assignmentMatrix = np.zeros((n,m), dtype=np.int)
        for studNr in range(n):
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

    return assignmentMatrix

class Initialize():
    
    def __init__(self, gui=None):
        #Constants that describe the optimization process---------------------------
        self.sdtFactor       = 0        #Factor how strong the standard deviation should influence the score
        self.outerCycleCount = 1000     #Count of permutations
        self.innerCycleCount = 100       #Count of permutation to find the next best permutation
        self.breakThreshold  = 100     #Count of how often the outer cycle should run without a change in score.
        self.permutationStrength = .5   #Factor of the exponentialdistribution
        
        #path to the initial student table, has to be done via GUI
        path = r'ScoreTable_test.csv'
        #print os.listdir(os.getcwd())
        self.ospath = os.path.abspath(path)
        scoreTable = read_initialTable(self.ospath)
        
        #list of modules, their maximum size, students, their grades and the wishmatrix-
        self.moduleNames    = scoreTable[0]
        self.moduleSize     = scoreTable[1]
        self.studentNames   = scoreTable[2]
        self.studentGrades  = scoreTable[3]
        wishList       = scoreTable[4]
        
        #TEST---------------------------------
        wishList = randomWishList()#-------
        self.moduleSize = randomModuleSize()#---
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
        
        #creation of the initial (random) assignment------------------------------------
        self.assignmentMatrix = initialAssignmentMatrix(wishList, self.moduleSize)
        
        
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