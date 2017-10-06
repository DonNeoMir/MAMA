################################################################################
################################ MAIN PROGRAM ##################################
################################################################################
from Initialize import Initialize
from Algorithm import RunOptimizer
from Output import SaveFinalTable

def main(que=None, guiroot=None, path=None):    
    #Initializing---------------------------------------------------------------
    #two variant, GUI with queue, or command line start
    if que:
        que.put("Start of the program")
        que.put("Initializing in progress...")
        values = Initialize(guiroot, que, path)
        que.put("Initializing completed!")

        RunOptimizer(values, que)
        SaveFinalTable(values, que)
        values.plot.Save()
        que.put("Program finished!")
    else:
        print "Start of the program"
        print "Initializing in progress..."
        values = Initialize()
        print "Initializing completed!"    

        RunOptimizer(values)
        SaveFinalTable(values)
        values.plot.Save()
        print "Program finished!"

if __name__ == '__main__':
    main()