from py_osm_cluster.util.coords import Coords as Coords
from py_osm_cluster.generator import trivial_gen as trivial_gen
from copy import deepcopy
import math
import os
from py_osm_cluster.parser.parser import Parser

from py_osm_cluster.cluster import scikit
from py_osm_cluster.cluster import partitioning
import py_osm_cluster.util.statistic as statistic
from py_osm_cluster.eval import comparative as comparative
from py_osm_cluster.eval import standalone as standalone
from py_osm_cluster.cluster import hierarchical

import py_osm_cluster.visualisation.visualisation as visu
import py_osm_cluster.visualisation.animation as anim
import matplotlib.pyplot as plt

def remove_outliers(data_obj):
	to_remove =[]
	for num,i in enumerate(data_obj.labels):
		if i ==(-1):
			to_remove.append(num)
	to_remove.reverse()
	for i in to_remove:
		data_obj.coords.pop(i)
		data_obj.labels.pop(i)
	return data_obj


#fil ="osm_data/podhale/suche.osm"

def summarize_fileset(data):
	centroid_distance = []

	output = []
	for k in data:
		out = data[k]["centroid_and_their_points_distances"]["max"]
		out = out /data[k]["centroid_and_their_points_distances"]["avg"]
		output.append(out)
		if "centroid_distances" in data[k]:
			mout = data[k]["centroid_distances"]["max"]
			mout = mout/data[k]["centroid_distances"]["avg"]
			centroid_distance.append(mout)
		#stdev_centorid_distance.append(data[k]["centroid_and_their_points_distances"]["stdev"])


	#print(statistic.avg(between_centroid_distances))
	#print(statistic.avg(external_distances))
	#print(statistic.avg(max_centroid_distance))
	#print(statistic.avg(avg_centorid_distance))
	#print(statistic.avg(stdev_centorid_distance))
	#print(statistic.avg(dunn))
	print(statistic.avg(output))
	print(statistic.avg(centroid_distance))
def research_file(filename):
	parser = Parser(filename)

	data_obj=parser.get_buildings_by_address_nodes()
	data_obj.c_number=3
	data_obj.labels =[0 for i in data_obj.coords]
	#data_obj = partitioning.k_means(data_obj)
	data_obj =scikit.scikit_dbscan(data_obj,max_dist=0.0013)
	data_obj = remove_outliers(data_obj)
	#print(len(data_obj.labels))
	#print(len(data_obj.coords))
	#print(standalone.standard_scores_dict(data_obj))
	#print(standalone.general_evaluate_clustered_object(data_obj))
	#print(data_obj)
	#visu.plot_coords_label_color(data_obj)
	#plt.xlabel(filename)
	#plt.legend()
	#plt.show()
	out = {}
	out.update({"num":len(data_obj.coords)})
	out.update({"cluster_num":len(set(data_obj.labels))})
	out.update(standalone.general_evaluate_clustered_object(data_obj))
	if(len(set(data_obj.labels)))>1:
		out.update({"dunn_index":standalone.dunn_index(data_obj)})
	return out

#print(research_file(fil))


main = "osm_data/"
podhale = main+"podhale"

podhale_d ={}
for i in os.listdir(podhale):
	podhale_d[i] = research_file(podhale+"/"+i)
	#print(podhale_d[i])
podhale_out = open("podhale","w")
podhale_out.write(str(podhale_d))
summarize_fileset(podhale_d)
spisz = main+"spisz"
spisz_d ={}
for i in os.listdir(spisz):
	spisz_d[i] = research_file(spisz+"/"+i)
spisz_out = open("spisz","w")
spisz_out.write(str(spisz_d))
summarize_fileset(spisz_d)
