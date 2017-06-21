from py_osm_cluster.util.coords import Coords as C
from copy import deepcopy

from py_osm_cluster.eval import standalone as standalone
from py_osm_cluster.generator import trivial_gen as trivial_gen
from py_osm_cluster.cluster import partitioning

import py_osm_cluster.visualisation.visualisation as visu
import matplotlib.pyplot as plt


def pront(data_obj,name):
	print("scikit_silhouette_score :"+str(standalone.scikit_silhouette_score(data_obj)))
	print("scikit_calinski_harabaz_score :"+str(standalone.scikit_calinski_harabaz_score(data_obj)))
	print("dunn_index :"+str(standalone.dunn_index(data_obj)))
	print(result_to_string(standalone.general_evaluate_clustered_object(data_obj)))
	visu.plot_coords_label_color(data_obj)
	visu.plot_centers_by_label_color(data_obj)
	plt.savefig(name+".png")
	plt.close()

def result_to_string(dictionary):
	out =""
	for key in dictionary:
		out = out + str(key) + "\n"
		for key_2 in dictionary[key]:
			out = out +"   " +str(key_2) + ": " + str(dictionary[key][key_2]) +"\n"
	return out

coords = trivial_gen.balanced_multiple_gauss_blobs(10.0,2.0,20,5,1.0)
pront(coords,"base")

print("!!!!!!!!!!!!!!!!!1")

newcoords = deepcopy(coords)
newcoords = partitioning.k_means(newcoords,initialisation="forgy")
pront(newcoords,"k_means")
