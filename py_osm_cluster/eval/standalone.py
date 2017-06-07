import sklearn.metrics as metrics
import numpy as np
import itertools
import math

def distance(a,b):
	return math.sqrt(math.pow(a[0]-b[0],2)+math.pow(a[1]-b[1],2))

def scikit_silhouette_score(data_obj):
	return metrics.silhouette_score(np.array(data_obj.coords),np.array(data_obj.labels))

def scikit_calinski_harabaz_score(data_obj):
	return metrics.calinski_harabaz_score(data_obj.coords,data_obj.labels)

#below: general information about data objects

""" calculates and returns average and standard deviation in tuple"""
def statistics_distance_within_data(coords):
	avg = 0
	stdev =0
	pairs =  list(itertools.permutations(coords,2))
	num =len(pairs)
	for i in pairs:
		avg = avg + distance(i[0],i[1])
	avg = avg/num
	for i in pairs:
		stdev = stdev + math.pow(avg -distance(i[0],i[1]),2)
	stdev = stdev/num
	stdev = math.sqrt(stdev)
	return (avg,stdev)

def statistics_distance_multi_cluster(data_obj):
	num_of_clusters = max(data_obj.labels)+1
	clustersets = [[] for i in range(num_of_clusters)]
	for num,i in enumerate(data_obj.labels):
		clustersets[i].append(data_obj.coords[num])
	clusterset_data =[]
	for i in clustersets:
		clusterset_data.append(statistics_distance_within_data(i))
	avg,stdev=zip(*clusterset_data)
	avg = sum(avg)/len(avg)
	stdev = sum(stdev)/len(stdev)
	return clusterset_data,avg,stdev

import py_osm_cluster.util.geom as geom

""" calculates average and standard deviation of triangulation edges of coordinate set"""
def triangulation_distance_within(coords):
	triangulated = geom.triangulate_set(coords)
	distances = [geom.distance(i[0],i[1]) for i in triangulated]
	avg = sum(distances)/len(distances)
	stdev =0
	for i in distances:
		stdev = stdev + math.pow(avg-i,2)
	stdev = math.sqrt(stdev/len(distances))
	return (avg,stdev)

def triangulation_general_info(data_obj):
	general_triangulation = geom.triangulate_set(data_obj.coords)
	clusters=[[]for i in range(len(data_obj.labels))]
	for num,i in enumerate(labels):
		clusters[i]=data_obj.coords[num]
	cluster_triangulations = [geom.triangulate_set(cluster) for cluster in clusters]
	for i in cluster_triangulations:
		general_triangulation = [x for x in general_triangulation if x not in i]
	#add average calculation and stdev for general and clusters
	#also test all of it
