import os
from copy import deepcopy
from py_osm_cluster.util.coords import Coords as Coords
from py_osm_cluster.cluster import scikit
from py_osm_cluster.cluster import partitioning

from py_osm_cluster.eval import comparative as comparative
from py_osm_cluster.eval import standalone as standalone
from py_osm_cluster.cluster import hierarchical

import py_osm_cluster.util.statistic as statistic

import py_osm_cluster.visualisation.visualisation as visu
import py_osm_cluster.visualisation.animation as anim
import matplotlib.pyplot as plt



class GeneralTest:
	def __init__(self):
		self.current_object = None
		self.current_rand_harvest = []

	""" compresses the list of dictionaries into dictionary of lists"""
	def compress_dicts(self,dictionary_list):
		out = {x:[] for x in dictionary_list[0]}
		for i in dictionary_list:
			for k in out:
				out[k].append(i[k])
		return out
	def harvest_rand_index(self,data_obj):
		self.current_rand_harvest.append(comparative.scikit_rand_index(data_obj,self.current_object))
		#print("harvesting")

	def test_data_object(self,file,n_of_tests,function,function_kwargs):
		function_kwargs["on_step"]=self.harvest_rand_index
		data_obj = Coords()
		data_obj.read_file(file)
		self.current_object = data_obj

		r_initial_standalone_dict = standalone.standard_scores_dict(data_obj)
		#r_initial_general_data_dict = standalone.general_evaluate_clustered_object(data_obj)
		r_standalone =[]
		r_comparative =[]
		r_rand_indexes = []
		for i in range(n_of_tests):
			self.current_rand_harvest=[]
			temp_data_obj = deepcopy(data_obj)
			temp_data_obj= function(data_obj,**function_kwargs)
			#print(self.current_rand_harvest)
			r_rand_indexes.append(self.current_rand_harvest)
			#plt.plot(self.current_rand_harvest)
			#plt.show()
			r_standalone.append(standalone.standard_scores_dict(temp_data_obj))
			r_comparative.append(comparative.scikit_all_scores_dict(temp_data_obj,self.current_object))
		#print(r_standalone)
		#print(r_comparative)
		out = {"rand_indexes":r_rand_indexes,"initial_standalone":r_initial_standalone_dict}
		#print(r_rand_indexes)
		out.update(self.compress_dicts(r_standalone))
		out.update(self.compress_dicts(r_comparative))
		return out
#"initial_general":r_initial_general_data_dict

	def test_data_set(self,folder_name,n_of_tests,function,function_kwargs):
		files = [folder_name+"/"+i for i in list(os.listdir(folder_name))]
		out =[]
		for i in files:
			print("investigating file:"+i)
			out.append(self.test_data_object(i,n_of_tests,function,function_kwargs))
		return out

	def compile_data(self,test_data_out):
		data = self.compress_dicts(test_data_out)
		data["initial_standalone"] = self.compress_dicts(data["initial_standalone"])
		data["rand_indexes"] = [i for sublist in data["rand_indexes"] for i in sublist]
		return data

	def calculate_avg_stdev(self,compiled_data):
		out={}
		out["rand_indexes"] = list(zip(*compiled_data["rand_indexes"]))
		out["rand_indexes"] = [statistic.stdev_avg(x) for x in out["rand_indexes"]]

		out["initial_standalone"] = {k:statistic.stdev_avg(compiled_data["initial_standalone"][k]) for k in compiled_data["initial_standalone"]}

		#out["initial_standalone"] = [statistic.stdev_avg(x) for x in out["rand_indexes"]]
		for i in compiled_data:
			if i is not "rand_indexes" and i is not "initial_standalone":
				out[i] = [item for sublist in compiled_data[i] for item in sublist]
				#print(out[i])
				out[i] = statistic.stdev_avg(out[i])
		return out;


	def execute(self,folder_name):
		data = self.compile_data(self.test_data_set(folder_name,5,partitioning.k_means,{}))
		return (data,self.calculate_avg_stdev(data))

import py_osm_cluster
def test_multiple_datasets(main_folder):
	short_folders = list(os.listdir(main_folder))
	#folders = [main_folder+"/"+i for i in list(os.listdir(main_folder))]
	gt = GeneralTest()
	for i in short_folders:
		full_folder =main_folder+"/"+i
		data = gt.execute(full_folder)
		#visu.lineplot(data[1]["rand_indexes"],i)
		plt.plot(data[1]["rand_indexes"],label=i)
		f = open("output_for:"+i,"w")
		f.write(str(data[1]))
	plt.xlabel("iteration")
	plt.ylabel("Rand index")
	plt.legend(loc='upper left')
	plt.show()
