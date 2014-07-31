import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt



lenses = ['a', 'b', 'c']
modality = ['h', 'l', 'f']
exposuretime = [9,10,85]
distance = [10, 15, 23]
brightness = [15, 16, 17]

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(exposuretime, distance, brightness, 'o')
for lens, x, y, z in zip(lenses, exposuretime, distance, brightness):
    label = 'Lens: %s' % lens
    ax.text(x, y, z, label)
ax.set_xlabel('Exposure time')
ax.set_ylabel('Source Detector Distance')
ax.set_zlabel('Brightness')
ax.set_xlim([0,100])
ax.set_ylim([0,100])
ax.set_zlim([0,100])

plt.show()
