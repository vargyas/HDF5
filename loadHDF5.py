###
### This macro reads the neural network outputs of the optical scan.
### Files are stored in HDF5 format, details are in ALICE3.recipe
### Plots maps and occurence plots of various parameters, e.g
### hole area, diameter, ellipse axises, etc
###

import glob
import math
import numpy as np
import h5py
from ROOT import *
import tables 
import os
from mplot import MPlot

"""
Function to load HDF5 files into numpy array
"""
def load_HDF5file(infilename):
    h5file = tables.open_file(infilename, mode='r')
    data={} 
    for idx,  group in enumerate(h5file.walk_groups()):
        if idx>0:
            flavour=group._v_name
            data[flavour]=group.data.read()
            #print data[flavour].shape
    h5file.close()
    return data

"""
Load all HDF5 files of one image
"""
xval  = [np.empty(0),np.empty(0)]
yval  = [np.empty(0),np.empty(0)]
diam  = [np.empty(0),np.empty(0)]
ndata = [0,0]

for ifile in glob.iglob('./data2/*.h5'):
    print 'processing: ', ifile
    data = load_HDF5file(ifile)
    idict_index=0
    for idict in ('inner','outer'):
        xtemp = np.array(data[idict][:,0])
        ytemp = np.array(data[idict][:,1])
        dtemp = np.array(data[idict][:,7])
        xval[idict_index]  = np.hstack( (xval[idict_index],xtemp) )
        yval[idict_index]  = np.hstack( (yval[idict_index],ytemp) )
        diam[idict_index]  = np.hstack( (diam[idict_index],dtemp) )
        ndata[idict_index] += data[idict].shape[0]
        print ndata[idict_index]
        idict_index += 1
    print "================================"

"""
Prepare and plot results
"""
print '\n\n', 'starting plotting\n\n'

xmin=[]; xmax=[]; ymin=[]; ymax=[]
cDM=[]; cDO=[]; hDiaMap=[]; hDiaOcc=[]; 
for i in (0,1): #idict_index
    xmin.append( xval[i].min() )
    ymin.append( yval[i].min() )
    xmax.append( xval[i].max() )
    ymax.append( yval[i].max() )

    hDiaMap.append( TH2D("hDiameterMap{}".format(i),"",1000,xmin[i],xmax[i],1000,ymin[i],ymax[i]) )
    hDiaOcc.append( TH1D("hDiameterOccurence{}".format(i),"",1000,0,100) )

    for ib in range(ndata[i]):
        ibin=hDiaMap[i].FindBin( xval[i][ib], yval[i][ib] )
        hDiaMap[i].SetBinContent( ibin, diam[i][ib]*4.42 )
        hDiaOcc[i].Fill( diam[i][ib]*4.42 )

    # draw diameter map
    cDM.append( TCanvas("cDM{}".format(i),"cDia",600,600) )
    cDM[i].Draw()
    gStyle.SetOptStat(0)
    hDiaMap[i].Rebin2D(10,10) #median should be used instead of mean
    hDiaMap[i].Scale(1./100.)
    hDiaMap[i].GetXaxis().SetTitle('x')
    hDiaMap[i].GetYaxis().SetTitle('y')
    hDiaMap[i].GetZaxis().SetTitle('d [#mum]')
    hDiaMap[i].Draw('colz')
    # draw diameter occurence
    cDO.append( TCanvas("cDO{}".format(i),"cDia",600,600) )
    cDO[i].Draw()
    hDiaOcc[i].Draw()

#create a graph just to check the grid
#gMap = TGraph(ndata,np.array(xval),np.array(yval))
#gMap.SetMarkerStyle(7)
#gMap.Draw('AP')
"""
def rebinH(h, nx, ny):
    for ix in range(nx):

        for iy in range(ny):
"""




"""
hDia = []
hDia.append( TH1D("hDiaInner","",1000,50,100) )
hDia.append( TH1D("hDiaOuter","",1000,50,100) )
hArea = []
hArea.append( TH1D("hAreaInner","",1000,0,100) )
hArea.append( TH1D("hAreaOuter","",1000,0,100) )

for i in range(data['inner'].shape[0]):
    hDia[0].Fill(data['inner'][i][7] * 4.42) # convert pixel to micrometer
    hArea[0].Fill(data['inner'][i][6])
for i in range(data['outer'].shape[0]):
    hDia[1].Fill(data['outer'][i][7] * 4.42) # convert pixel to micrometer
    hArea[1].Fill(data['outer'][i][6])

"""
"""
Plot diameter distribution
"""
#mdia = MPlot(0,'diameter [#mum]','occurence',False)
#hList   = [hDia[0], hDia[1]]
#legList = ['inner','outer']
#mdia.AddHlist(hList, legList, 'pe','p')
#mdia.Draw()

"""
Plot area distribution
"""
#marea = MPlot(1,'area [?]','occurence',False)
#hList   = [hArea[0],hArea[1]]
#marea.AddHlist(hList, legList, 'pe','p')
#marea.Draw()

"""
Plot ellipse angle 
"""

wait = input("PRESS ENTER TO CONTINUE.")



