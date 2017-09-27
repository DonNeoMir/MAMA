import numpy as np
import sys
from random import shuffle, randrange


#checks if the assignment violates moduleSize constraints-----------------------
def moduleOccupancy(assignment, moduleSize):
    return not len(np.where(moduleSize < assignment.sum(axis=0))[0]) > 0
#-------------------------------------------------------------------------------

#checks if the input is correct-------------------------------------------------
def correctStudentGrades(studentGrades,studentNames):
    for index,grad in enumerate(studentGrades):
        try:
            int(grad)
        except ValueError:
            print "At least Student ",studentNames[index], " does not have an integer as a grade assigned to him."
            print "The Value assigned to him is >>",grad,"<<. (For help look at example)!" 
            sys.exit()
        else:
            if float(grad)>= 0 and float(grad)<=100:
                pass
            else:
                print "At least Student ",studentNames[index], " does not have a number between 0 and 100 as a grade assigned to him." 
                print "The Value assigned to him is >>",grad,"<<. (For help look at example)!" 
                sys.exit()

def correctModuleSize(moduleSize, moduleNames):
    for index,size in enumerate(moduleSize):
        try:
            int(size)
        except ValueError:
            print "At least Module ",moduleNames[index], " does not have an integer as a max. size assigned to it."
            print "The Value assigned to it is >>",size,"<<. (For help look at example)!" 
            sys.exit() 
        else:
            if  set(range(1,len(moduleSize)+1)) == set(map(int, moduleSize)):
                print "The modulesize includes every number from 1 to 15 so i guess this is a priority list of a student, so i better stop here."
                print "(For help look at example)!"
                sys.exit() 

def correctWishList(wishList,studentNames):
    prioSum = 0
    for  n in range(wishList.shape[1]+1):
        prioSum += n

    for n in np.sum(wishList.astype(np.int), axis=1):
        if prioSum != n:
            print "At least Student >>",studentNames[n],"<< has not used all priorities."
            print "The Sum of his priorities is >>",n,"<< instead of >>",prioSum,"<< which would be expected for >>",wishList.shape[1],"<< modules"
            sys.exit() 

#-------------------------------------------------------------------------------

#creation of random testcases---------------------------------------------------
def randomWishList():
    Listmatrix = []
    for _ in range(40):
        wahlMoeglichkeit = []
        for n in range(1,16):
            wahlMoeglichkeit.append(n)
            shuffle(wahlMoeglichkeit)
        Listmatrix.append(wahlMoeglichkeit)

    return np.asarray(np.matrix(Listmatrix))

def randomModuleSize():
    return np.array(randrange(7,15) for _ in range(15))
#-------------------------------------------------------------------------------