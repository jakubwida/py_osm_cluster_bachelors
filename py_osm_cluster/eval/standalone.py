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

import py_osm_cluster.util.statistic as statistic
import itertools
#standard indexes:

""" dunn index = a/b where a = min(distances between clusters), b = max(cluster sizes). distances between clusters and cluster sizes can be defined differently for different purposes. Here cluster size = mean(distances between all points in cluster and its centroid), distance between clusters = avg(distance between centroids of clusters, min distance between two points from different clusters).
Note that larger inter-cluster distances (better separation) and smaller cluster sizes (more compact clusters) lead to a higher DI value."""
def dunn_index(data_obj):
	clusters = {}
	for num,i in enumerate(data_obj.coords):
		label = data_obj.labels[num]
		if label in clusters:
			clusters[label].append(i)
		else:
			clusters[label] = [i]

	centroids ={}
	avg_distances_to_center ={}
	for key in clusters:
		centroid = statistic.avg_coords(clusters[key])
		centroids[key] = centroid
		distances_to_center = [geom.distance(centroid,i) for i in clusters[key]]
		avg_distances_to_center[key] = sum(distances_to_center)/len(distances_to_center)

	max_cluster_size = max(list(avg_distances_to_center.values()))


	cluster_key_pairs = list(itertools.combinations(list(clusters.keys()),2))
	resulting_distances_between_cluster_pairs ={}

	distances_between_cluster_centroids = {}
	for i in cluster_key_pairs:
		distances_between_cluster_centroids[i] = geom.distance(centroids[i[0]],centroids[i[1]])


	distances_between_clusters_as_min_dist_between_pairs = {}
	for i in cluster_key_pairs:
		point_pairs_between_2_clusters = list(itertools.product(clusters[i[0]],clusters[i[1]]))
		distances_in_point_pairs = [geom.distance(j[0],j[1]) for j in point_pairs_between_2_clusters]
		distances_between_clusters_as_min_dist_between_pairs[i] = min (distances_in_point_pairs)


	for i in cluster_key_pairs:
		resulting_distances_between_cluster_pairs[i] = (distances_between_cluster_centroids[i]+ distances_between_clusters_as_min_dist_between_pairs[i])/2.0

	min_distance_between_clusters = min(list(resulting_distances_between_cluster_pairs.values()))

	return min_distance_between_clusters/max_cluster_size

#another go at general data from the clustering:
def dataset_values(coord_array):
	out = {}
	internal_distances = [geom.distance(i[0],i[1]) for i in itertools.combinations(coord_array,2)]
	i_d_stdev_avg = statistic.stdev_avg(internal_distances)
	out["internal ditances avg"] = i_d_stdev_avg[1]
	out["internal ditances stdev"] = i_d_stdev_avg[0]
	out["internal distances max"] = max(internal_distances)
	out["internal distances min"] = min(internal_distances)

	centroid_stdev_avg = statistic.stdev_avg_array(coord_array)
	centroid = centroid_stdev_avg[1]
	out["centroid"] = centroid
	out["stdev of coordinates against centroid"] = centroid_stdev_avg[0]
	distances_centroid_point = [geom.distance(i,centroid) for i in coord_array]
	avg_stdev_d_c = statistic.stdev_avg(distances_centroid_point)
	out["avg distance from centroid"] = avg_stdev_d_c[1]
	out["stdev distance from centroid"] = avg_stdev_d_c[0]
	out["min distance from centroid"] = min(distances_centroid_point)
	out["max distance from centroid"] = max(distances_centroid_point)
	return out

def general_evaluate_entire_object(data_obj):
	return dataset_values(data_obj.coords)

def general_evaluate_clustered_object(data_obj):
	out ={}
	cluster_dict = data_obj.clusters_into_lists_dict()

	internal_distances = []
	avg_internal_distances_per_cluster =[]
	for key in cluster_dict:
		internal_pairs = itertools.combinations(cluster_dict[key],2)
		current_internal_distances = [geom.distance(a[0],a[1]) for a in internal_pairs]
		internal_distances = internal_distances + current_internal_distances
		avg_internal_distances_per_cluster.append(statistic.avg(current_internal_distances))
	out["internal_distances"]=statistic.dict_evaluation(internal_distances)
	
	out["internal_distances_per_cluster"] = statistic.dict_evaluation(avg_internal_distances_per_cluster)

	external_distances =[]
	cluster_key_pairs = itertools.combinations(list(cluster_dict.keys()),2)
	for i in cluster_key_pairs:
		external_distances = external_distances + list(itertools.product(cluster_dict[i[0]],cluster_dict[i[1]]))
	if(len(set(data_obj.labels)))>1:
		external_distances = [geom.distance(i[0],i[1]) for i in external_distances]
		out["external_distances"]=statistic.dict_evaluation(external_distances)


	cluster_sizes =[]
	for i in cluster_dict:
		cluster_sizes.append(len(cluster_dict[key]))

	out["cluster_sizes"]=statistic.dict_evaluation(cluster_sizes)

	#centroids = [statistic.avg_array(cluster_dict[key]) for key in cluster_dict]
	centroids = []

	distances_between_centroids_and_their_points = []
	for key in cluster_dict:
		centroid = statistic.avg_array(cluster_dict[key])
		centroids.append(centroid)
		distances = [geom.distance(centroid,i) for i in cluster_dict[key]]
		distances_between_centroids_and_their_points.extend(distances)

	out["centroid_and_their_points_distances"]=statistic.dict_evaluation(distances_between_centroids_and_their_points)
	if(len(set(data_obj.labels)))>1:
		centroid_distances = [geom.distance(a[0],a[1]) for a in list(itertools.combinations(centroids,2))]
		out["centroid_distances"]=statistic.dict_evaluation(centroid_distances)



	return out
	#we need:
	# average/min/max/stdev distances between all objects in same clusters
 	# average/min/max/stdev distances between objects in different clusters
	# average/min/max/stdev cluster size
	# average/min/max/stdev distance from centroid withn clusters
	# average/min/max/stdev distance between all centroids


def standard_scores_dict(data_obj):
	out ={}
	out["silhouette_score"]=scikit_silhouette_score(data_obj)
	out["dunn_index"]=dunn_index(data_obj)
	out["scikit_calinski_harabaz_score"] =scikit_calinski_harabaz_score(data_obj)
	return out
