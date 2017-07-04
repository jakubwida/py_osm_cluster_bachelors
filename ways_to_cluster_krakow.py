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

parser = Parser("osm_data/krakow/wider_center.osm")

def visualise(data_obj,name):
	#plt.xlabel(name)
	visu.plot_coords_label_color(data_obj)
	visu.plot_centers_by_label_color(data_obj)
	plt.savefig(name+".png")
	plt.close()



buildings = parser.get_buildings_data_obj()
buildings.labels = [0 for i in buildings.coords]
buildings.c_number = 20
churches_coords =[]
for i in list(parser.ways.values()):
	if "building" in i.tags and i.tags["building"]=="church":
		churches_coords.append(list(i.geom.centroid.coords)[0])

restaurant_coords = []
for i in list(parser.nodes.values()):
	if "amenity" in i.tags and i.tags["amenity"]=="restaurant":
		restaurant_coords.append(list(i.geom.coords)[0])

pub_coords = []
for i in list(parser.nodes.values()):
	if "amenity" in i.tags and i.tags["amenity"]=="pub":
		pub_coords.append(list(i.geom.coords)[0])

hotel_coords = []
for i in list(parser.nodes.values()):
	if "tourism" in i.tags and i.tags["tourism"]=="hotel":
		hotel_coords.append(list(i.geom.coords)[0])

museum_coords = []
for i in list(parser.ways.values()):
	if "building:use" in i.tags and i.tags["building:use"]=="museum":
		museum_coords.append(list(i.geom.centroid.coords)[0])

data = {}
data["churches_coords"]=churches_coords
#data["restaurant_coords"]=restaurant_coords
data["pub_coords"]=pub_coords
data["hotel_coords"]=hotel_coords
data["museum_coords"]=museum_coords

def cluster_set(data_obj,centers,iterations,name):
	print(name)
	data_obj.labels = [0 for i in buildings.coords]
	clustering = deepcopy(data_obj)
	num = len(centers)
	print("A")
	#clustering.c_positions = [ trivial_gen.gauss_point(i,0.001) for i in centers]
	clustering.c_positions = centers
	clustering.c_number = num
	clustering = partitioning.k_means(clustering,initialisation="default_pos",iterations=iterations)
	visualise(clustering,name)

	print("B")
	comparison = deepcopy(data_obj)
	comparison.c_number = num
	comparison = partitioning.k_means(comparison,initialisation="kmeans_++",iterations=iterations)
	comparison.labes = [i+1 for i in clustering.labels]


	out ={}
	out["number"] = len(centers)
	out["comparison"] = comparative.scikit_all_scores_dict(clustering,comparison)
	out["default_pos"] = standalone.standard_scores_dict(clustering)
	out["kmeans_++"] = standalone.standard_scores_dict(comparison)
	return out

out ={}
#out["default_clustering_20"] = partitioning.k_means(deepcopy(buildings) ,initialisation="kmeans_++",iterations=20)
#out["church_clustering_20"] = cluster_set(buildings,churches_coords,20)
#out["pub_clustering_20"] = cluster_set(buildings,pub_coords,20)
#out["hotel_clustering_20"] = cluster_set(buildings,hotel_coords,20)
#out["museum_clustering_20"] = cluster_set(buildings,museum_coords,20)

for i in data:
	out[i] = cluster_set(buildings,data[i],20,i)




for i in out:
	print(i)
	for j in out[i]:
		print("  "+j)
		print("    "+str(out[i][j]))
