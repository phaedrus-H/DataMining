# -*- coding: utf-8 -*-
"""
Created on Sat Sep 10 21:12:50 2016

@author: harshad
"""
#%%
#Input for MSApriori
from collections import OrderedDict

T = [['20','30','80','70','50','90'],['20','10','80','70'],['10','20','80'],['20','30','80'],['20','80'],['20','30','80','70','50','90','100','120','140']]
MS = {'10':0.43, '20':0.30, '30':0.30, '40':0.40, '50':0.40, '60':0.30, '70':0.20, '80':0.20, '90':0.20, '100':0.10, '120':0.20, '140':0.15}
SDC = 0.1

#%%
#Find list of items and sort them based on MIS values
I = list(MS.keys())
M = list(OrderedDict(sorted(MS.items(), key = lambda x : x[1])))

Tcount = len(T)
Icount = len(I)
Mcount = len(M)

#%%
#L <- initPass(M,T)

#Step 1 - Construct support dictionary
supportList = []
for icounter in range(Icount):
    counter = 0
    for tcounter in range(Tcount):
        counter += T[tcounter].count(I[icounter])
    supportList.append((I[icounter],format(counter/Tcount, '.2f')))

SupportDict = dict(supportList)

#Step 2 Calculate L
L = []
pivot = 0
for mcounter in range(Mcount):
    if MS[M[mcounter]] < float(SupportDict[M[mcounter]]):
        L.append(M[mcounter])
        pivot = mcounter
        break

for mcounter in range(pivot+1, Mcount):
    if MS[M[pivot]] < float(SupportDict[M[mcounter]]):
        L.append(M[mcounter])

Lcount = len(L)
#%%
#Calculate F1
F = []
F1 = []
for lcounter in range(Lcount):
    if float(SupportDict[L[lcounter]]) >= MS[L[lcounter]]:
        F1.append([L[lcounter]])
F.append(F1)
print(F)

#%%
#Calculate F(2-k)
k=1
C = []
while(True):
    
    if k > len(F):
        break
    if k==1:
        Ctemp = []
        for lcounter in range(Lcount):
            if float(SupportDict[L[lcounter]]) >= MS[L[lcounter]]:
                for hcounter in range(lcounter+1,Lcount):
                    cond1 = float(SupportDict[L[hcounter]]) >= MS[L[lcounter]]
                    cond2 = (abs(float(SupportDict[L[hcounter]]) - float(SupportDict[L[lcounter]])) <= SDC)
                    if cond1 & cond2:
                        Ctemp.append([L[lcounter],L[hcounter]])
        C.append(Ctemp)
        print(C[k-1])
    else:
        Ctemp = []
        #code for MSCandidateGen
        C.append(Ctemp)
    
    Ftemp = []
    candidatecounter = 0
    candidatedict = {}
    candidatetaildict = {}
    for tcounter in range(Tcount):  
        t = T[tcounter]
        for ccounter in range(len(C[k-1])):
            c = C[k-1][ccounter]
            if set(c).issubset(set(t)):
                if not tuple(c) in candidatedict:
                    candidatedict[tuple(c)] = 1
                else:
                    candidatedict[tuple(c)] += 1
            ctail = list(c)
            ctail.pop(0)
            if set(ctail).issubset(set(t)):
                if not tuple(ctail) in candidatetaildict:
                    candidatetaildict[tuple(ctail)] = 1
                else:
                    candidatetaildict[tuple(ctail)] += 1
    for candidate in candidatedict.keys():
        if candidatedict[candidate]/Tcount >= MS[candidate[0]]:
            Ftemp.append(candidate)
    print(Ftemp)
    print(candidatedict)
    print(candidatetaildict)
    k = k + 1
print(F)
#%%    