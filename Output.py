import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import ntpath
import numpy as np

class Plot:
    
    def __init__(self, gui=None):
        self.fig = plt.figure(figsize=(6,5))
        self.fig.set_facecolor("grey")
        self.axarr1 = self.fig.add_subplot(221)
        self.axarr2 = self.fig.add_subplot(223)
        self.axarr3 = self.fig.add_subplot(122)
         
        self.axarr1.set_ylabel("Score Value")
        self.axarr1.axhline(y=100.0, linewidth=1, color='r')
        
        self.axarr2.set_xlabel("Tries of Permutations")
        self.axarr2.set_ylabel("Standard Deviation")
        self.axarr2.axhline(y=0, linewidth=1, color='r')
        
        self.gui = gui
        
        if self.gui:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.gui)
            self.canvas.get_tk_widget().place(x=420, y=0)

        
    def Draw(self,step, score, std):
        self.axarr1.scatter(step, score, color="green") 
        self.axarr2.scatter(step, std  , color="blue")
        if self.gui:
            self.canvas.draw()
        else:
            plt.pause(0.001)

    def DrawHeat(self, assignmentMatrix,rawWishList):
        prioOrderedMatrix = np.empty((rawWishList.shape))
        
        for stud in range (0,rawWishList.shape[0]):
            for prio in range(1,rawWishList.shape[1]+1):
                for index, modul in enumerate(rawWishList[stud]):
                    if modul == prio:
                        prioOrderedMatrix[stud][prio-1] = assignmentMatrix[stud][index]
        prioOrderedMatrix = prioOrderedMatrix.astype(int)

        self.axarr3.imshow(prioOrderedMatrix,cmap="RdYlGn", interpolation='nearest')


    def Show(self):
        if not self.gui:
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
            "This error should have never happened!"

    f = open('FinalAssigment.csv', 'w')
    
    f.write("," + ",".join(moduleNames) + "\n")

    for index,name in enumerate(studentNames):
        f.write(name + "," + ",".join(map(str,assignmentMatrix[index])) + "\n")

    f.close()