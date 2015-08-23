import argparse
from sapaths import SAPath
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='A small progy to visualize paths in gta sa!')
parser.add_argument('-n','--single-node', help='Site Id for the alert to be added on to', required=True)
parser.add_argument('-d','--nodes-directory', help='Alarm name', required=False)
args = vars(parser.parse_args())

node_file = args['single_node']

node = SAPath(node_file)
print(len(node.Paths()))
for i in node.Paths():
	print(i)
 

radius = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
area = [3.14159, 12.56636, 28.27431, 50.26544, 78.53975, 113.09724]
plt.plot(radius, area)
plt.show()

from matplotlib import mpl,pyplot
import numpy as np

# make values from -5 to 5, for this example
zvals = np.random.rand(100,100)*10-5

# make a color map of fixed colors
cmap = mpl.colors.ListedColormap(['blue','black','red'])
bounds=[-6,-2,2,6]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

# tell imshow about color map so that only set colors are used
img = pyplot.imshow(zvals,interpolation='nearest',
                    cmap = cmap,norm=norm)

# make a color bar
pyplot.colorbar(img,cmap=cmap,
                norm=norm,boundaries=bounds,ticks=[-5,0,5])

pyplot.show()
