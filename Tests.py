import numpy as np
import sys
from random import shuffle, randrange


#checks if the assignment violates moduleSize constraints (TRUE)----------------
def moduleOccupancy(assignment, moduleSize):
    #print moduleSize, assignment.sum(axis=0)
    return not len(np.where(moduleSize < assignment.sum(axis=0))[0]) > 0
#-------------------------------------------------------------------------------

#checks if the input is correct-------------------------------------------------
def correctStudentGrades(studentGrades,studentNames, que=None):
    for index,grad in enumerate(studentGrades):
        try:
            int(grad)
        except ValueError:
            if que:
                que.put("ERROR: At least Student " + studentNames[index] + " does not have an integer as a grade assigned to him.")
                que.put("ERROR: The Value assigned to him is >>" + grad + "<<. (For help look at example)!")
            else:
                print "At least Student ",studentNames[index], " does not have an integer as a grade assigned to him."
                print "The Value assigned to him is >>",grad,"<<. (For help look at example)!"
            sys.exit()
        else:
            if float(grad)>= 0 and float(grad)<=100:
                pass
            else:
                if que:
                    que.put("ERROR: At least Student " + studentNames[index] + " does not have a number between 0 and 100 as a grade assigned to him.") 
                    que.put("ERROR: The Value assigned to him is >>" + grad + "<<. (For help look at example)!")
                else:
                    print "At least Student ",studentNames[index], " does not have a number between 0 and 100 as a grade assigned to him." 
                    print "The Value assigned to him is >>",grad,"<<. (For help look at example)!"                    
                sys.exit()

def correctModuleSize(moduleSize, moduleNames, que=None):
    for index,size in enumerate(moduleSize):
        try:
            int(size)
        except:
            if que:
                que.put("ERROR: At least Module " + moduleNames[index] + " does not have an integer as a maximum size assigned to it.")
                que.put("ERROR: The Value assigned to it is >>" + size + "<<. (For help look at example)!")
            else:  
                print "At least Module ",moduleNames[index], " does not have an integer as a max. size assigned to it."
                print "The Value assigned to it is >>",size,"<<. (For help look at example)!"
            sys.exit() 

    if  range(1,len(moduleSize)+1) == sorted(map(int, moduleSize)):
        if que:
            que.put("ERROR: The modulesize includes every number from 1 to 15, this looks like a priority list of a student.")
            que.put("ERROR: Please enter the correct modulesizes (For help look at example)!")
        else:
            print "The modulesize includes every number from 1 to 15 so i guess this is a priority list of a student, so i better stop here."
            print "(For help look at example)!"  
        sys.exit() 

def correctWishList(wishList,studentNames, que=None):
    prioSum = sum(range(wishList.shape[1]+1))

    summo = np.sum(wishList.astype(np.int), axis=1)
    for i in range(len(wishList.astype(np.int))):
        if range(1,wishList.shape[1] + 1) != sorted(wishList.astype(np.int)[i]):
            if que:
                que.put("ERROR: At least Student >>" + studentNames[i] + "<< has not used all priorities.")
                que.put("ERROR: The Sum of his priorities is >>" + str(summo[i]) + "<< instead of >>" + str(prioSum) + "<< which would be expected for >>" + str(wishList.shape[1]) + "<< modules")
            else:
                print "At least Student >>",studentNames[i],"<< has not used all priorities."
                print "The Sum of his priorities is >>",summo[i],"<< instead of >>",prioSum,"<< which would be expected for >>",wishList.shape[1],"<< modules"
            #sys.exit() 
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
    return np.array([randrange(7,15) for _ in range(15)])
#-------------------------------------------------------------------------------

#checking if the file exists----------------------------------------------------
def correctPath(path, que=None):
    try:
        with open(path) as _:
            if que:
                que.put("File found and read")
            else:
                print "File found and read"
            pass
    except:
        if que:
            que.put("ERROR: file not found OR not readable, please choose another file")
        else:
            print "ERROR: file not found OR not readable, please choose another file"
        sys.exit()
#-------------------------------------------------------------------------------
