from py_osm_cluster.util.coords import Coords as Coords
from py_osm_cluster.generator import trivial_gen as trivial_gen
from copy import deepcopy
import math
import os
from py_osm_cluster.parser.parser import Parser

from py_osm_cluster.cluster import scikit
from py_osm_cluster.cluster import partitioning

from py_osm_cluster.eval import comparative as comparative
from py_osm_cluster.eval import standalone as standalone
from py_osm_cluster.cluster import hierarchical

import py_osm_cluster.visualisation.visualisation as visu
import py_osm_cluster.visualisation.animation as anim
import matplotlib.pyplot as plt

parser = Parser("osm_data/near_krakow/wegrzce_bibice.osm")

churches = Coords()
for i in list(parser.ways.values()):
	if "building" in i.tags and i.tags["building"]=="church":
		churches.coords.append(list(i.geom.centroid.coords)[0])
churches.labels = [1 for i in churches.coords]

data = parser.get_buildings_data_obj()
data.c_number = 10
data.labels =[0 for i in data.coords]
data = partitioning.k_means(data,initialisation="kmeans_++",iterations=25)

print(data)
visu.plot_coords_label_color(data)
visu.plot_coords_label_color(churches)
plt.show()
