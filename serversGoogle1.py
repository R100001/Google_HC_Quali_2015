for math import ceil

def main():
    capacity = 0
    r,rS,unSlots,pl,servers = readProblem()
    servers.sort()#sorted by cap/slot, size, capacity 
    sM=slotsArray(r,rS,unSlots)#available slots Matrix
    bCrs=measures(r,rS,servers, unSlots,sM)#best case (average) capacity per row's slot
    scl=grouping(0,servers)#creates a dictionary of servers grouped/clustered by their size
    print(scl)
    
    finInList=[]
    for k in range(len(sM)):#k: rows of sM
        for bl in sM[k]:#each block in this row
            size=bl[1]-bl[0]#block's size
            if size > 5:
                while(size > 5):
                    for i in range(5,0,-1):
                        if scl.get(i) != []:
                            size -= i
                            serv = findbestserv(bCrs[k],scl,i)
                            if serv == None:
                                continue
                            else:
                                capacity += serv[2]
                            scl[serv[0]].remove(serv)
                            servers.remove(serv)
                            finInList.append([serv[3],k,bl[0],0])
                            bl[0] += i
            else:
                for i in range(5,0,-1):
                        if scl.get(i) != []:
                            size -= i
                            serv = findbestserv(bCrs[k],scl,i)
                            if serv == None:
                                continue
                            else:
                                capacity += serv[2]
                            scl[serv[0]].remove(serv)
                            servers.remove(serv)
                            finInList.append([serv[3],k,bl[0],0])
                            bl[0] += i
    print(capacity)
    makeOutF( finInList, servers)
    
def measures(r,rS,servers, unSlots,sM):
    total_size = r*rS-len(unSlots) #real total size = all slots - unavailable slots
    currSize=0 #currentSize
    best_cap=0 #best case total capacity
    
    for s in servers:
        if currSize+s[1]>total_size:
            break
        currSize+=s[1]
        best_cap+=s[2]
    bCr=best_cap/r #best case (average) total capacity per row
    print(best_cap)
    return [ceil(bCr/i) for i in availSlotsR(rS,sM)] #best case (average) capacity per row's slot

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
            elif i<=sl:
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

def grouping(a,aList):
    
    if aList is None:
        return None
    
    aList.sort()
    aDict = dict()
    for el in aList:
        if el[a] in aDict:
            aDict[el[a]].append(el)
        else:
            aDict[el[a]]=[el]
    #print(size_serv_dict)
    return aDict

def findbestserv(bc,scl,size):
   
    flag=True#permits to switch while examining a pair of bigger smaller capacity. If flag==True,we 
             #examine first the next bigger capacity, else we examine first the next smaller capacity
    i=0
    keyL= list(scl.keys())
    bcInd=keyL.index(bc)
    s=None
    
    while(True):
        if i==0:
            tmpL=scl.get(bc)
            s=servProperSize(tmpL,size)
            if s!=None:
                break
            i+=1
        else:
            if flag:
                if bcInd+i<len(keyL):               
                    tmpL=scl.get(bcInd+i)
                    s=servProperSize(tmpL,size)
                    if s!=None:
                        break
                if bcInd-i>=0:
                    tmpL=scl.get(bcInd-i)
                    s=servProperSize(tmpL,size)
                    if s!=None:
                        break
                flag=False
            else:
                if bcInd-i>=0:                
                    tmpL=scl.get(bcInd-i)
                    s=servProperSize(tmpL,size)
                    if s!=None:
                        break
                if bcInd+i<len(keyL):
                    tmpL=scl.get(bcInd+i)
                    s=servProperSize(tmpL,size)
                    if s!=None:
                        break
                flag=True
            i+=1#There is not a server of the proper size having either the first next bigger or smaller capacity. 
                #we increase i to check the next pair of bigger/smaller capacity
            if bcInd-i<0 and bcInd+i>=len(keyL):
                break#there is no server that could fit in this gap
    return s

def servProperSize(tmpL,size):
    if tmpL!=None:
        for s in tmpL:
            if s[1]==size:
                return s
    return None

def makeOutF(inL,outL): 
    outfile=open("outfile.txt",'w')
    for el in inL:
        outfile.write("Server %d placed in row %d at slot %d and assigned to pool %d\r\n" %(el[0], el[1], el[2], el[3]) )
    for el in outL:
        outfile.write("Server %d not allocated \r\n" %(el[3]) )
    outfile.close()
    
def score(lines):
    sums = []
    for line in lines:
        sums.append(sum(line))
    return sum(sums) - max(sums)

main()