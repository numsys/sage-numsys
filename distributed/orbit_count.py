import random

def selectByListFromList(l,selector):
    innerSelect = l[selector[0]]
    if isinstance(innerSelect, list):
        return selectByListFromList(innerSelect,selector[1:])
    else:
        return innerSelect
        
def setByListToList(l,selector,setTo):
    innerSelect = l[selector[0]]
    if isinstance(innerSelect, list):
        return setByListToList(innerSelect,selector[1:],setTo)
    else:
        oldValue = l[selector[0]] 
        l[selector[0]] = setTo
        return oldValue
        
def minusCoordByCoord(a,b):
    return [a[i] - b[i] for i in range(len(a))]
    
def addCoordByCoord(a,b):
    return [a[i] + b[i] for i in range(len(a))]
    
    
def smallerEqCoordByCoord(a,b):    
    for i in range(len(a)):
        if a[i] > b[i]:
            return False
    return True
    
def betweenCoord(a,b,c):
    return smallerEqCoordByCoord(a,b) and smallerEqCoordByCoord(b,c)
    
def count_orbits(ns, startPoints=None):
    import copy
    import pprint
    coverBox = ns.getCoverBox()
    lowerBound = [coverBox[0][i] for i in range(len(coverBox[0]))] 
    sizes = [coverBox[1][i] - coverBox[0][i] + 1 for i in range(len(coverBox[0]))]    
    #print "cover",coverBox
    #print "sizes",sizes 
    stateMatrix = [(None,None)]*sizes[len(sizes)-1]
    for i in range(ns.getDimension()-2,-1,-1):
        tempMatrix = []
        for j in range(sizes[i]):
            tempMatrix.append(copy.deepcopy(stateMatrix))
        stateMatrix = tempMatrix

    periodicPoints = [[0]*ns.getDimension()]
    periodicCycles = [[[0]*ns.getDimension()]]
    signature = [1]
    orbitLengths = [{0:1}] 
    sourceDistances = [{0:1}] 
    setByListToList(stateMatrix,minusCoordByCoord([0]*ns.getDimension(),lowerBound),(0,0))
   
    
    def incWithAdd(target,newVal):
        if newVal not in target:
            target[newVal] = 0
        target[newVal] += 1
    

    def innerStep(val):
        if selectByListFromList(stateMatrix,minusCoordByCoord(val,lowerBound))[0] == None:  
            #print("TRY",val)
            actualOrbit = []
            periodicPointId = None
            periodFound = False
            actualPoint = val
            orbitEndDistanceFromPeriodicPoint = 0
            while not periodFound:
                #print("orbit act point",actualPoint)
                for periodicCyclesIt in range(len(periodicCycles)):
                    if actualPoint in periodicCycles[periodicCyclesIt]:
                        periodicPointId = periodicCyclesIt
                        periodFound = True                
                
                if betweenCoord(coverBox[0],actualPoint,coverBox[1]):
                    stateMatrixValAtActualPoint = selectByListFromList(stateMatrix,minusCoordByCoord(actualPoint,lowerBound))
                    if stateMatrixValAtActualPoint[0] != None:
                        periodicPointId = stateMatrixValAtActualPoint[1]
                        orbitEndDistanceFromPeriodicPoint =  stateMatrixValAtActualPoint[0]
                        periodFound = True
                                     
                actualOrbit.append(actualPoint)
                actualPoint = ns.phiFunction(actualPoint)

                if actualPoint in actualOrbit:
                    actualOrbit = actualOrbit[:actualOrbit.index(actualPoint)+1] 
                    periodFound = True

            #print("orbit",actualOrbit)                
                                        
            if periodicPointId == None:
                periodicPoints.append(actualOrbit[-1])
                periodicPointId = len(periodicPoints) - 1 

                newCycle = ns.getOrbitFrom(actualOrbit[-1])[:-1]
                periodicCycles.append(newCycle)
                cycleLength = len(newCycle)
                signature.append(cycleLength)
                orbitLengths.append({0:cycleLength})
                sourceDistances.append({})
                for cyclePoint in newCycle:
                    incWithAdd(sourceDistances[periodicPointId],max([abs(x) for x in cyclePoint]))
                    setByListToList(stateMatrix,minusCoordByCoord(cyclePoint,lowerBound),(0,periodicPointId))
                

            #print("periodicPointId",periodicPointId)           
            for actualOrbitIt in range(len(actualOrbit)-1):
                if betweenCoord(coverBox[0],actualOrbit[actualOrbitIt],coverBox[1]):
                    try:
                        distanceFromPeriodicPoint = (len(actualOrbit) - 1 - actualOrbitIt + orbitEndDistanceFromPeriodicPoint)   
                        #print("distanceFromPeriodicPoint",distanceFromPeriodicPoint)
                        setByListToList(stateMatrix,minusCoordByCoord(actualOrbit[actualOrbitIt],lowerBound),(distanceFromPeriodicPoint,periodicPointId))
                        signature[periodicPointId] += 1
                        incWithAdd(orbitLengths[periodicPointId],distanceFromPeriodicPoint)
                        incWithAdd(sourceDistances[periodicPointId],max([abs(x) for x in actualOrbit[actualOrbitIt]]))

                    except (ValueError,IndexError): 
                        print("NEMJOOO")
                        print(actualOrbit[actualOrbitIt])
                        print(coverBox)
                        print(smallerEqCoordByCoord(coverBox[0],actualOrbit[actualOrbitIt]))
                        print(smallerEqCoordByCoord(actualOrbit[actualOrbitIt],coverBox[1]))
                        
            #print("stateMatrix",stateMatrix)
            #print("orbitLengths",orbitLengths)
            #print("sourceDistances",sourceDistances)
    
    if startPoints == None:
        act = ns.getPointsInBoxStartVal()
        while not act["finished"]:
            innerStep(act["val"])
            act = ns.getPointsInBoxStepVal(act)
    else:
        for act in startPoints:
            innerStep(act)
       
    def numberKeyDictToArray(d):
        temp = []
        for i in range(max(d)+1):
            temp.append(d[i] if i in d else 0)
        return temp

    orbitLengthsList = [numberKeyDictToArray(x) for x in orbitLengths]
    sourceDistancesList = [numberKeyDictToArray(x) for x in sourceDistances]
    
    return stateMatrix,signature,periodicCycles,orbitLengthsList,sourceDistancesList
