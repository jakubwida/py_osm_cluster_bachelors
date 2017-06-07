from py_osm_cluster.util.coords import Coords as C
from py_osm_cluster.generator import trivial_gen as trivial_gen
from copy import deepcopy
import math

from py_osm_cluster.parser.parser import Parser

from py_osm_cluster.cluster import scikit
from py_osm_cluster.cluster import partitioning

from py_osm_cluster.eval import comparative as Comp
from py_osm_cluster.eval import standalone as Std
from py_osm_cluster.cluster import hierarchical




"""
parser = Parser("map.osm")
coords = parser.get_buildings_data_obj()
coords.c_number=3
coords.c_positions=[trivial_gen.gauss_point((0.0,0.0),50) for i in range(3)]
"""

#coords = trivial_gen.balanced_multiple_gauss_blobs(10.0,3.0,20,5,0.5)
coords = trivial_gen.croissants(30,5.0,0.5)

newcoords = deepcopy(coords)
newcoords = hierarchical.agglomerative_single_link(newcoords,2)

#print(Std.statistics_distance_multi_cluster(newcoords))
#print(Std.triangulation_distance_within(newcoords.coords))

import py_osm_cluster.visualisation.visualisation as visu
import matplotlib.pyplot as plt
#visu.plot_coords(newcoords)

visu.plot_coords_label_color(newcoords)
visu.plot_centers_by_label_color(newcoords)
plt.show()
