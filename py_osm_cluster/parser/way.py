import xml.etree.ElementTree as etree
from py_osm_cluster.parser.tag_parse import *

from shapely.geometry import LinearRing
from shapely.geometry import LineString
class Way:
	def __init__(self,osm_tree_child,parser):
		#print("way wat")
		self.parser =parser
		self.id = osm_tree_child.attrib["id"] # id unique in ways
		self.way_nodes=[]
		way_tuples=[]
		self.tags = parse_tags(osm_tree_child) # dictionary of tags, where k= key, v = value
		for i in osm_tree_child:
			if i.tag == "nd":
				node = self.parser.nodes[i.attrib["ref"]]
				self.way_nodes.append(node)
				way_tuples.append((node.lat,node.lon))
		self.geom =None
		if self.way_nodes[0]==self.way_nodes[-1]:
			self.geom = LinearRing(way_tuples)
		else:
			self.geom = LineString(way_tuples)
