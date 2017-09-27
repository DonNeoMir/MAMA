################################################################################
################################ MAIN PROGRAM ##################################
################################################################################
from Initialize import Initialize
from Algorithm import RunOptimizer
from Output import SaveFinalTable

if __name__ == '__main__':
    #Initilaizing---------------------------------------------------------------
    print "Start of the program"
    print "Initializing in progress..."
    values = Initialize()
    #print str(values)
    print "Initializing completed!"
    
    #finding the best assignment------------------------------------------------
    
    optimalAssignmentMatrix, scoreList, stdList = RunOptimizer(values)
    
    #OUTPUT---------------------------------------------------------------------
    SaveFinalTable(values)
    values.plot.Save()