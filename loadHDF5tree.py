###
### This macro reads the neural network outputs of the optical scan.
### Files are stored in HDF5 format, details are in ALICE3.recipe
### Plots maps, distribution of area, diameter, ellipse axises, etc
###

import numpy as np
import h5py
from ROOT import *
import tables 
import os
import glob

from root_numpy import root2array, tree2array
from root_numpy import array2tree, array2root
from root_numpy.testdata import get_filepath

"""
Convert dictionary to names numpy array
which will be converted into a TTree
(names are according to ALICE3.recipe,
with whitespaces replaced by "_")
"""
def convert_dict_nparray(dictionary, key):
    while dictionary.has_key(key):
        try:
            # print 'processing <<', key, '>> out of ', dictionary.keys()

            # convert np.ndarray (2D) into a list of tuples
            tmp_array = list()
            for line in dictionary[key]:
                line = tuple(line)
                tmp_array.append( line )
            
            # create a named list which will be directly
            # converted to a TTree object
            my_array = np.array( tmp_array, 
                    dtype=[('x',np.float64),
                        ('y',np.float64),
                        ('bb_x',np.float64),
                        ('bb_y',np.float64),
                        ('bb_width',np.float64),
                        ('bb_height',np.float64),
                        ('area',np.float64),
                        ('diameter',np.float64),
                        ('perimColour_B',np.float64),
                        ('perimColour_G',np.float64),
                        ('perimColour_R',np.float64),
                        ('ellipse_angle',np.float64),
                        ('moment_1',np.float64),
                        ('moment_2',np.float64),
                        ('moment_3',np.float64),
                        ('moment_4',np.float64),
                        ('moment_5',np.float64),
                        ('moment_6',np.float64),
                        ('ellipse_big_axis',np.float64),
                        ('ellipse_small_axis',np.float64),
                        ('bb_Colour_B',np.float64),
                        ('bb_Colour_G',np.float64),
                        ('bb_Colour_R',np.float64),
                        ('bool_0=background_1=foreground',np.bool)] )
            return my_array
        except:
            print 'not valid key'
            return -1


"""
Load HDF5 files into dictionary
"""
def load_HDF5file_dict(infilename):
    h5file = tables.open_file(infilename, mode='r')
    data={} 
    for idx,  group in enumerate(h5file.walk_groups()):
        if idx>0:
            flavour=group._v_name
            data[flavour]=group.data.read()
    h5file.close()
    return data


"""
M A I N   P R O G R A M
"""

# Creating empty container for data (the ugly way)
data_array = np.array( [(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)],
                    dtype=[('x',np.float64),
                        ('y',np.float64),
                        ('bb_x',np.float64),
                        ('bb_y',np.float64),
                        ('bb_width',np.float64),
                        ('bb_height',np.float64),
                        ('area',np.float64),
                        ('diameter',np.float64),
                        ('perimColour_B',np.float64),
                        ('perimColour_G',np.float64),
                        ('perimColour_R',np.float64),
                        ('ellipse_angle',np.float64),
                        ('moment_1',np.float64),
                        ('moment_2',np.float64),
                        ('moment_3',np.float64),
                        ('moment_4',np.float64),
                        ('moment_5',np.float64),
                        ('moment_6',np.float64),
                        ('ellipse_big_axis',np.float64),
                        ('ellipse_small_axis',np.float64),
                        ('bb_Colour_B',np.float64),
                        ('bb_Colour_G',np.float64),
                        ('bb_Colour_R',np.float64),
                        ('bool_0=background_1=foreground',np.bool)] )

# Loop over the chunks
print '========================='
ifile = 0
for ifilename in glob.iglob('./data2/*.h5'):
#for ifilename in glob.iglob('./data2/Test_Image_objectdata_1_chunk-5-2.h5'):
    print 'load file:', ifile,'/',len(glob.glob('./data2/*.h5')), ':', ifilename
    # load HDF5 into a python dictionary
    data_dict = load_HDF5file_dict(ifilename)
    # convert that to named (structured) numpy array
    data_array_tmp = convert_dict_nparray(data_dict, 'inner')
    # merge that with the empty container defined outside of the loop
    data_array = np.concatenate( (data_array_tmp, data_array), axis=0 ) 
    ifile += 1
print '========================='

# create a tree from the array
print '\ncreate a tree from the array'
tree = array2tree(data_array, name='inner_tree')

# merge the trees (takes some time)
#tree = TTree.MergeTrees( tlist )

print 'writing file'
outFile = TFile('outfile.root', 'RECREATE')
outFile.cd()
tree.Write()
outFile.Write()
outFile.Close()

