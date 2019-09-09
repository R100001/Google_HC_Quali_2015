import operator
from time import time
from math import ceil

def main():
    r,rS,unSlots,pl,servers = readProblem()
    capacity = [0 for i in range(r)]
    servers.sort(reverse=True)
    sM=slotsArray(r,rS,unSlots)#available slots Matrix
    bCrs, bC=measures(r,rS,servers, unSlots,sM)#best case (average) capacity per row's slot
    scl=grouping(1,0,servers)#creates a dictionary of servers grouped/clustered by their size
    
    nServersSizes = [0 for i in range(max([key[0] for key in scl.keys()]))]
    for server in servers:
        nServersSizes[server[1]-1] += 1
    
    usedServers = [[-1,-1] for i in range(len(servers))]
    availableSlots = [i for i in availSlotsR(rS, sM)]
    print(availableSlots)
    
    for row in range(len(sM)):

        for space in sM[row]:
            serversSizes, indeces = getSizes(space[0], space[1], nServersSizes)
            for i in range(len(serversSizes)):
                nServersSizes[i] -= serversSizes[i]

            for size in range(len(serversSizes)-1, -1, -1): #reverse traverse of servers' sizes 
                                                #needed, starting from the biggest ones.
                for num in range(serversSizes[size]):
                    serverChosen = None
                    nextBigCap=0
                    i = 1
                    mul = 1
                    while True:
                        flag = True
                        try:
                            listChosen=scl.pop((size+1, ceil(bCrs[row]) + nextBigCap))
                        except:
                            flag = False
                        if listChosen != [] and flag:
                            serverChosen = listChosen[0]
                            capacity[row] += serverChosen[2]
                            scl.update({(size+1, ceil(bCrs[row]) + nextBigCap): listChosen[1:]})
                            bCrs[row], availableSlots[row] = computeNewBestCase(serverChosen, availableSlots[row], bCrs[row])
                            break
                        nextBigCap += i * mul
                        i += 1
                        mul *= -1
                        
                    usedServers[serverChosen[3]-1][0] = row
                    usedServers[serverChosen[3]-1][1] = indeces[-1]
                    indeces.pop(-1)
    
    print("Final capacity:", sum(capacity))
    print("Final score:", sum(capacity)-max(capacity))
    
    makeOutF(usedServers)
        
def measures(r,rS,servers, unSlots,sM):
    total_size = r*rS-len(unSlots) #real total size = all slots - unavailable slots
    currSize=0 #currentSize
    best_cap=0 #best case total capacity
    
    for s in servers:
        if currSize+s[1]>total_size:
            break
        currSize+=s[1]
        best_cap+=s[2]
    print("Best case:", best_cap)
    print("Best score:", best_cap - ceil(best_cap/r))
    bCr=best_cap/r #best case (average) total capacity per row
    return [bCr/i for i in availSlotsR(rS,sM)], bCr #best case (average) capacity per row's slot

def cpSlot(l):#capacity per slot
    return l[1]//l[0]

def readProblem():
    unSlots, servers=[],[]
    sl,pl,r,rS,idS = 0,0,0,0,0
    with open("dc.in",'r') as infile:
        i=1
        for line in nonblank_lines(infile):
            l=[int(x) for x in line.split()]
            if i==1:
                r=l[0]
                rS=l[1]                
                sl=l[2]
                pl=l[3]
                i=i+1
            elif i<=sl+1:
                unSlots.append(l)  
                i=i+1
            elif i>sl:
                l.insert(0,cpSlot(l))
                l.append(idS)
                idS+=1
                servers.append(l)
    infile.close()
    return r, rS,unSlots,pl,servers

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line
            
def slotsArray(rows, slots, unavSlots):
    unavSlots.sort()
    freeSlots = [[] for i in range(rows)]
    j = 0
    for i in range(rows):
        if unavSlots[j][0] != i:
            freeSlots[i].append([0, slots])
            continue
        prevAnav = -1
        while(True):
            if unavSlots[j][0] == i:
                freeSlots[i].append([prevAnav+1, unavSlots[j][1]])
                prevAnav = unavSlots[j][1]
                j += 1
            else:
                break
            if j == len(unavSlots):
                break
        freeSlots[i].append([prevAnav+1, slots])
    return freeSlots

def availSlotsR(rS,sM):   
    avSr=[]#unavailable slots per row
    for r in sM:
        sumR=0
        i=1
        while i<len(r):
            sumR+=r[i][0]-r[i-1][1]
            i+=1
        avSr.append(rS-sumR)
    return avSr

def grouping(prime,sec,aList):#menei

    if aList is None:
        return None
    
    aList.sort(key = operator.itemgetter(prime,sec))

    aDict = dict()

    for el in aList:
        if ( el[prime], el[sec] ) in aDict:
            aDict[ ( el[prime], el[sec] ) ].append(el)
        else:
            aDict[ ( el[prime], el[sec] ) ]=[el]

    return aDict

def makeOutF(usedServers): 
    with open("outfile.txt",'w') as outfile:
        for server in usedServers:
            if server[0] == -1:
                outfile.write("x\n")
            else:
                outfile.write(str(server[0]) + " " + str(server[1]) + " 0\n")
    
def computeNewBestCase(aServer, availableSlots, bestCase):
    try:
        return (bestCase * availableSlots - aServer[2]) / (availableSlots - aServer[1]), availableSlots - aServer[1]
    except:
        return 0, 0
    
def getSizes(space0, space1, aList):
    aSpace = space1 - space0
    nServers = [0 for i in range(len(aList))]
    for i in range(len(aList)-1, -1, -1):
        n = aSpace // (i+1)
        if n > aList[i]:
            n = aList[i]
        aSpace -= n * (i+1)
        nServers[i] = n
    indeces = [space0]
    index = 0
    for size in range(len(nServers)):
        for j in range(nServers[size]):
            index = size + 1
            indeces.append(index+indeces[-1])
    indeces.pop(-1)
    return nServers, indeces

x = time()
main()
print("Computational time:",time() - x)
