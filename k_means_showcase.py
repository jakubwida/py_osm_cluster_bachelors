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
from py_osm_cluster.eval import summary as summary
from py_osm_cluster.cluster import hierarchical
from py_osm_cluster.util import statistic

import py_osm_cluster.visualisation.visualisation as visu
import py_osm_cluster.visualisation.animation as anim
import matplotlib.pyplot as plt

from copy import deepcopy

def generate_test_datasets():
	location = "k_means_data"
	for i in ["balanced_gauss","big_gauss","difficult_gauss","scars","different_sizes"]:
		if not os.path.exists(location+"/"+i):
			os.makedirs(location+"/"+i)

	#simple gauss
	for i in range(10):
		data_obj = trivial_gen.balanced_multiple_gauss_blobs(10.0,2.0,20,5,0.5)
		data_obj.write_file(location+"/balanced_gauss/data"+str(i))
	#big_gauss
	for i in range(10):
		data_obj = trivial_gen.balanced_multiple_gauss_blobs(10.0,2.0,100,5,0.5)
		data_obj.write_file(location+"/big_gauss/data"+str(i))
	#difficult_gauss
	for i in range(10):
		data_obj = trivial_gen.balanced_multiple_gauss_blobs(10.0,2.0,20,5,0.75)
		data_obj.write_file(location+"/difficult_gauss/data"+str(i))

	#scars
	for i in range(10):
		data_obj = trivial_gen.balanced_multiple_weighted_gauss_blobs(10.0,[1.0,0.5],20,5,[0.75,0.25])
		data_obj.write_file(location+"/scars/data"+str(i))
	#different_sizes
	for i in range(10):
		data_obj = trivial_gen.balanced_random_size_gauss_blobs(10.0,2.0,2,100,5,0.5)
		data_obj.write_file(location+"/different_sizes/data"+str(i))

	#used for testing
def showfiles():
	for i in ["balanced_gauss","big_gauss","difficult_gauss","scars","different_sizes"]:
		for j in range(10):
			data_obj = Coords()
			data_obj.read_file("k_means_data"+"/"+i+"/data"+str(j))
			visu.plot_coords_label_color(data_obj)
			visu.plot_centers_by_label_color(data_obj)
			plt.show()

#generate_test_datasets()
#showfiles()
n =0;

def _screenshot(data_obj):
	global n
	visu.plot_coords_label_color(data_obj)
	visu.plot_centers_by_label_color(data_obj)
	n+=1
	plt.savefig("kmeans_frame_"+str(n)+".png")
	plt.close()



def sample_process():
	data_obj = trivial_gen.balanced_multiple_gauss_blobs(5.0,2.0,10,2,0.6)
	_screenshot(data_obj)
	partitioning.k_means(data_obj,iterations=3,on_step=_screenshot)
	#visu.plot_coords_label_color(data_obj)
	#visu.plot_centers_by_label_color(data_obj)
	#plt.show()
#sample_process()


gt = summary.GeneralTest()
#print(gt.test_data_object("k_means_data/balanced_gauss/data0",5,partitioning.k_means,{}))
#gt.execute("k_means_data/balanced_gauss")

#summary.test_multiple_datasets("k_means_data",30,partitioning.k_means,{"iterations":15})
"""
indexes =[]
for k in range(100):
	data_obj = trivial_gen.balanced_multiple_gauss_blobs(10.0,2.0,20,5,1.0)
	index = []
	def harvest_index(input_obj):
		global data_obj
		index.append(comparative.scikit_rand_index(input_obj,data_obj))
	new_obj = deepcopy(data_obj)
	new_obj = partitioning.k_means(new_obj,on_step=harvest_index)
	indexes.append(index)
indexes = list(zip(*indexes))
indexes = [statistic.avg(i) for i in indexes ]
visu.lineplot(indexes,"what")
plt.show()
"""

def test_on_random_sized():
	data_obj = trivial_gen.balanced_random_size_gauss_blobs(10.0,2.0,5,100,5,0.5)
	data_obj = partitioning.k_means(data_obj)
	visu.plot_coords_label_color(data_obj)
	visu.plot_centers_by_label_color(data_obj)
	plt.show()
#test_on_random_sized()

#rand_test_data = trivial_gen.balanced_multiple_gauss_blobs(10.0,2.0,20,5,0.5)

#visu.plot_coords_label_color(rand_test_data)
#plt.show()
def test_rand_indexes_on_single_data(rand_test_data,initialisation,marker):
	rand_indexes =[]
	for i in range(100):
		data_obj = deepcopy(rand_test_data)
		uncaught = True
		while uncaught:
			try:
				data_obj = partitioning.k_means(data_obj,initialisation = initialisation,iterations=10)
				rand_indexes.append(comparative.scikit_rand_index(data_obj,rand_test_data))
				uncaught = False
			except ZeroDivisionError:
				uncaught =True
	rand_indexes.sort()
	plt.plot(list(range(100)),rand_indexes,marker,label=initialisation)


def test_init_methods():
	rand_test_data = trivial_gen.balanced_random_size_gauss_blobs(10.0,2.0,2,100,5,0.5)
	test_rand_indexes_on_single_data(rand_test_data,"forgy","r-")
	test_rand_indexes_on_single_data(rand_test_data,"random_partitions","b-")
	test_rand_indexes_on_single_data(rand_test_data,"kmeans_++","g-")
	plt.legend(loc="lower right")
	plt.ylabel("Rand index value")
	plt.show()
	plt.savefig("initialisations.png")

def croissants():
	data =trivial_gen.croissants(100,5.0,0.5)
	visu.plot_coords_label_color(data)
	visu.plot_centers_by_label_color(data)
	plt.show()
	data =partitioning.k_means(data,initialisation="kmeans_++")
	visu.plot_coords_label_color(data)
	visu.plot_centers_by_label_color(data)
	plt.show()
croissants()
