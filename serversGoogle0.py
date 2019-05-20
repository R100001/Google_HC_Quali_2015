# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 10:49:52 2019

@author: user
"""
import math

def main():
    r,rS,unSlots,pl,servers = readProblem()
    servers.sort()#sorted by cap/slot, size, capacity 
    sM=slotsArray(r,rS,unSlots)#available slots Matrix
    bCrs=measures(r,rS,servers, unSlots,sM)#best case (average) capacity per row's slot
    scl=grouping(0,servers)#creates a dictionary of servers grouped/clustered by their size
    
    finInList=[]
    for k in range(len(sM)):#k: rows of sM
        for bl in sM[k]:#each block in this row
            size=bl[1]-bl[0]#block's size
            serv=findbestserv(bCrs[k],scl,size)
            if serv==None:
                continue
            else:
                servers.remove(serv)
                finInList.append([serv[3],k,bl[0],0])
    
    makeOutF( finInList, servers)
    
def measures(r,rS,servers, unSlots,sM):
    total_size = r*rS-len(unSlots) #real total size = all slots - unavailable slots
    currSize=0 #currentSize
    best_cap=0 #best case total capacity
    
    for s in servers:
        if currSize+s[1]>total_size:
            break
        else:
            currSize+=s[1]
            best_cap+=s[2]
    bCr=best_cap/r #best case (average) total capacity per row
    avSr=availSlotsR(rS,sM)
    
    for i in range(len(avSr)):
        avSr[i]=math.ceil(bCr/avSr[i])
    return avSr #best case (average) capacity per row's slot
   
    
def cpSlot(l):#capacity per slot
    return l[1]/l[0]
    

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
            
            
def slotsArray(r, rS, unSlots):
    unSlots.sort()
    slotsMatrix = []
    j,k=0,0
    while(True):
        if j==r:
            break
        else:
            k,l = rowSlotBlocks(k, unSlots, rS, j)
            slotsMatrix.append(l)
            j+=1
    #print(slotsMatrix)
    return slotsMatrix
  
    
def rowSlotBlocks(k, unSlots, rS, j):
    availSlotsR=[]
    col=0
    for i in range(k, len(unSlots)):
        
        if j!=unSlots[k][0]:
            availSlotsR.append( [ 0, rS ] )
            break
        else:
            if unSlots[k][0]!=unSlots[i][0]:
                j=i-1
                fAvail=unSlots[j][1]+1
                availSlotsR.append( [ fAvail,rS ] )#last block of available slots (in this row, which is not the last row) is added
                break
            if unSlots[i][1]==col:
                    col+=1
                    continue
            else:#unSlots[i][1]!=col 
                if i==k:
                    fAvail=col
                else: #i!=k
                    fAvail=unSlots[i-1][1]+1
                    col=unSlots[i][1]+1
                availSlotsR.append( [ fAvail,unSlots[i][1] ] )
                if i==len(unSlots)-1 and unSlots[i][1]+1 !=rS :#last block of available slots (in the last row) is added if the last unavailable slot is not the 16 100
                     availSlotsR.append( [ unSlots[i][1]+1, rS ] )
    return i, availSlotsR
   


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
      

#we can not find that capacity for this size 
    
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
        outfile.write("Server %d placed in row %d at slot %d and assigned to pool %d\r\n" %(el) )
    for el in outL:
        outfile.write("Server %d not allocated %\r\n" %(el[3]) )
    outfile.close()
	
def score(lines):
    sums = []
    for line in lines:
        sums.append(sum(line))
    return sum(sums) - max(sums)


main()
