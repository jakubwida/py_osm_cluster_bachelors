import py_osm_cluster.util.statistic as statistic
import py_osm_cluster.eval.standalone as standalone
a = [1,3,5]
b= [0,10]

aa =[[0,0],[2,2]]
bb = [[0,0],[1,1],[2,2],[3,3],[4,4]]
"""
print(statistic.avg(a))
print(statistic.avg(b))
print(statistic.stdev_avg(a))
print(statistic.stdev_avg(b))
print("he he he")
print(statistic.avg_array(aa))
print(statistic.avg_array(bb))
print(statistic.stdev_avg_array(aa))
print(statistic.stdev_avg_array(bb))
"""

c = [(0,0),(2,0),(4,0)]

print(standalone.dataset_values(c))
