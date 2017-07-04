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

data = trivial_gen.balanced_multiple_gauss_blobs(10.0,2.0,20,5,0.75)
data = scikit.scikit_dbscan(data,max_dist=1.0)
visu.plot_coords_label_color(data)
plt.show()
