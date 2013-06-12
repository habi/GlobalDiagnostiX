'''
Script to calculate the MTF from a real image.

Based on /afs/EssentialMed/Dev/MTF.py
'''
from pylab import *
import numpy as np
import scipy
import os

ion()

def MTF(edgespreadfunction):
    '''
    Compute the modulation transfer function (MTF).

    The MTF is defined as the FFT of the line spread function.
    The line spread function is defined as the derivative of the edge spread
    function. The edge spread function are the values along an edge, ideally a
    knife-edge test target. See an explanation here: http://is.gd/uSC5Ve
    '''
    linespreadfunction = np.diff(edgespreadfunction)
    return np.abs(np.fft.fft(linespreadfunction))
    

def LSF(edgespreadfunction):
    '''
    Compute the modulation transfer function (MTF).

    The MTF is defined as the FFT of the line spread function.
    The line spread function is defined as the derivative of the edge spread
    function. The edge spread function are the values along an edge, ideally a
    knife-edge test target. See an explanation here: http://is.gd/uSC5Ve
    '''
    return np.abs(np.diff(edgespreadfunction))


def rgb2gray(rgb):
    '''
    convert an image from rgb to grayscale
    http://stackoverflow.com/a/12201744/323100
    '''
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])    

ImagePath = '/afs/psi.ch/project/EssentialMed/Images'
ImageDir = '11-MTF'
ImageFile = 'iPhone_with_xray_film.jpg'
ImageFile = 'iPhone_with_xray_film_hdr.jpg'

ImageToLoad = os.path.join(ImagePath,ImageDir,ImageFile)

# Read the image and convert it to grayscale rightaway
ImageRGB = plt.imread(ImageToLoad)
Image = rgb2gray(ImageRGB)

ImageWidth = Image.shape[0]
ImageHeight = Image.shape[1]
print 'The image we loaded is', ImageWidth, 'by', ImageHeight,\
    'pixels big. That is', round(ImageWidth * ImageHeight/1e6,3), 'MPx.'

plt.subplot(221)
plt.imshow(Image,origin='lower',cmap=plt.gray())
PickPoint = ginput(1)
Horizon = int(PickPoint[0][1])
Vertigo = int(PickPoint[0][0])
print 'selected horizontal line', Horizon, 'and vertical line', Vertigo
plt.hlines(Horizon, 0, ImageHeight, 'r')
plt.vlines(Vertigo, 0, ImageWidth, 'b')
plt.draw()
plt.subplot(223)
HorizontalProfile = Image[Horizon,:]
plt.plot(HorizontalProfile,'r')
plt.title('Horizontal Profile')
plt.xlim(0,ImageHeight)
plt.ylim(0,256)
plt.subplot(222)
VerticalProfile = Image[:,Vertigo]
plt.plot(VerticalProfile,range(ImageWidth),'b')
plt.xlim(0,256)
plt.ylim(0,ImageWidth)
plt.title('Vertical Profile')
plt.draw()


print 'hello'
#~ if item in HorizontalProfile>100:
    #~ print item
    #~ 
#~ if item in VerticalProfile>100:
    #~ print item    


plt.show()
ioff()

exit()

plt.figure()
for i in range(3):
    plt.subplot(2, 4, i+1)
    plt.imshow(ImageRGB[:,:,i],origin='lower',cmap=plt.gray())
    plt.title(' '.join(['Channel', str(i)]))
    plt.subplot(2, 4, i+1+4)
    plt.imshow(ImageRGB[:,:,0]-Image[:,:,i],origin='lower',cmap=plt.gray())
    plt.title(' '.join(['Diff 0 &', str(i)]))
plt.subplot(244)
plt.imshow(ImageRGB,origin='lower')
plt.title('Original')
plt.subplot(248)
plt.imshow(rgb2gray(Image),origin='lower')
plt.title('rgb21gray(Original)')
plt.show()

#~ plt.imshow(Image,cmap="Greys_r")
#~ plt.show()

print ImageToLoad
exit()
