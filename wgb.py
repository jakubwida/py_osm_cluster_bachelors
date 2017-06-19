from py_osm_cluster.generator import trivial_gen as trivial_gen
import py_osm_cluster.visualisation.visualisation as visu
from py_osm_cluster.util.coords import Coords as C
import matplotlib.pyplot as plt

data_obj = trivial_gen.balanced_multiple_weighted_gauss_blobs(10.0,[0.5,2.0],50,5,[0.2,2.0])
visu.plot_coords_label_color(data_obj)
visu.plot_centers_by_label_color(data_obj)
plt.show()
