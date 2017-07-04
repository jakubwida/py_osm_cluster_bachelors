from py_osm_cluster.util.coords import Coords as Coords
from py_osm_cluster.generator import trivial_gen as trivial_gen
from copy import deepcopy
import math

from py_osm_cluster.parser.parser import Parser

from py_osm_cluster.cluster import scikit
from py_osm_cluster.cluster import partitioning

from py_osm_cluster.eval import comparative as comparative
from py_osm_cluster.eval import standalone as standalone
from py_osm_cluster.cluster import hierarchical

import py_osm_cluster.visualisation.visualisation as visu
import py_osm_cluster.visualisation.animation as anim
import matplotlib.pyplot as plt


parser = Parser("osm_data/krakow/krakow_center.osm")




all_buildings = parser.get_buildings_data_obj()
all_buildings.labels = [0 for i in all_buildings.coords]
churches = Coords()

for i in list(parser.ways.values()):
	if "building" in i.tags and i.tags["building"]=="church":
		churches.coords.append(list(i.geom.centroid.coords)[0])
churches.labels = [1 for i in churches.coords]

#print(churches)
#print(all_buildings)
all_buildings.c_number = len(churches.coords)

all_buildings.c_positions = churches.coords
all_buildings = partitioning.k_means(all_buildings,iterations=1,initialisation="default_pos")
print(all_buildings)
#all_buildings = partitioning.k_means(all_buildings,iterations=20,initialisation="kmeans_++")
#all_buildings = hierarchical.agglomerative(all_buildings,linkage="c-link")

visu.plot_coords_label_color(all_buildings)
visu.plot_coords_label_color(churches)
plt.show()
