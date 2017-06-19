import sklearn.metrics as metrics


""" adjusted rand index - measures similarity between two clusterings"""
def scikit_rand_index(data_obj,model_obj):
	return metrics.adjusted_rand_score(model_obj.labels,data_obj.labels)

def scikit_completeness_score(data_obj,model_obj):
	return metrics.completeness_score(model_obj.labels,data_obj.labels)

def scikit_fowlkes_mallows_score(data_obj,model_obj,sparse=False):
	return metrics.fowlkes_mallows_score(model_obj.labels,data_obj.labels,sparse)

def scikit_homogeneity_score(data_obj,model_obj):
	return metrics.homogeneity_score(model_obj.labels,data_obj.labels)

def scikit_normalized_mutual_info_score(data_obj,model_obj):
	return metrics.normalized_mutual_info_score(model_obj.labels,data_obj.labels)

def scikit_v_measure_score(data_obj,model_obj):
	return metrics.v_measure_score(model_obj.labels,data_obj.labels)

def scikit_all_scores_dict(data_obj,model_obj):
	out ={}
	out["rand_index"]=scikit_rand_index(data_obj,model_obj)
	out["completeness_score"]=scikit_completeness_score(data_obj,model_obj)
	out["fowlkes_mallows_score"]=scikit_fowlkes_mallows_score(data_obj,model_obj)
	out["homogeneity_score"]=scikit_homogeneity_score(data_obj,model_obj)
	out["normalized_mutual_info_score"]=scikit_normalized_mutual_info_score(data_obj,model_obj)
	out["v_measure_score"]=scikit_v_measure_score(data_obj,model_obj)
	return out
