from random import shuffle
from random import randrange
from random import expovariate as ex
import numpy as np
import random
import math
import sys
import matplotlib.pyplot as plt
import os
import ntpath
import time

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


        break

    print "Initial random assignment is created!"
    return AssignmentMatrix

def read_initialTable(path):#Function to read the initial matrix

    with open(path) as f:
        ncols = len(f.readline().split(','))-1

    moduleNames   = np.loadtxt(path, delimiter=',', skiprows=0, dtype="str", usecols=range(1, ncols ))[0]
    studentNames  = np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1))

    try:
        moduleSize    = np.loadtxt(path, delimiter=',', skiprows=1, dtype="int", usecols=range(1, ncols ))[0]
    finally:
        pass
        #check_moduleSize(np.loadtxt(path, delimiter=',', skiprows=1, dtype="str", usecols=range(1, ncols ))[0],moduleNames)
    

    try:
        studentGrades = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=[ncols])
    finally:
        pass
        #check_studentGrades(np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=[ncols]),studentNames)
        
    try:
        wishList      = np.loadtxt(path, delimiter=',', skiprows=2, dtype="int", usecols=range(1, ncols ))
    finally:
        pass
        #check_wishList(np.loadtxt(path, delimiter=',', skiprows=2, dtype="str", usecols=range(1, ncols )),studentNames)

    return [moduleNames, moduleSize, studentNames, studentGrades, wishList]

path = os.path.abspath('ScoreTable_test.csv')


scoreTable = read_initialTable(path)
moduleNames    = scoreTable[0]
moduleSize     = scoreTable[1]
studentNames   = scoreTable[2]
studentGrades  = scoreTable[3]
wishList       = scoreTable[4]


studenList=[]
for n in range(1,41):
    studenList.append("Student_"+str(n))

assignmentMatrix = give_initAssignmentMatrix(wishList)  

###############################################
###############################################
#Hier gehts los!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
###############################################
###############################################

def give_prioOrderedMatrix(assignmentMatrix,wishList):
    #reorders the assignmentMatrix so that the colums no longer represent the Modul but the prio.
    #so the first colum is whether the studends are assignt to there first prioority or not.
    prioOrderedMatrix = np.empty([wishList.shape[0],wishList.shape[1]])
    for stud in range (0,wishList.shape[0]):
        for prio in range(1,wishList.shape[1]+1):
            for index, modul in enumerate(wishList[1]):
                if modul == prio:
                    prioOrderedMatrix[stud][prio-1] = assignmentMatrix[stud][index]
    return prioOrderedMatrix.astype(int)




fig = plt.figure('matrix figure')
ax = fig.add_subplot(313)
#plt.figure('matrix figure') 
plt.yticks(range(40), studenList)
plt.xticks(range(15), range(1,16))
plt.xlabel("Module Priority")


for n in range(10):
    assignmentMatrix = give_initAssignmentMatrix(wishList)
    
    ax.imshow(give_prioOrderedMatrix(assignmentMatrix,wishList),cmap="RdYlGn", interpolation='nearest')
    plt.xlabel("Module Priority"+str(n))
    plt.ion()
    plt.show()
    plt.pause(0.1)
    #plt.clf()
#plt.imshow(give_prioOrderedMatrix(assignmentMatrix,wishList),cmap="RdYlGn", interpolation='nearest')

