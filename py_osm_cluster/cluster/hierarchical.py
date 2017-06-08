import itertools
import py_osm_cluster.util.geom as geom
import copy

#notatki z khg
#DnD było popularne w atach 80
#potem zaginął nastolatek w "kanałach" i detektyw który prowadził sprawę wydał w trakcie książkę o tym że to wina DnD
#nastolatek się odnalazł, ale chuj
#potem teleewangeliści połączyli to z okultyzmem i zaczęli wydawać książki o tym że to szatan
#potem jakaś baba wydała romans że chłop wybiera między nia a DnD
#jest kilka innych spraw dot DnD i wpływu na zbronie, wszystko brenie
#ostatecznie stereotyp DnD ma dwie części : sataista, oraz infantylny
#infantylny wzięło się z tego że ci ludzie mają dobrą wrażliwość i dlatego mogą grać



#goal:
#1. make ordered distance arrray
#2. sort by distance
#3. take 1st element
#4. remove all elements that are within the same cluster as the 1st one
#5. repeat from step 3 untill

""" checks I,II label index value-> sets all labels that have II value to I one. returns list of indexes with this value """
def combine_clusters(index_a,index_b,data_obj):
	out =[]
	val_1 = data_obj.labels[index_a]
	val_2 = data_obj.labels[index_b]
	for num,i in enumerate(data_obj.labels):
		if i == val_2:
			data_obj.labels[num]=val_1
			out.append(num)
		if i == val_1:
			out.append(num)
	return [set(i) for i in itertools.combinations(out,2)]

""" requires Coords object with coordinates set, and target cluster number as a second argument. returns clustered (labelled) Coords object. Agglomerative bottom - up algorithm starting with each point as its own cluster. every itertation two points with shortest distances have their clusters combined., and all resulting internal distances form that connection are eliminated withinn storage. Algorithm is very slow"""
def agglomerative_single_link(data_obj,target_c_num):
	c = [[i] for i in range(len(data_obj.coords))]
	#dict of clusters, keys: int, first value used, val = indexes of points
	clusters = {}
	for i in c:
		clusters[i[0]]=i

	data_obj.labels = [0 for i in data_obj.coords]

	#dict of distances. key = frozenset(cluster_a,cluster_b) val = distance(cluster_a,cluster_b)
	distances ={}
	for i in itertools.combinations(clusters.keys(),2):
		distances[frozenset(i)]=geom.distance(data_obj.coords[i[0]],data_obj.coords[i[1]])

	while len(clusters) > target_c_num:
		# finding a set(c_index,c_index) where distance between indexes is minimal

		min_c = list(min(distances,key=distances.get))
		a = min_c[0]
		b = min_c[1]
		# merging clusters
		clusters[min_c[0]].extend(clusters[min_c[1]])
		clusters.pop(min_c[1],None)

		#merging distances form two clusters so that the larger distance betweeen cluster remains

		#what do we need:
		distance_hash_pairs = []
		for i in clusters:
			added = [frozenset((i,a)),frozenset((i,b))]
			if len(added[0]) == 1:
				added[0] = added[1]
			if len(added[1]) ==1:
				added[1] = added[0]
			distance_hash_pairs.append(added)

		for i in distance_hash_pairs:
			distances[i[0]] = min((distances[i[0]],distances[i[1]]))
			distances.pop(i[1],None)
	for key,val in clusters.items():
		for i in val:
			data_obj.labels[i]=key
	return data_obj


""" algorithm similar to the above one - with the diffenerence that distance between each clustre is determined by distance between two furthest points between the clusters. Uses simple implementation -generally optimall"""
def agglomerative_complete_link(data_obj,target_c_num):
	c = [[i] for i in range(len(data_obj.coords))]
	#dict of clusters, keys: int, first value used, val = indexes of points
	clusters = {}
	for i in c:
		clusters[i[0]]=i

	data_obj.labels = [0 for i in data_obj.coords]

	#dict of distances. key = frozenset(cluster_a,cluster_b) val = distance(cluster_a,cluster_b)
	distances ={}
	for i in itertools.combinations(clusters.keys(),2):
		distances[frozenset(i)]=geom.distance(data_obj.coords[i[0]],data_obj.coords[i[1]])

	while len(clusters) > target_c_num:
		# finding a set(c_index,c_index) where distance between indexes is minimal

		min_c = list(min(distances,key=distances.get))
		a = min_c[0]
		b = min_c[1]
		# merging clusters
		clusters[min_c[0]].extend(clusters[min_c[1]])
		clusters.pop(min_c[1],None)

		#merging distances form two clusters so that the larger distance betweeen cluster remains

		#what do we need:
		distance_hash_pairs = []
		for i in clusters:
			added = [frozenset((i,a)),frozenset((i,b))]
			if len(added[0]) == 1:
				added[0] = added[1]
			if len(added[1]) ==1:
				added[1] = added[0]
			distance_hash_pairs.append(added)

		for i in distance_hash_pairs:
			distances[i[0]] = max((distances[i[0]],distances[i[1]]))
			distances.pop(i[1],None)
	for key,val in clusters.items():
		for i in val:
			data_obj.labels[i]=key
	return data_obj
		#replaces distances that lead to A with larger of distances of A-X, B-X (X is the same)
		#removes all distances that are connected to b




import random
import py_osm_cluster.util.statistic as statistic
import copy
import itertools
""" a simple k-means algorithm, outputting list of clusters, each represented by lsit of indexes of coords in data_obj. requires intital list of indexes (clustered sublist of data_obj and desired number of clusters as cluster_num)"""
def simplified_k_means(data_obj,indexes,iterations,cluster_num):
	centers = random.sample(indexes,cluster_num)
	centers = [data_obj.coords[i] for i in centers]
	#print(indexes)

	for i in range(iterations):
		subclusters =[[] for i in range(cluster_num)]
		distances = [i for i in indexes]
		distances = [[geom.distance(data_obj.coords[i],j) for j in centers] for i in distances ]
		for num,i in enumerate(distances):
			index = i.index(min(i))
			subclusters[index].append(num)

		for num,i in enumerate(subclusters):
			centroided = [data_obj.coords[j] for j in i]
			if len(centroided) > 0:
				print(centroided)
				centers[num] = statistic.avg_coords(centroided)
			else:
				centers[num] = random.choice(data_obj.coords)
	return subclusters

def divisive_k_means(data_obj,level):

	length = len(data_obj.coords)
	data_obj.labels=[0 for i in range(length)]
	subclusters = [list(range(length))]
	for i in range(level):

		for num,i in enumerate(subclusters):
			subclusters[num] = simplified_k_means(data_obj,i,5,3)
		subclusters = list(itertools.chain(*subclusters))
	for num,i in enumerate(subclusters):
		for j in i:
			data_obj.labels[j] = num

	return data_obj
