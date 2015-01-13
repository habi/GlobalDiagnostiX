# -*- coding: utf-8 -*-

"""
This script reads the RAW files from the Aptina cameras as numpy arrays,
ready for display or further use.
Made to help Valerie Duay get up to speed :)
"""
import os
import numpy
import matplotlib.pyplot as plt

Directory = '/scratch/tmp/DevWareX/MT9M001/DSL949A-NIR/'
Folder = '1394629994_MT9M001_DSL949A-NIR_0.0_0.0f_040ms_090mm_to150mm'
File = 'MT9M001_1280x1024_DSL949A-NIR_0.0_0.0f_040ms_090mm_to150mm_090mm.raw'
Size = [int(File.split('_')[1].split('x')[1]),
        int(File.split('_')[1].split('x')[0])]

# fromfile
FileToLoad = os.path.join(Directory, Folder, File)

FromFile = numpy.fromfile(FileToLoad, dtype=numpy.uint16).reshape(Size)
#~ FromFile -= numpy.mean(FromFile)

MemMap = numpy.memmap(FileToLoad, dtype=numpy.uint16, shape=(Size[0], Size[1]))
#~ MemMap -= numpy.mean(MemMap)

plt.figure(File)
plt.subplot(121)
plt.imshow(FromFile, cmap='gray')
plt.title('numpy.fromfile > leaves file')
plt.subplot(122)
plt.imshow(MemMap, cmap='gray')
plt.title('numpy.memmap > destroys file')
plt.show()

print 'Only use "numpy.memmap" for displaying files! If you perform some',\
    'calculations on the files (e.g "File -= numpy.mean(File)") these',\
    'calculations are immediately saved to disk, essentially destroying the',\
    'file! In this case use "numpy.fromfile"!'
