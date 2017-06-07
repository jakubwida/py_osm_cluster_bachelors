"""additional in connstructori is a dict with any other data- that is mostly cluster_num=integer with number of clusters """
class Unlabeled_Coords:
	def __init__(self,coords=[]):
		self.coord_list=coords
		self.additional={"number":ClusterNumber(self,0),"positions":ClusterPositions(self,[]),"labels":Labels(self,[])};
		self.labels = self.additional["labels"]
		self.number = self.additional["number"]
		self.positions = self.additional["positions"]

	""" adds single point, requires tuple or array as parameter with two elements (x,y) """
	def add_data_point(self,coords):
		self.coord_list.append(coords)

	def get_points(self):
		return(self.coord_list)

	def get_plottable_data(self):
		x_coords = [x[0] for x in self.coord_list]
		y_coords = [x[1] for x in self.coord_list]
		return (x_coords,y_coords)

	def __str__(self):
		additional_strings = ""
		for key in self.additional:
			additional_strings=additional_strings+"\n"+str(self.additional[key])
		return("Unlabeled_Coords:\n"+str(self.coord_list)+"\n additionals:"+additional_strings)

	def parse_line(self,line):
		floats =[float(x) for x in list(line.split(" "))]
		self.add_data_point(floats)

	def line_to_file_string(self,index):
		data = self.coord_list[index]
		return(str(data[0])+" "+str(data[1]))

	def from_file(self,filename):
		f = open(filename,'r')
		mode="to_data"
		for line in f:
			line=line.replace("\n","")
			if line in self.additional:
				mode = line
			else:
				if mode == "to_data":
					self.parse_line(line)
				else:
					self.additional[mode].parse_line(line)

	def to_file(self,filename):
		f = open(filename,'w')
		for i in range(len(self.coord_list)):
			f.write(self.line_to_file_string(i)+"\n")
		for i in self.additional:
			f.write(i+"\n")
			self.additional[i].write_to_file(f)

	""" adds another set of unlabeled coordinates to this one. local additional data stays, except if the other object has cluster number then it is added"""
	def combine_with(self,other):
		self.coord_list.append(other.coord_list);
		for i in self.additional:
			self.additional[i].combine_with(other.additional[i])


class Additional:
	def __init__(self,coord_obj):
		self.coord_obj=coord_obj
		self.complete =True
		self.name="additional"

	def combine_with(self,other_Addit):
		if other_Addit.complete==False:
			self.complete=False

	def __str__(self):
		return(self.name)

	def parse_line(self,line):pass
	def write_to_file(self,file):pass

class ClusterNumber(Additional):
	def __init__(self,coord_obj,num):
		super().__init__(coord_obj)
		self.number=num;
		self.name="Cluster number"

	def combine_with(self,other_Addit):
		super().combine_with(other_Addit)
		self.number+=other_Addit.number

	def __str__(self):
		return(self.name+" "+str(self.number))

	def parse_line(self,line):
		self.number=int(line)

	def write_to_file(self,file):
		file.write(str(self.number)+"\n")

class ClusterPositions(Additional):
	def __init__(self,coord_obj,positions):
		super().__init__(coord_obj)
		self.positions=positions;
		self.name="Cluster center positions"

	def combine_with(self,other_Addit):
		super().combine_with(other_Addit)
		self.positions+=other_Addit.positions

	def add_position(self,pos):
		self.positions.append(pos)

	def __str__(self):
		return(self.name+" "+str(self.positions))

	def parse_line(self,line):
		self.positions.append([float(x) for x in list(line.split(" "))])

	def write_to_file(self,file):
		for i in self.positions:
			file.write(str(self.positions[0])+" "+str(self.positions[1])+"\n")

#untested
class Labels(Additional):
	def __init__(self,coord_obj,labels):
		super().__init__(coord_obj)
		self.labels=labels;
		self.name="Labels"

	def combine_with(self,other_Addit):
		super().combine_with(other_Addit)
		self.labels+=other_Addit.labels

	def __str__(self):
		return(self.name+" "+str(self.labels))

	def parse_line(self,line):
		self.labels.append(int(line))

	def write_to_file(self,file):
		for i in self.labels:
			file.write(str(i)+"\n")



class Coords:
	def __init__(self):
		self.labels = []
		self.coords = []
		self.c_number = 0
		self.c_positions = []

	def assimilate(self,other_coords):
		self.coords = self.coords+other_coords.coords
		self.c_number = self.c_number+other_coords.c_number
		self.c_positions = self.c_positions+other_coords.c_positions
		max_label = max(self.labels)
		self.labels = self.labels + [x+max_label for x in other_coords.labels]

	def write_file(self,filename):
		f = open(filename,'w')
		f.write(str(self))
		"""
		f.write('coords\n')
		for element in self.coords:
			f.write(str(element[0])+' '+str(element[1])+'\n')
		f.write('labels\n')
		for element in self.labels:
			f.write(str(element)+'\n')
		f.write('c_number\n')
		f.write(str(self.c_number)+'\n')
		f.write('c_positions\n')
		for element in self.c_positions:
			f.write(str(element[0])+' '+str(element[1])+'\n')
		"""

	def read_file(self,filename):
		f = open(filename,'r')
		modes =["coords","labels","c_number","c_positions"]
		mode = None
		for line in f:
			line = line.strip("\n")
			print(repr(line))
			if line in modes:
				mode = line
			else:
				line = [float(x) for x in line.split(" ")]
				if mode == "coords":
					self.coords.append(line)
				elif mode == "c_positions":
					self.c_positions.append(line)
				elif mode == "c_number":
					self.c_number = int(line[0])
				elif mode == "labels":
					self.labels.append(int(line[0]))

	def __str__(self):
		out =""
		out = out + 'coords\n'
		for element in self.coords:
			out = out + str(element[0])+' '+str(element[1])+'\n'
		out = out + 'labels\n'
		for element in self.labels:
			out = out + str(element)+'\n'
		out = out + 'c_number\n'
		out = out + str(self.c_number)+'\n'
		out = out + 'c_positions\n'
		for element in self.c_positions:
			out = out + str(element[0])+' '+str(element[1])+'\n'
		return out
