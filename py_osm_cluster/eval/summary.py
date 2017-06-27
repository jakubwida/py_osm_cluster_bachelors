import os
from copy import deepcopy
from py_osm_cluster.util.coords import Coords as Coords
from py_osm_cluster.cluster import scikit
from py_osm_cluster.cluster import partitioning

from py_osm_cluster.eval import comparative as comparative
from py_osm_cluster.eval import standalone as standalone
from py_osm_cluster.cluster import hierarchical

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
		self.current_rand_harvest = comparative.scikit_rand_index(data_obj,self.current_object)

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
			r_rand_indexes.append(self.current_rand_harvest)
			r_standalone.append(standalone.standard_scores_dict(temp_data_obj))
			r_comparative.append(comparative.scikit_all_scores_dict(temp_data_obj,self.current_object))
		#print(r_standalone)
		#print(r_comparative)
		return {"rand_indexes":r_rand_indexes,\
"standalone":self.compress_dicts(r_standalone),\
"comparative":self.compress_dicts(r_comparative),\
"initial_standalone":r_initial_standalone_dict}
#"initial_general":r_initial_general_data_dict

	def test_data_set(self,folder_name,n_of_tests,function,function_kwargs):
		files = [folder_name+"/"+i for i in list(os.listdir(folder_name))]
		out =[]
		for i in files:
			print("investigating file:"+i)
			out.append(self.test_data_object(i,n_of_tests,function,function_kwargs))
		return out


	def execute(self,folder_name):
		data = self.test_data_set(folder_name,5,partitioning.k_means,{})
		data = self.compress_dicts(data)
		for k in data:
			print(k)
			print(data[k])
