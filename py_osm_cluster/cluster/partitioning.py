import math
import random




import py_osm_cluster.util.geom as geom
""" a k_means utility functions. assigns Coords.labels of Coords.coords to nearest Coords.c_positions in given data_obj (Coords)"""
def _reassign_to_cluster_centers(data_obj):
	for num,i in enumerate(data_obj.coords):
		distances = [geom.distance(i,c) for c in data_obj.c_positions]
		mindist = min(distances)
		data_obj.labels[num] = distances.index(mindist)

""" sets Coords.c_positions (data_obj) to means of clusters, as each cluster is represented by subset of Coords.coords with distinct Coords.labels on the same index """
def _move_centers_to_centroids(data_obj):

	center_sums = [[0.0,0.0] for i in range(data_obj.c_number)]
	num_in_clusters =[0 for i in range(data_obj.c_number)]
	data_obj.c_positions =[None for i in range(data_obj.c_number)]
	for num,i in enumerate(data_obj.labels):
		center_sums[i] = [center_sums[i][j] + data_obj.coords[num][j] for j in range(2)]
		num_in_clusters[i] += 1
	for num,i in enumerate(center_sums):
		val = [i[j]/num_in_clusters[num] for j in range(2)]
		data_obj.c_positions[num] = val

""" requires data_obj with c_number set. picks random points."""
def _init_forgy(data_obj):
	data_obj.c_positions = random.sample(data_obj.coords,data_obj.c_number)

""" requires data_obj with c_number set. makes clusters form random points, and updates centroids. CHANGES data_obj.labels"""
def _init_random_partitions(data_obj):
	possibles = list(range(data_obj.c_number))
	data_obj.labels = [random.choice(possibles) for i in data_obj.labels]
	#print(data_obj.labels)
	_move_centers_to_centroids(data_obj)

from numpy.random import choice
""" requires data_obj with c_number set. makes clusters form random points, and updates centroids. CHANGES data_obj.labels"""
def _init_plus_plus(data_obj):
	data_obj.c_positions =[]
	remaining = data_obj.c_number
	if remaining > 0:
		remaining -=1
		data_obj.c_positions.append(random.choice(data_obj.coords))
	distances = [float("inf") for i in data_obj.coords]
	while remaining > 0:
		last_center = data_obj.c_positions[-1]
		remaining -=1
		for num,i in enumerate(distances):
			current_coord = data_obj.coords[num]
			#print(last_center)
			newdistance = math.pow(geom.distance(last_center,current_coord),2.0)
			distances[num] = min([distances[num],newdistance])

		sums = sum(distances)
		next_distances = [i/sums for i in distances]

		indexes = list(range(len(data_obj.coords)))
		#print(distances)
		new_center = choice(indexes,1,p=next_distances)
		new_center = data_obj.coords[new_center]
		data_obj.c_positions.append(new_center)
	#inicjalizacja:
	#1 centrum jest losowo wybierane z punktów
	# robimy tablice dystansów^2 dla kazdegu punktu do centrum
	# 2 cntrum jest wybierane z punktów proporcjonalneie do ich dystansu^2 do 1. (Dpunkt^2/suma(Dwszystkie_punkty2))
	# kazde nastepne centrum jest wybierane proporcjonalnie do minimum dystansow z danego punktu

""" does nothing"""
def _init_default_pos(data_obj):pass

import copy as copy
""" performs k_means. Non destructive
data_obj = Coords object. must have Coords.c_number set. Coords.c_positions optional
kwargs:
	iterations =int, default 5, number of iterations
	on_step = function(data_obj), default None. runs given function every step
	initialisation = string, one of : "forgy" "random_partitions" "kmeans_++" "default_pos", default = "forgy"
"""
def k_means(data_obj,**kwargs):
	data_obj = copy.deepcopy(data_obj)
	on_step = kwargs.get("on_step",None)
	iterations = kwargs.get("iterations",5)
	initialisation = kwargs.get("initialisation","forgy")
	init_dict = {"forgy":_init_forgy,"random_partitions":_init_random_partitions,"kmeans_++":_init_plus_plus,"default_pos":_init_default_pos}
	init_dict[initialisation](data_obj)
	for i in range(iterations):
		_reassign_to_cluster_centers(data_obj)
		_move_centers_to_centroids(data_obj)
		if on_step !=None:
			on_step(data_obj)
	return data_obj
