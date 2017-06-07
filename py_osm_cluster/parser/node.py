import xml.etree.ElementTree as etree
from py_osm_cluster.parser.tag_parse import *
from shapely.geometry import Point
class Node:
	def __init__(self,osm_tree_child):
		self.id = osm_tree_child.attrib["id"] # id unique in nodes
		self.lat = float(osm_tree_child.attrib["lat"]) #latitude (y)
		self.lon = float(osm_tree_child.attrib["lon"]) #longitude (x)
		self.tags = parse_tags(osm_tree_child) # dictionary of tags, where k= key, v = value
		self.geom = Point(self.lat,self.lon)
		#print("node wat")
