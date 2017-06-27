import matplotlib.pyplot as plt
import math
#from py_osm_cluster.util.unlabeled_coords import Unlabeled_Coords as UC
"""
def plot_simple_data(data_obj):
	tup = data_obj.get_plottable_data()
	plt.plot(tup[0],tup[1],'or')

def plot_labeled_data_num(data_obj):
	tup = data_obj.get_plottable_data()
	labels = data_obj.labels.labels
	plt.plot(tup[0],tup[1],'or')
	for i,txt in enumerate(labels):
			print(i,txt)
			plt.annotate(txt,(tup[0][i],tup[1][i]))

def plot_labeled_data_color(data_obj):
	tup = data_obj.get_plottable_data()
	labels = data_obj.labels.labels
	for i in labels:pass
	plt.plot(tup[0],tup[1],'or')
"""

def util_unzip(coords):
	x_c = [x[0] for x in coords]
	y_c = [x[1] for x in coords]
	return x_c,y_c

def get_color_shape(num):
	colors=['b','g','r','c','m','y','k']
	shapes = ['o','.','v','^','<','>','8','s','p']
	col_out = colors[num%len(colors)]
	shape_out = shapes[(math.floor(num/len(colors)))%len(shapes)]
	return(col_out+shape_out)

def get_color(num):
	colors=['b','g','r','c','m','y','k']
	return(colors[num%len(colors)]+'l')

def plot_coords(data_obj):
	x,y = util_unzip(data_obj.coords)
	plt.plot(x,y,'ro')

def plot_coords_label_num(data_obj):
	data_x,data_y = util_unzip(data_obj.coords)
	plt.plot(data_x,data_y,'ro')
	for i,txt in enumerate(data_obj.labels):
			print(i,txt)
			plt.annotate(txt,(data_x[i],data_y[i]))

def plot_coords_label_color(data_obj):
	for i in range(len(data_obj.labels)):
		coords = data_obj.coords[i]
		plt.plot(coords[0],coords[1],get_color_shape(data_obj.labels[i]))

def plot_centers_by_label_color(data_obj):
	for num,val in enumerate(data_obj.c_positions):
		plt.plot(val[0],val[1],get_color_shape(num),markersize=10)

def lineplot(dataset,labels):
		plt.plot(dataset,label=labels)
