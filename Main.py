################################################################################
################################ MAIN PROGRAM ##################################
################################################################################
from Initialize import Initialize
from Algorithm import RunOptimizer
from Output import SaveFinalTable

def main(ID=None,que=None):    
    #Initializing---------------------------------------------------------------
    #two variant, GUI with queue, or command line start
    if que:
        que.put("Start of the program")
        que.put("Initializing in progress...")
        values = Initialize()
        que.put("Initializing completed!")
        #finding the best assignment--------------------------------------------
        RunOptimizer(values, ID, que)
        
        
    else:
        print "Start of the program"
        print "Initializing in progress..."
        values = Initialize()
        print "Initializing completed!"    
                 
        #finding the best assignment--------------------------------------------
        RunOptimizer(values)
    
    #OUTPUT---------------------------------------------------------------------
    SaveFinalTable(values)
    values.plot.Save()
#-------------------------------------------------------------------------------


if __name__ == '__main__':
    main()