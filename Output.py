import matplotlib.pyplot as plt
import os
import ntpath

class Plot:
    def __init__(self, func):
        plt.ion()
        self.fig, self.axarr = plt.subplots(2, sharex=True) 
        self.axarr[0].set_ylabel("Score Value")
        self.axarr[0].axhline(y=(func(1) + func(2) + func(3)) * 40, linewidth=1, color='r')
        
        self.axarr[1].set_xlabel("Tries of Permutations")
        self.axarr[1].set_ylabel("Standard Deviation")
        self.axarr[1].axhline(y=0, linewidth=1, color='r')
        
    def Draw(self,step, score, std):
    
        self.axarr[0].scatter(step, score,  color="blue")
        #self.axarr[0].annotate('Final score of '+ str(scoreList[-1]), xy=(0.9, 0.9), xycoords='axes fraction', fontsize=16, horizontalalignment='right', verticalalignment='top')   
        self.axarr[1].scatter(step, std, color="green")
        #self.axarr[1].annotate('Final StadDev of '+str(stdList[-1])[:4], xy=(0.9, 0.9), xycoords='axes fraction', fontsize=16, horizontalalignment='right',verticalalignment='top')
        plt.pause(0.1)
    
    def Halt(self):
        plt.pause(2)
        
        
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
    print path
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