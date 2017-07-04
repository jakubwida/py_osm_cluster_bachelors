import scipy.spatial as spatial
import math


""" requires 2 coordinates, calculates euclidean distance between them"""
def distance(a,b):
	return math.sqrt(math.pow(a[0]-b[0],2)+math.pow(a[1]-b[1],2))


""" requires list of ccordinates, returns pairs of coordinates forming triangulation graph"""
def triangulate_set(coords):
	out = spatial.Delaunay(coords)
	alledges = set()
	for i in out.simplices:
		ab =frozenset((coords[i[0]],coords[i[1]]))
		bc =frozenset((coords[i[1]],coords[i[2]]))
		ca =frozenset((coords[i[2]],coords[i[0]]))
		alledges.add(ab)
		alledges.add(bc)
		alledges.add(ca)

	return [list(x) for x in alledges ]

""" requires list of ccordinates, returns pairs of coordinates, by their indexes, forming triangulation graph"""
def triangulate_set_labelling(coords):
	out = spatial.Delaunay(coords)
	alledges = set()
	for i in out.simplices:
		ab =frozenset((i[0],i[1]))
		bc =frozenset((i[1],i[2]))
		ca =frozenset((i[2],i[0]))
		alledges.add(ab)
		alledges.add(bc)
		alledges.add(ca)

	return [list(x) for x in alledges ]
