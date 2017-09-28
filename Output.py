import matplotlib.pyplot as plt
import os
import ntpath
import numpy as np

class Plot:
    
    def __init__(self, func):
        plt.ion()
        self.fig = plt.figure()#, (self.axarr, self.axarr1) = plt.subplots()
        self.axarr1 = self.fig.add_subplot(221)
        self.axarr2 = self.fig.add_subplot(223)
        self.axarr3 = self.fig.add_subplot(122)
         
        self.axarr1.set_ylabel("Score Value")
        self.axarr1.axhline(y=(func(1) + func(2) + func(3)) * 40, linewidth=1, color='r')
        
        self.axarr2.set_xlabel("Tries of Permutations")
        self.axarr2.set_ylabel("Standard Deviation")
        self.axarr2.axhline(y=0, linewidth=1, color='r')
        
    def Draw(self,step, score, std):
        self.axarr1.scatter(step, score,  color="blue")
        #self.axarr[0].annotate('Final score of '+ str(scoreList[-1]), xy=(0.9, 0.9), xycoords='axes fraction', fontsize=16, horizontalalignment='right', verticalalignment='top')   
        self.axarr2.scatter(step, std, color="green")
        #self.axarr[1].annotate('Final StadDev of '+str(stdList[-1])[:4], xy=(0.9, 0.9), xycoords='axes fraction', fontsize=16, horizontalalignment='right',verticalalignment='top')
        plt.pause(0.1)

    def DrawHeat(self, assignmentMatrix,rawWishList):
        prioOrderedMatrix = np.empty((rawWishList.shape))
        
        for stud in range (0,rawWishList.shape[0]):
            for prio in range(1,rawWishList.shape[1]+1):
                for index, modul in enumerate(rawWishList[stud]):
                    if modul == prio:
                        prioOrderedMatrix[stud][prio-1] = assignmentMatrix[stud][index]
        prioOrderedMatrix = prioOrderedMatrix.astype(int)

        self.axarr3.imshow(prioOrderedMatrix,cmap="RdYlGn", interpolation='nearest')
        plt.pause(0.1)

    def Show(self):
        plt.ioff()
        plt.show()        
        
    def Save(self):
        self.fig.savefig('FinalPlot.png')
        return
    
    
def SaveFinalTable(values):
    assignmentMatrix = values.assignmentMatrix
    rawWishList      = values.rawWishList
    moduleNames      = values.moduleNames
    studentNames     = values.studentNames
    path             = values.ospath
    
    assignmentMatrix *= rawWishList

    os.chdir(os.path.dirname(path))
    inputName = ntpath.basename(path).split(".")[0]
    for n in range(1,100):
        folderName = "Results_"+str(inputName)+"_"+str(n)
        try:
            os.mkdir(folderName)
            os.chdir(folderName)
            break
        except:
            "This error should have never happend!"

    f = open('FinalAssigment.csv', 'w')
    
    f.write("," + ",".join(moduleNames) + "\n")

    for index,name in enumerate(studentNames):
        f.write(name + "," + ",".join(map(str,assignmentMatrix[index])) + "\n")

    f.close()