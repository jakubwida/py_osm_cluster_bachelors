def parse_tags(osm_tree_child):
	tags={}
	for i in osm_tree_child:
			if i.tag == "tag":
				tags[i.attrib["k"]]=i.attrib["v"]
	return tags

def parse_members(osm_tree_child):
	members=[]
	for i in osm_tree_child:
			if i.tag == "member":
				members.append(i.attrib)
	return members
