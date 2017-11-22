import numpy as np
import sys
from random import shuffle, randrange


#checks if the assignment violates moduleSize constraints (TRUE)----------------
def moduleOccupancy(assignment, moduleSize):
    #print moduleSize, assignment.sum(axis=0)
    return not len(np.where(moduleSize < assignment.sum(axis=0))[0]) > 0
#-------------------------------------------------------------------------------

#checks if the input is correct-------------------------------------------------
def correctStudentGrades(rawStudentGrades,studentNames, que=None):
    studentGrades = []
    
    for index,grad in enumerate(rawStudentGrades):
        if grad:
            if grad.isdigit() and int(grad) < 0 or int(grad) > 100:
                if que:
                    que.put("ERROR: At least Student " + studentNames[index] + " does not have a number between 0 and 100 as a grade assigned to him.") 
                    que.put("ERROR: The Value assigned to him is >>" + grad + "<<. (For help look at example)!")
                else:
                    print "At least Student ",studentNames[index], " does not have a number between 0 and 100 as a grade assigned to him." 
                    print "The Value assigned to him is >>",grad,"<<. (For help look at example)!"  
                sys.exit()
            else:
                studentGrades += [int(grad)]
        else:
            studentGrades += [0]
            if que:
                que.put("WARNING: Student " + studentNames[index] + " does not have a grade assigned to him.")
                que.put("WARNING: New grade 0 was assigned.")
            else:
                print "Student ",studentNames[index], " does not have a grade assigned to him."
                print "WARNING: New grade 0 was assigned."

    return np.array(studentGrades)

def correctModuleSize(rawModuleSize, moduleNames, que=None):
    moduleSize = []
    offset = 0
    for index,size in enumerate(rawModuleSize):
        if size and size.isdigit():
            if int(size) < 2:
                if que:
                    que.put("WARNING: Module " + moduleNames[index + offset] + " has little space, maybe a wish?")
                else:
                    print "WARNING: Module " + moduleNames[index + offset] + " has little space, maybe a wish?"
            else:
                moduleSize += [int(size)]
        elif size:
            if que:
                que.put("ERROR: At least Module " + moduleNames[index] + " does not have an integer as a maximum size assigned to it.")
                que.put("ERROR: The Value assigned to it is >>" + size + "<<. (For help look at example)!")
            else:  
                print "At least Module ",moduleNames[index], " does not have an integer as a max. size assigned to it."
                print "The Value assigned to it is >>",size,"<<. (For help look at example)!"
            sys.exit()
        else:
            offset -= 1   

    if len(moduleSize) != len(moduleNames):
        if que:
            que.put("ERROR: Size of Modules is not valid, please check input.")
        else:
            print "ERROR: Size of Modules is not valid, please check input."
        sys.exit()

    return np.array(moduleSize)

def correctWishList(rawWishList,studentNames, que=None):
    wishList = []

    #check if all modules are assigned otherwise fix
    goal = range(1,rawWishList.shape[1] + 1)

    for student, wish in enumerate(rawWishList):
        newWish = []
        for i in wish:
            if i and i.isdigit() and int(i) not in newWish and int(i) in goal:
                prio = int(i)
                newWish += [prio]
            else:
                newWish += [0]
                
        goodValues    = filter(lambda x: x!=0, newWish)
        missingValues = sorted(list(set(goal) - set(goodValues)))
        
        if missingValues:
            ind = 0
            for i in range(len(newWish)):
                if newWish[i] == 0:
                    newWish[i] = missingValues[ind]
                    ind += 1
            if que:
                que.put("WARNING: Student " + studentNames[student] + " set his priorities not entirely correct!")
                que.put("WARNING: they were corrected from >>" + str(wish) + "<< to >>" + str(newWish) + "<<.")
            else:
                print "WARNING: Student " + studentNames[student] + " set his priorities not entirely correct!"
                print  "WARNING: they were corrected from >>" + str(wish) + "<< to >>" + str(newWish) + "<<."
                
        wishList += [newWish]

    return np.array(wishList)
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
