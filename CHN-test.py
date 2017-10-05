import numpy as np
import random

import matplotlib.pyplot as plt
def moduleOccupancy(assignment, moduleSize):
    return not len(np.where(moduleSize < assignment.sum(axis=0))[0]) > 0

def DrawHeat(assignmentMatrix,rawWishList):
    prioOrderedMatrix = np.empty((rawWishList.shape))
    
    for stud in range (0,rawWishList.shape[0]):
        for prio in range(1,rawWishList.shape[1]+1):
            for index, modul in enumerate(rawWishList[1]):
                if modul == prio:
                    prioOrderedMatrix[stud][prio-1] = assignmentMatrix[stud][index]
    prioOrderedMatrix = prioOrderedMatrix.astype(int)

    plt.imshow(prioOrderedMatrix,cmap="RdYlGn", interpolation='nearest')
    #plt.minorticks_on()
    plt.xticks( np.arange(0.5,15))#hier
    plt.yticks( np.arange(0.5,40), range(1,41) )#hier
    plt.grid(b=True, which='both', color='0.65',linestyle='-')

    #plt.grid(color='w', linestyle='-', linewidth=0.5)
    plt.show()


def read_initialTable(path):#Function to read the initial matrix

    with open(path) as f:
        ncols = len(f.readline().split(','))-1

    moduleNames   = np.loadtxt(path, delimiter=',', skiprows=0, dtype="str", usecols=range(1, ncols ))[0]
    studentNames  = np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1))

    try:
        moduleSize    = np.loadtxt(path, delimiter=',', skiprows=1, dtype="int", usecols=range(1, ncols ))[0]
    finally:
        pass
        #correctModuleSize(np.loadtxt(path, delimiter=',', skiprows=1, dtype="str", usecols=range(1, ncols ))[0],moduleNames)
    

    try:
        studentGrades = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=[ncols])
    finally:
        pass
        #correctStudentGrades(np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=[ncols]),studentNames)
        
    try:
        wishList      = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=range(1, ncols ))
    finally:
        pass
        #correctWishList(np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1, ncols )),studentNames)

    return [moduleNames, moduleSize, studentNames, studentGrades, wishList]

wishList = read_initialTable("ScoreTable_test.csv")[-1]
moduleSize = read_initialTable("ScoreTable_test.csv")[1]
def initialAssignmentMatrix(wishList, moduleSize):#creates an initial assignment
    (n, m) = np.shape(wishList)
    
    while True:
        assignmentMatrix = np.zeros((n,m), dtype=np.int)
        for studNr in range(n):
            initValues = []
            for _ in range(3):
                while len(initValues) < 3:
                    value = random.randrange(0, m)
                    if value not in initValues:
                        initValues.append(value)
            for value in initValues:
                assignmentMatrix[studNr][value] = 1

        if moduleOccupancy(assignmentMatrix, moduleSize):
            break

    return assignmentMatrix

assignmentMatrix = initialAssignmentMatrix(wishList,moduleSize)

DrawHeat(assignmentMatrix,wishList)