import random
import math
import py_osm_cluster.util.geom as geom


#util below
def distance(a,b):
	return math.sqrt(math.pow(a[0]-b[0],2)+math.pow(a[1]-b[1],2))
#end util


def gauss_point(coords,sigma):
	return [random.gauss(0,sigma)+coords[x] for x in range(2)]

def weighted_gauss_point(coords,sigmas):
	return [random.gauss(0,x)+coords[num] for num,x in enumerate(sigmas)]

def linear_square_point(coords,side):
	return [random.uniform(coords[x]-side/2.0,coords[x]+side/2.0) for x in range(2)]

def linear_circle_point(coords,radius):
	while True:
		x = random.uniform(-radius,radius)
		y = random.uniform(-radius,radius)
		if geom.distance((0.0,0.0),(x,y))<radius:
			#print(math.sqrt(math.pow(x-coords[0],2)+math.pow(x-coords[0],2)))
			break
	return (x+coords[0],y+coords[1])

#below: helper functions generating linear list of points

"""generates a number of points on the line defined by two points. points generated are on the line in equal distances, not random"""
def segment_linear_division(coords_1,coords_2,number):
	out =[]
	length = math.sqrt(math.pow(coords_1[0]-coords_2[0],2)+math.pow(coords_1[1]-coords_2[1],2))
	distance = float(length)/float(number)
	print(length)
	print(distance)
	for i in range(number):
		print(distance*i)
		x = coords_1[0]+distance*(i/length)*(coords_2[0]-coords_1[0])
		y = coords_1[1]+distance*(i/length)*(coords_2[1]-coords_1[1])
		xy =(x,y)
		print(xy)
		out.append(xy)
	return out

"""generates a number of points on the arc defined by coords, radius and two angles. points generated are on the arc in equal distances, not random"""
def arc_linear_division(coords,radius,angle_1,angle_2,number):
	out =[]
	angle_unit = (angle_2-angle_1)/number
	for i in range(number):
		x = radius*math.sin(angle_1+i*angle_unit)
		y = radius*math.cos(angle_1+i*angle_unit)
		xy =(x+coords[0],y+coords[1])
		out.append(xy)
	return out


#below: functions generating multiple points

""" sigma = variance (0.1 = centered, 5= over large area )"""
def gauss_blob(coords,sigma,number):
	out =[]
	for i in range(number):
		out.append(gauss_point(coords,sigma))
	return out

def weighted_gauss_blob(coords,sigmas,number):
	out =[]
	for i in range(number):
		out.append(weighted_gauss_point(coords,sigmas))
	return out

def gauss_segment(coords_1,coords_2,sigma,number):
	points = segment_linear_division(coords_1,coords_2,number)
	out =[]
	for i in points:
		out.append(gauss_point(i,sigma))
	return out

def gauss_arc(coords,radius,angle_1,angle_2,sigma,number):
	points = arc_linear_division(coords,radius,angle_1,angle_2,number)
	out =[]
	for i in points:
		out.append(gauss_point(i,sigma))
	return out


def linear_circle(coords,radius,number):
	out =[]
	for i in range(number):
		out.append(linear_circle_point(coords,radius))
	return out

def linear_square(coords,side,number):
	out =[]
	for i in range(number):
		out.append(linear_square_point(coords,side))
	return out

#imperfect, but will do
def linear_imperfect_arc(coords,radius,thickness,angle_1,angle_2,number):
	points = arc_linear_division(coords,radius,angle_1,angle_2,number)
	out =[]
	for i in points:
		out.append(linear_circle_point(i,thickness))
	return out


#generators returning Coord objects
from py_osm_cluster.util.coords import Coords as C

def balanced_multiple_linear_circles(field_size,min_distance_between_centers,n_in_blob,n_of_blobs,radius):
	data_obj = C()
	data_obj.c_number = n_of_blobs
	data_obj.c_positions.append([random.uniform(0.0,field_size) for i in range(2)])
	while len(data_obj.c_positions) < data_obj.c_number:
		newpos = [random.uniform(0.0,field_size) for i in range(2)]
		insert = True
		for i in data_obj.c_positions:
			if distance(i,newpos) < min_distance_between_centers:
				insert = False
				break
		if insert:
			data_obj.c_positions.append(newpos)
	for num,val in enumerate(data_obj.c_positions):
		gb = linear_circle(val,radius,n_in_blob)
		data_obj.coords = data_obj.coords + gb
		data_obj.labels = data_obj.labels + [num for j in range(n_in_blob)]
	return data_obj

#generates gauss blobs given possible area (field size 0,0 to fs,fs), number of blobs and number of items per blob
def multiple_gauss_blobs(field_size,n_in_blob,n_of_blobs,sigma):
	data_obj =C()
	data_obj.c_number = n_of_blobs
	for i in range(n_of_blobs):
		data_obj.c_positions.append([random.uniform(0.0,field_size) for i in range(2)])
	for num,val in enumerate(data_obj.c_positions):
		gb = gauss_blob(val,sigma,n_in_blob)
		data_obj.coords = data_obj.coords + gb
		data_obj.labels = data_obj.labels + [num for j in range(n_in_blob)]
	return data_obj

def multiple_weighted_gauss_blobs(field_size,n_in_blob,n_of_blobs,sigmas):
	data_obj =C()
	data_obj.c_number = n_of_blobs
	for i in range(n_of_blobs):
		data_obj.c_positions.append([random.uniform(0.0,field_size) for i in range(2)])
	for num,val in enumerate(data_obj.c_positions):
		gb = weighted_gauss_blob(val,sigmas,n_in_blob)
		data_obj.coords = data_obj.coords + gb
		data_obj.labels = data_obj.labels + [num for j in range(n_in_blob)]
	return data_obj


#Warning! not always possible, may loop
def balanced_multiple_gauss_blobs(field_size,min_distance_between_centers,n_in_blob,n_of_blobs,sigma):
	data_obj = C()
	data_obj.c_number = n_of_blobs
	data_obj.c_positions.append([random.uniform(0.0,field_size) for i in range(2)])
	while len(data_obj.c_positions) < data_obj.c_number:
		newpos = [random.uniform(0.0,field_size) for i in range(2)]
		insert = True
		for i in data_obj.c_positions:
			if distance(i,newpos) < min_distance_between_centers:
				insert = False
				break
		if insert:
			data_obj.c_positions.append(newpos)
	for num,val in enumerate(data_obj.c_positions):
		gb = gauss_blob(val,sigma,n_in_blob)
		data_obj.coords = data_obj.coords + gb
		data_obj.labels = data_obj.labels + [num for j in range(n_in_blob)]
	return data_obj

""" generates num integers that sum up to given number"""
def _integers_summing(num, sum):
    dividers = sorted(random.sample(list(range(1, sum)), num - 1))
    return [a - b for a, b in zip(dividers + [sum], [0] + dividers)]

#Warning! not always possible, may loop
def balanced_random_size_gauss_blobs(field_size,min_distance_between_centers,min_in_blob,total_points,n_of_blobs,sigma):
	data_obj = C()
	data_obj.c_number = n_of_blobs
	data_obj.c_positions.append([random.uniform(0.0,field_size) for i in range(2)])
	while len(data_obj.c_positions) < data_obj.c_number:
		newpos = [random.uniform(0.0,field_size) for i in range(2)]
		insert = True
		for i in data_obj.c_positions:
			if distance(i,newpos) < min_distance_between_centers:
				insert = False
				break
		if insert:
			data_obj.c_positions.append(newpos)
	for num,val in enumerate(data_obj.c_positions):
		gb = gauss_blob(val,sigma,min_in_blob)
		data_obj.coords = data_obj.coords + gb
		data_obj.labels = data_obj.labels + [num for j in range(min_in_blob)]
	sum_no_min = total_points - (n_of_blobs*min_in_blob)
	points_to_add = _integers_summing(n_of_blobs, sum_no_min)
	#print(points_to_add)
	for num,i in enumerate(points_to_add):
		gb = gauss_blob(data_obj.c_positions[num],sigma,i)
		data_obj.coords = data_obj.coords + gb
		data_obj.labels = data_obj.labels + [num for j in range(i)]
	#print(len(data_obj.coords))
	return data_obj



#Warning! not always possible, may loop
def balanced_multiple_weighted_gauss_blobs(field_size,min_distances_between_centers,n_in_blob,n_of_blobs,sigmas):
	data_obj = C()
	data_obj.c_number = n_of_blobs
	data_obj.c_positions.append([random.uniform(0.0,field_size) for i in range(2)])
	while len(data_obj.c_positions) < data_obj.c_number:
		newpos = [random.uniform(0.0,field_size) for i in range(2)]
		insert = True
		for i in data_obj.c_positions:
			if math.fabs(i[0]-newpos[0]) < min_distances_between_centers[0] or math.fabs(i[1]-newpos[1]) < min_distances_between_centers[1]:
				insert = False
				break
		if insert:
			data_obj.c_positions.append(newpos)
	for num,val in enumerate(data_obj.c_positions):
		gb = weighted_gauss_blob(val,sigmas,n_in_blob)
		data_obj.coords = data_obj.coords + gb
		data_obj.labels = data_obj.labels + [num for j in range(n_in_blob)]
	return data_obj

def gauss_circle_in_other(outer_radius,p_in_central,p_in_outer,sigma_in,sigma_out):
	data_obj = C()
	data_obj.c_number = 2
	data_obj.coords = data_obj.coords + gauss_blob((0.0,0.0),sigma_in,p_in_central)
	data_obj.labels = data_obj.labels + [0]*p_in_central
	data_obj.coords = data_obj.coords + gauss_arc((0.0,0.0),outer_radius,0.0,2*math.pi,sigma_out,p_in_outer)
	data_obj.labels = data_obj.labels + [1]*p_in_outer
	return data_obj

def croissants(number_in_c,radius_distance,sigma):
	data_obj = C()
	data_obj.c_number = 2
	data_obj.coords = data_obj.coords + gauss_arc((0.0,0.0),radius_distance,0.0,1*math.pi,sigma,number_in_c)
	data_obj.labels = data_obj.labels + [0]*number_in_c
	data_obj.c_positions.append((radius_distance,0.0))

	data_obj.coords = data_obj.coords + gauss_arc((0.0,radius_distance),radius_distance,math.pi,2*math.pi,sigma,number_in_c)
	data_obj.labels =  data_obj.labels + [1]*number_in_c
	data_obj.c_positions.append((-radius_distance,radius_distance))
	return data_obj
