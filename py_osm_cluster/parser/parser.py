from py_osm_cluster.parser.node import *
from py_osm_cluster.parser.way import *
from py_osm_cluster.parser.relation import *
import xml.etree.ElementTree as etree
from  py_osm_cluster.util.coords import Coords as C
class Parser:
	def __init__(self,filename):
		self.nodes = {} #{id:node}
		self.ways = {} # {id:way}
		self.relations ={} # {id:relation}

		tree = etree.parse(filename)
		root = tree.getroot()

		for child in root:
			tag = child.tag
			if tag =="node":
				self.nodes[child.attrib["id"]]=Node(child)
			elif tag =="way":
				self.ways[child.attrib["id"]]=Way(child,self)
			#elif tag =="relation":
			#	self.relations[child.attrib["id"]]=Relation(child,self)

	def get_buildings_data_obj(self):
		out = C()
		for i in list(self.ways.values()):
			#print(i.tags)
			if "building" in i.tags and i.tags["building"]=="yes":
				out.coords.append(list(i.geom.centroid.coords)[0])
				#print("a building!")
		return out

	def get_buildings_by_address_nodes(self):
		out = C()
		for i in list(self.nodes.values()):
			#print(i.tags)
			if "addr:housenumber" in i.tags:
				out.coords.append(list(i.geom.coords)[0])
		return out
