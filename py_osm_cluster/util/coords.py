

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
			#print(repr(line))
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

	""" returns a dictionary where keys = label values, values = lists of coords under these labels"""
	def clusters_into_lists_dict(self):
		out = {}
		for num,i in enumerate(self.coords):
			label = self.labels[num]
			if label in out:
				out[label].append(i)
			else:
				out[label] = [i]
		return out
