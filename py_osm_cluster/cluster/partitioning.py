import math
import random

def distance(a,b):
	return math.sqrt(math.pow(a[0]-b[0],2)+math.pow(a[1]-b[1],2))

""" centroid with fallback 0.0,0.0 for coordinate set"""
def centroid(coords):
	num = len(coords)
	if num == 0:
		return [0.0,0.0]
	lists = list(zip(*coords))

	x = sum(lists[0])/num
	y = sum(lists[1])/num
	xy =(x,y)
	return xy

""" centroid with random coordinate as fallback"""
def centroid_rand(data_obj,coords):
	num = len(coords)
	if num == 0:
		return random.choice(data_obj.coords)
	lists = list(zip(*coords))
	x = sum(lists[0])/num
	y = sum(lists[1])/num
	xy =(x,y)
	return xy


""" medain centroid with radnom fallback"""
def median_centroid_rand(data_obj,coords):
	num = len(coords)
	if num == 0:
		return random.choice(data_obj.coords)
	return coords[math.floor(num/2.0)]




#actual clustering

"""requires Coords object with cluster number  fallback centroid is at 0.0 (when one centroid has no closest points compared to others)
kwargs:
	iterations
	use_default_centers
	anim_obj
"""
def k_means(data_obj,**kwargs):
	if "use_default_centers" not in kwargs or kwargs["use_default_centers"] == False:
		data_obj.c_positions=[]
		data_obj.c_positions = random.sample(data_obj.coords,data_obj.c_number)

	iterations  = 10
	if "iterations" in kwargs:
		iterations = kwargs["iterations"]

	anim_obj = kwargs.get("anim_obj",None)
	animated = False
	if anim_obj!=None:
		animated = True

	for i in range(iterations):
		data_obj.labels = []
		for coord in data_obj.coords:
			distances = [[distance(coord,center),num] for num,center in enumerate(data_obj.c_positions)]
			distances = sorted(distances,key=lambda x: x[0])
			data_obj.labels.append(distances[0][1])
		mini_c =[[] for i in data_obj.c_positions]
		for num,val in enumerate(data_obj.labels):
			mini_c[val].append(data_obj.coords[num])
		#print(mini_c)
		for index,val in enumerate(mini_c):
			data_obj.c_positions[index] = centroid(val)
		if animated:
			anim_obj.add_step(data_obj)
	return data_obj




"""requirres Coords object with cluster number set. . As fallback it chooses random point instead of 0.0
kwargs:
	iterations
	use_default_centers
	anim_obj
"""
def k_means_fallback(data_obj,**kwargs):
	if "use_default_centers" not in kwargs or kwargs["use_default_centers"] == False:
		data_obj.c_positions=[]
		data_obj.c_positions = random.sample(data_obj.coords,data_obj.c_number)

	iterations  = 10
	if "iterations" in kwargs:
		iterations = kwargs["iterations"]

	anim_obj = kwargs.get("anim_obj",None)
	animated = False
	if anim_obj!=None:
		animated = True

	for i in range(iterations):
		data_obj.labels = []
		for coord in data_obj.coords:
			distances = [[distance(coord,center),num] for num,center in enumerate(data_obj.c_positions)]
			distances = sorted(distances,key=lambda x: x[0])
			data_obj.labels.append(distances[0][1])
		mini_c =[[] for i in data_obj.c_positions]
		for num,val in enumerate(data_obj.labels):
			mini_c[val].append(data_obj.coords[num])
		#print(mini_c)
		for index,val in enumerate(mini_c):
			data_obj.c_positions[index] = centroid_rand(data_obj,val)
		if animated:
			anim_obj.add_step(data_obj)
	return data_obj




""" requires Coords object with custer nuber set. chooses median as centroid and fallback
kwargs:
	iterations
	use_default_centers
	anim_obj
"""
def k_medians_fallback(data_obj,**kwargs):
	if "use_default_centers" not in kwargs or kwargs["use_default_centers"] == False:
		data_obj.c_positions=[]
		data_obj.c_positions = random.sample(data_obj.coords,data_obj.c_number)

	iterations  = 10
	if "iterations" in kwargs:
		iterations = kwargs["iterations"]

	anim_obj = kwargs.get("anim_obj",None)
	animated = False
	if anim_obj!=None:
		animated = True

	for i in range(iterations):
		data_obj.labels = []
		for coord in data_obj.coords:
			distances = [[distance(coord,center),num] for num,center in enumerate(data_obj.c_positions)]
			distances = sorted(distances,key=lambda x: x[0])
			data_obj.labels.append(distances[0][1])
		mini_c =[[] for i in data_obj.c_positions]
		for num,val in enumerate(data_obj.labels):
			mini_c[val].append(data_obj.coords[num])
		#print(mini_c)
		for index,val in enumerate(mini_c):
			data_obj.c_positions[index] = median_centroid_rand(data_obj,val)
		if animated:
			anim_obj.add_step(data_obj)
	return data_obj



""" requires Coords object with custer nuber set. each iteration divides equally the set between cluster centers
kwargs:
	iterations
	use_default_centers
	anim_obj
"""
def k_means_balanced(data_obj,**kwargs):
	if "use_default_centers" not in kwargs or kwargs["use_default_centers"] == False:
		data_obj.c_positions=[]
		data_obj.c_positions = random.sample(data_obj.coords,data_obj.c_number)

	iterations  = 10
	if "iterations" in kwargs:
		iterations = kwargs["iterations"]

	anim_obj = kwargs.get("anim_obj",None)
	animated = False
	if anim_obj!=None:
		animated = True

	num_per_cluster = math.floor(len(data_obj.coords)/len(data_obj.c_positions))
	for i in range(iterations):
		data_obj.labels = [0]*len(data_obj.coords)

		distances = []
		for num,j in enumerate(data_obj.coords):
			distances.append(([distance(j,center) for center in data_obj.c_positions],num))
		distances = sorted(distances,key = lambda x: min(x[0]) )
		for j in range(data_obj.c_number):
			for k in range(num_per_cluster):
				current_d  = distances[j*k]
				data_obj.labels[current_d[1]]=current_d[0].index(min(current_d[0]))

		mini_c =[[] for i in data_obj.c_positions]
		for num,val in enumerate(data_obj.labels):
			mini_c[val].append(data_obj.coords[num])
		#print(mini_c)
		for index,val in enumerate(mini_c):
			data_obj.c_positions[index] = centroid_rand(data_obj,val)
		if animated:
			anim_obj.add_step(data_obj)
	return data_obj
