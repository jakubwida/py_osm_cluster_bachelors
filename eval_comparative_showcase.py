from py_osm_cluster.util.coords import Coords as C
from copy import deepcopy

from py_osm_cluster.eval import comparative as Comp

import py_osm_cluster.visualisation.visualisation as visu
import matplotlib.pyplot as plt

def save(data_obj,name):
	visu.plot_coords_label_color(data_obj)
	plt.xlim((-0.5,2.5))
	plt.ylim((-0.5,2.5))
	plt.savefig(name+".png")

data_obj = C()
for i in range(3):
	for j in range(3):
		data_obj.coords.append((float(i),float(j)))
		data_obj.labels.append(i)
data_obj.c_number = 3


print("data_obj")
print(Comp.scikit_all_scores_dict(data_obj,data_obj))
save(data_obj,"data_obj")


one_cluster = deepcopy(data_obj)
one_cluster.labels = [0,0,0,0,0,0,0,0,0]
print("one_cluster")
print(Comp.scikit_all_scores_dict(one_cluster,data_obj))
save(one_cluster,"one_cluster")


cross_wrong = deepcopy(data_obj)
cross_wrong.labels = [0,1,2,0,1,2,0,1,2]
print("cross_wrong")
print(Comp.scikit_all_scores_dict(cross_wrong,data_obj))
save(cross_wrong,"cross_wrong")


many_clusters = deepcopy(data_obj)
many_clusters.labels = [0,1,2,3,4,5,6,7,8]
print("many_clusters")
print(Comp.scikit_all_scores_dict(many_clusters,data_obj))
save(many_clusters,"many_clusters")


###
#need to add evaluation
