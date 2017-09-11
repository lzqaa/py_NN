import os
from random import *
import pandas as pd
import shutil

rs = Random()
rs.seed(1)

trainlabels = pd.read_csv('trainLabels.csv')
fids = []

opd = pd.DataFrame()
for clabel in range (1,10):
    mids = trainlabels[trainlabels.Class == clabel]
    mids = mids.reset_index(drop=True)

    rchoice = [rs.randint(0,len(mids)-1) for i in range(100)]
    print rchoice   
    
#     for i in rchoice:
#         fids.append(mids.loc[i].Id)
#         opd = opd.append(mids.loc[i])

    rids = [mids.loc[i].Id for i in rchoice]
    fids.extend(rids)
    opd = opd.append(mids.loc[rchoice])
    

print len(fids)
opd = opd.reset_index(drop=True)
print opd
opd.to_csv('subtrainLabels.csv', encoding='utf-8', index=False)

sbase = '/home/whp/moon/MalwareClassification/'  #/home/whp/moon/MalwareClassification
tbase = '/home/whp/moon/MalwareClassification/'

for fid in fids:
	fnames = ['{0}.asm'.format(fid),'{0}.bytes'.format(fid)]
	for fname in fnames:
		cspath = sbase + fname
		ctpath = tbase + fname
		shutil.copy(cspath,ctpath)
