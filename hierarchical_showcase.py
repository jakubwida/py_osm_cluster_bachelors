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

def simple_demo():
	data_obj = trivial_gen.croissants(100,5.0,0.5)
	data_obj = hierarchical.agglomerative(data_obj,linkage="c-link")
	visu.plot_coords_label_color(data_obj)
	plt.show()
#simple_demo()


def _save_iteration_picture(data_obj):
	visu.plot_coords_label_color(data_obj)
	global iteration
	plt.savefig("hierarchical_"+str(iteration))
	iteration +=1
	plt.close()
iteration = 1
def demonstration():

	data_obj = trivial_gen.balanced_multiple_gauss_blobs(10.0,2.0,5,5,0.5)
	data_obj = hierarchical.agglomerative(data_obj,linkage="s-link",on_step=_save_iteration_picture)

#demonstration()

def general_summary():
	avg_rand_s_link={}
	avg_rand_c_link ={}
	stdev_rand_s_link={}
	stdev_rand_c_link ={}
	folders = list(os.listdir("k_means_data"))
	#print(folders)
	for i in folders:
		#if i !="B":
		data_files = list(os.listdir("k_means_data/"+i))
		rand_s_link =[]
		rand_c_link =[]
		for j in data_files:
			j = "k_means_data/"+i+"/"+j
			data_obj = Coords()
			data_obj.read_file(j)
			newdata = deepcopy(data_obj)
			newdata = hierarchical.agglomerative(newdata)
			rand_s_link.append(comparative.scikit_rand_index(newdata,data_obj))
			newdata = deepcopy(data_obj)
			newdata = hierarchical.agglomerative(newdata,linkage="c-link")
			rand_c_link.append(comparative.scikit_rand_index(newdata,data_obj))
			print("researching: "+j+" in:"+i)
		stdev_avg_c = statistic.stdev_avg(rand_c_link)
		stdev_avg_s = statistic.stdev_avg(rand_s_link)
		i =str(i)
		avg_rand_c_link[i]=stdev_avg_c[1]
		avg_rand_s_link[i]=stdev_avg_s[1]
		stdev_rand_c_link[i]=stdev_avg_c[0]
		stdev_rand_s_link[i]=stdev_avg_s[0]
	abcde =  ["A","B","C","D","E"]
	nums =[0,1,2,3,4]

	plt.errorbar(nums,[avg_rand_c_link[k] for k in abcde],[stdev_rand_c_link[k] for k in abcde],linestyle="None",marker="o",label="C-link")
	plt.xticks(range(5), abcde, size='small')
	plt.ylabel("Rand index")
	plt.axis([-0.2,4.2,0.0,1.2])
	plt.legend()
	plt.savefig("C-link")
	plt.close()
	plt.errorbar(nums,[avg_rand_s_link[k] for k in abcde],[stdev_rand_s_link[k] for k in abcde],linestyle="None",marker="o",label="S-link")
	plt.xticks(range(5), abcde, size='small')
	plt.axis([-0.2,4.2,0.0,1.2])
	plt.ylabel("Rand index")
	plt.legend()
	plt.savefig("S-link")
	plt.close()
	print(avg_rand_c_link)
	print(avg_rand_s_link)
		#print(data_files)
#general_summary()

def _save(data_obj,name):
	visu.plot_coords_label_color(data_obj)
	plt.savefig(name+".png")
	plt.close()
def c_vs_s_link():
	croissants = trivial_gen.croissants(50,5.0,0.5)
	difficult = trivial_gen.balanced_multiple_gauss_blobs(10.0,2.0,20,5,0.75)
	c_c = deepcopy(croissants)
	c_d = deepcopy(difficult)
	s_c = deepcopy(croissants)
	s_d = deepcopy(difficult)
	c_c = hierarchical.agglomerative(c_c,linkage="c-link")
	c_d = hierarchical.agglomerative(c_d,linkage="c-link")
	s_c = hierarchical.agglomerative(s_c)
	s_d = hierarchical.agglomerative(s_d)
	_save(c_c,"clink_croissant")
	_save(s_c,"slink_croissant")
	_save(c_d,"clink_difficult")
	_save(s_d,"slink_difficult")
c_vs_s_link()
