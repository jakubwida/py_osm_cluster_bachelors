import os
import py_osm_cluster.visualisation.visualisation as visu
import imageio
import matplotlib.pyplot as plt



class Animation:
	def __init__(self,filename,draw_labels=False,draw_centers=False,frame_duration=0.5):
		if not os.path.exists(filename):
		    os.makedirs(filename)
		self.draw_labels = draw_labels
		self.draw_centers = draw_centers
		self.filename = filename
		self.step_count = 0
		self.filenames = []
		self.duration = frame_duration
	def add_step(self,data_obj):
		print("frame:"+str(self.step_count))
		self.step_count = self.step_count +1
		name = str(self.step_count)
		self.filenames.append(name)
		if self.draw_labels:
			visu.plot_coords_label_color(data_obj)
		else:
			visu.plot_coords_label_num(data_obj)
		if self.draw_centers:
			visu.plot_centers_by_label_color(data_obj)
		plt.savefig(self.filename+"/"+name+".png")
		plt.close()

	def compile(self):
		images = []
		for f in self.filenames:
			fname = self.filename+"/"+f+".png"
			images.append(imageio.imread(fname))
			os.remove(self.filename+"/"+f+".png")
		os.rmdir(self.filename)
		imageio.mimsave(self.filename+'.gif', images,duration=self.duration)
