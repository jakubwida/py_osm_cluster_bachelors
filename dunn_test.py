from py_osm_cluster.util.coords import Coords as C
from py_osm_cluster.generator import trivial_gen as trivial_gen
from py_osm_cluster.eval import standalone as standalone

import py_osm_cluster.visualisation.visualisation as visu
import py_osm_cluster.visualisation.animation as anim
import matplotlib.pyplot as plt

from py_osm_cluster.cluster import partitioning

data_obj = C()
for i in range(3):
	for j in range(3):
		data_obj.coords.append((float(i),float(j)))
		data_obj.labels.append(i)
data_obj.c_number = 3


data_2 = trivial_gen.multiple_gauss_blobs(10.0,20,5,0.5)
print(standalone.dunn_index(data_2))
visu.plot_coords_label_color(data_2)
plt.show()

data_2 = partitioning.k_means(data_2)
print(standalone.dunn_index(data_2))
visu.plot_coords_label_color(data_2)
plt.show()
