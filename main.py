import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from clusterization import Cluster, Point
import file

PATH_TO_DATA = 'data/bubble.csv'
CLUSTERS_PATH = 'data/clusters/cluster'
SIZES_PATH = 'data/sizes/cluster_size'
data = file.read(PATH_TO_DATA)


points = np.array(list(map(Point.reformat, data)))
cluster = Cluster('0', points)
first_clusters = cluster.spectre(2)
second_clusters = first_clusters[0].spectre(2)
third_clusters = first_clusters[1].spectre(2)

cluster_header = '| Nt | x | y | z | distances | differences |'
file.single_write(cluster.name, cluster.params(), CLUSTERS_PATH, cluster_header)
file.multy_write([cl.name for cl in first_clusters], [cl.params() for cl in first_clusters],
                 CLUSTERS_PATH, cluster_header)
file.multy_write([cl.name for cl in second_clusters], [cl.params() for cl in second_clusters],
                 CLUSTERS_PATH, cluster_header)
file.multy_write([cl.name for cl in third_clusters], [cl.params() for cl in third_clusters],
                 CLUSTERS_PATH, cluster_header)

size_header = '|x_center|y_center|z_center| R1 | R2 | R3 | '
file.multy_write([cl.name for cl in first_clusters], [[cl.expected_size()] for cl in first_clusters],
                 SIZES_PATH, size_header)
file.multy_write([cl.name for cl in second_clusters], [[cl.expected_size()] for cl in second_clusters],
                 SIZES_PATH, size_header)
file.multy_write([cl.name for cl in third_clusters], [[cl.expected_size()] for cl in third_clusters],
                 SIZES_PATH, size_header)


x = cluster.x
y = cluster.y
z = cluster.z

fig = plt.figure()
ax = Axes3D(fig)
ax.set_facecolor('gray')
ax.scatter(x, y, z, c='#7f22c7')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()


x0 = first_clusters[0].x
y0 = first_clusters[0].y
z0 = first_clusters[0].z

x1 = first_clusters[1].x
y1 = first_clusters[1].y
z1 = first_clusters[1].z

fig = plt.figure()
ax = Axes3D(fig)
ax.set_facecolor('gray')
ax.scatter(x0, y0, z0, c='#00705a')
ax.scatter(x1, y1, z1, c='#ad09a3')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()


x0 = second_clusters[0].x
y0 = second_clusters[0].y
z0 = second_clusters[0].z

x1 = second_clusters[1].x
y1 = second_clusters[1].y
z1 = second_clusters[1].z

x2 = third_clusters[0].x
y2 = third_clusters[0].y
z2 = third_clusters[0].z

x3 = third_clusters[1].x
y3 = third_clusters[1].y
z3 = third_clusters[1].z

fig = plt.figure()
ax = Axes3D(fig)
ax.set_facecolor('gray')
ax.scatter(x0, y0, z0, c='#00705a')
ax.scatter(x1, y1, z1, c='#ad09a3')
ax.scatter(x2, y2, z2, c='#0f56d9')
ax.scatter(x3, y3, z3, c='#9bab0c')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

fig = plt.figure()
ax = Axes3D(fig)
ax.set_facecolor('gray')
ax.scatter(x0, y0, z0, c='#00705a')
ax.scatter(x1, y1, z1, c='#ad09a3')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

fig = plt.figure()
ax = Axes3D(fig)
ax.set_facecolor('gray')
ax.scatter(x2, y2, z2, c='#0f56d9')
ax.scatter(x3, y3, z3, c='#9bab0c')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()







