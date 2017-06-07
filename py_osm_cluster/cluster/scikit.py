from copy import deepcopy
def scikit_k_means(data_obj):
	from sklearn.cluster import KMeans
	kmeans = KMeans(n_clusters=data_obj.c_number)
	kmeans.fit(data_obj.coords)
	labels = kmeans.labels_
	from py_osm_cluster.util.coords import Coords as C
	c = deepcopy(data_obj)
	c.labels = labels
	return(c)
