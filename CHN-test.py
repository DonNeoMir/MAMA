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
    fig, ax = plt.subplots()
    im = ax.imshow(prioOrderedMatrix,cmap="RdYlGn", interpolation='nearest')
    #fig.colorbar(im)
    xlabels = np.arange(1,16)
    xlocs = np.arange(len(xlabels))

    ylabels = np.arange(1,41)
    ylocs = np.arange(len(ylabels))
    
    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.xlabel("Modul Priority")
    plt.ylabel("Students ID")

    ax.xaxis.set_ticks(xlocs + 0.5, minor=True)
    ax.xaxis.set(ticks=xlocs, ticklabels=xlabels)
    ax.yaxis.set_ticks(ylocs + 0.5, minor=True)
    ax.yaxis.set(ticks=ylocs, ticklabels=ylabels)


    # Turn on the grid for the minor ticks
    ax.grid(True, which='minor')
    """
    ax.minorticks_on()


    ax.xaxis.set_xticks( np.arange(1,15,2),np.arange(2,15,2))#hier
    ax.xlabel("Modul Priority")#hier
    ax.yticks( np.arange(1,40,2), [] )#hier
    ax.ylabel("Students")#hier
    ax.grid(True, which='minor', color='0.65',linestyle='-')

    #plt.grid(color='w', linestyle='-', linewidth=0.5)
    """

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