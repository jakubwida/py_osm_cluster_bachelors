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

from sklearn.cluster import DBSCAN

def scikit_dbscan(data_obj,**kwargs):
	out = deepcopy(data_obj)
	max_dist = kwargs.get("max_dist",0.05)
	dbscan = DBSCAN(eps=max_dist)
	dbscan.fit(data_obj.coords)
	out.labels = list(dbscan.labels_)
	return out
