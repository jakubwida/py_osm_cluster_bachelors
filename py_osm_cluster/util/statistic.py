import math
#this file is currently unused


def avg_coords(coords):
	x,y=list(zip(*coords))
	x=sum(x)
	y=sum(y)
	x=x/len(coords)
	y=y/len(coords)
	return(x,y)

#unfinished
def stdev_coords(coords):pass
#avg = avg_coords(coords)
#x,y =


def avg(array):
	return sum(array)/len(array)

def avg_array(array_array):
	rows = list(zip(*array_array))
	avgs = [avg(i) for i in rows]
	return avgs

def stdev_avg(array):
	avg_result = avg(array)
	differences = [math.pow(avg_result-i,2) for i in array]
	#print(differences)
	var = avg(differences)
	stdev = math.sqrt(var)
	return(stdev,avg_result)

# retuns list of 2 values first stdev then avg. these two are lists of stdev and avg for each coordinate
def stdev_avg_array(array_array):
	rows = list(zip(*array_array))
	stdev_avgs = [stdev_avg(i) for i in rows]
	stdev_avgs = list(zip(*stdev_avgs))
	return stdev_avgs

def dict_evaluation(array):
	out = {}
	sa = stdev_avg(array)
	out["stdev"] = sa[0]
	out["avg"] = sa[1]
	out["max"] = max(array)
	out["min"] = min(array)
	return out
