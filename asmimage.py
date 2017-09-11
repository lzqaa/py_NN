import os
import numpy
from collections import *
import pandas as pd
import binascii


def getMatrixfrom_bin(filename, width = 512, oneRow = False):
    with open(filename, 'rb') as f:
        content = f.read()
    hexst = binascii.hexlify(content)
    fh = numpy.array([int(hexst[i:i+2],16) for i in range(0, len(hexst), 2)])
    if oneRow is False:
        rn = len(fh)/width
        fh = numpy.reshape(fh[:rn*width],(-1,width))
    fh = numpy.uint8(fh)
    return fh

def getMatrixfrom_asm(filename, startindex = 0, pixnum = 5000):
    with open(filename, 'rb') as f:
        f.seek(startindex, 0)
        content = f.read(pixnum)
    hexst = binascii.hexlify(content)
    fh = numpy.array([int(hexst[i:i+2],16) for i in range(0, len(hexst), 2)])
    fh = numpy.uint8(fh)
    return fh

def getMatrixfrom_hex(filename, width):
    hexar = []
    with open(filename,'rb') as f:
        for line in f:
            hexar.extend(int(el,16) for el in line.split()[1:] if el != "??")
    rn = len(hexar)/width
    fh = numpy.reshape(hexar[:rn*width],(-1,width))
    fh = numpy.uint8(fh)
    return fh

def read_hexbytes(filename):
    hexar = []
    with open(filename,'rb') as f:
        for line in f:
            hexar.extend(int(el,16) for el in line.split()[1:] if el != "??")
    rn = len(hexar)/256
    fh = numpy.reshape(hexar[:rn*256],(-1,256))
    fh = numpy.uint8(fh)
    return fh

basepath = "/home/whp/moon/subtrain/"
mapimg = defaultdict(list)
subtrain = pd.read_csv('subtrainLabels.csv')
i = 0
for sid in subtrain.Id:
    i += 1
    print "dealing with {0}th file...".format(str(i))
    filename = basepath + sid + ".asm"
    im = getMatrixfrom_asm(filename, startindex = 0, pixnum = 1500)
    mapimg[sid] = im

dataframelist = []
for sid,imf in mapimg.iteritems():
    standard = {}
    standard["Id"] = sid
    for index,value in enumerate(imf):
        colName = "pix{0}".format(str(index))
        standard[colName] = value
    dataframelist.append(standard)

df = pd.DataFrame(dataframelist)
df.to_csv("imgfeature.csv",index=False)
