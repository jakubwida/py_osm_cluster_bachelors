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


#source of below: http://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
def _on_segment(p,q,r):
	if (q[0] <= max((p[0], r[0])) and q[0] >= min((p[0], r[0])) and q[1] <= max((p[1], r[1])) and q[1] >= min((p[1], r[1]))):
		return True
	else:
		return False

def _orientation(p,q,r):
	val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
	if val == 0:
		return 0
	elif val > 0:
		return 1
	else:
		return 2


def are_segments_intersecting(a1,a2,b1,b2):
	o1 = _orientation(a1, a2, b1)
	o2 = _orientation(a1, a2, b2)
	o3 = _orientation(b1, b2, a1)
	o4 = _orientation(b1, b2, a2)

	if o1 != o2 and o3 !=o4:
		return True
	elif o1 == 0 and _on_segment(a1,b1,a2):
		return True
	elif o2 == 0 and _on_segment(a1,b2,a2):
		return True
	elif o3 == 0 and _on_segment(b1,a1,b2):
		return True
	elif o4 == 0 and _on_segment(b2,a2,b2):
		return True
	else:
		return False
