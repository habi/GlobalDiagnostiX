'''
Script to visualize the "Noise vs. Exposure" data from DevWare
'''

import os
import numpy
import matplotlib.pyplot as plt

Root = '/afs/psi.ch/project/EssentialMed/Images/NoiseVsExposure'
Files = [
    'AR0130_Navitar_10_100_3_16.txt',
    'AR0130_Navitar_10_500_3_16.txt',
    'AR0130_Navitar_20_200_3_12.txt',
    'AR0130_Navitar_20_200_4_16.txt',
    'AR0130_Navitar_20_200_6_16.txt',
    'AR0130_Navitar_20_500_5_16.txt',
    'AR0130_Navitar_50_100_1_10.txt'
    ]

Labels = ['Exposure time [ms]',
    'Signal',
    'RMS Dyn',
    'Avg Dyn',
    'FPN',
    'Col FPN',
    'Row FPN',
    'Col Dyn',
    'Row Dyn']

for counter,item in enumerate(Files):
    print 'Working on', item

    File = os.path.join(Root, item)
    Data = numpy.loadtxt(File, skiprows=3)

    FigureTitle = item[:-4].split('_')
    Title = FigureTitle[0], FigureTitle[1], FigureTitle[2], \
        'frames', FigureTitle[3], 'ms max exposure', FigureTitle[4], \
        'Decades', FigureTitle[5], 'Samples/Decade'

    # The title of the plot is split over all the suplots, othewise it destroys
    # the layout due to the long length

    plt.figure(' '.join(Title), figsize=(16,9))
    # Signal
    plt.subplot(131)
    plt.plot(Data[:,0], Data[:,1])
    plt.xlabel(Labels[0])
    plt.ylabel(Labels[1])
    plt.title(' '.join(Title[:2]))

    # FPN
    plt.subplot(132)
    for i in range(4,7):
        plt.plot(Data[:,0], Data[:,i], label=Labels[i])
    plt.xlabel(Labels[0])
    plt.ylabel('FPN')
    plt.title(' '.join(Title[2:6]))
    plt.legend(loc='best')

    # DYN
    plt.subplot(133)
    for i in [2,3,7,8]:
        plt.plot(Data[:,0], Data[:,i], label=Labels[i])
    plt.legend(loc='best')
    plt.xlabel(Labels[0])
    plt.ylabel('Dyn')
    plt.title(' '.join(Title[6:]))
    plt.tight_layout()
    plt.savefig(os.path.join(Root,item[:-4] + '.png'), Transparent=True,
         bbox_inches='tight')
    plt.draw()
plt.show()
