from itertools import product
from statistics import mean

from .data import eq_class_scores, eq_class_values, eq_class_max_subvectors, eq_class_max_distance, metric_distances, eq_class_metrics
from .transform import *
from .classes import InvalidEqClass

def score_eq_class(eq_class, validate=True):
    if validate and not eq_class in eq_class_scores:
        raise InvalidEqClass("Invalid equivalence class")
    else:
        return eq_class_scores[eq_class]

def next_lower_eq_classes(eq_class):
    eq_list = [int(eq_c) for eq_c in eq_class]
    next_lowers = {}
    for i in [1, 2, 4, 5]:
        eq = eq_list[i-1]
        if eq + 1 in eq_class_values[i-1]:
            next_lower = eq_list.copy()
            next_lower[i-1] = eq + 1
            next_lowers['eq' + str(i)] = "".join(map(str, next_lower))
        else:
            next_lowers['eq' + str(i)] = None
    nl_eq36 = eq_list.copy()
    eq36 = eq_class[2] + eq_class[5]
    if eq36 == '11':
        nl_eq36[2] = 2
    elif eq36 == '01':
        nl_eq36[2] = 1
    elif eq36 == '10':
        nl_eq36[5] = 1
    elif eq36 == '00':
        next_lower_left = eq_list.copy()
        next_lower_right = eq_list.copy()
        next_lower_left[2] = 1
        next_lower_right[5] = 1
        left_score = score_eq_class("".join(map(str, next_lower_left)))
        right_score = score_eq_class("".join(map(str, next_lower_right)))
        if left_score > right_score:
            nl_eq36 = next_lower_left
        else:
            nl_eq36 = next_lower_right
    else:
        nl_eq36 = None
    if nl_eq36 is not None:
        next_lowers['eq36'] = "".join(map(str, nl_eq36))
    else:
        next_lowers['eq36'] = None
    return next_lowers

def severity_distance(vector1, vector2, drop_any_negative=False):
    if isinstance(vector1, str):
        vector1 = vector_str_to_object(vector1, validate_vector=False, warn_modified=False)
    if isinstance(vector2, str):
        vector2 = vector_str_to_object(vector2, validate_vector=False, warn_modified=False)
        
    distances = {}
    required_mets = metric_categories['base'] + ["E", "CR", "IR", "AR"]

    for metric in required_mets:
        distances[metric] = metric_distances[metric][vector1[metric]] - metric_distances[metric][vector2[metric]]
    return distances
    


def score_vector(vector, validate_vector=True, warn_modified=True, replace_default=True):
    v = vector_str_to_object(vector, validate_vector=validate_vector, warn_modified=warn_modified, replace_default=replace_default)
    is_zero = all([v[m] == 'N' for m in ["VC", "VI", "VA", "SC", "SI", "SA"]])
    if is_zero:
        return 0
    eq_c = vector_to_equivalence_class(v)
    assert is_valid_eq_class(eq_c)
    
    eq_d = {'eq36':eq_c[2] + eq_c[5]}
    for i in [1, 2, 4, 5]:
        eq_d['eq' + str(i)] = eq_c[i-1]

    #print("Macrovector: ", eq_c)
    
    base_score = score_eq_class(eq_c) 
    next_lowers = next_lower_eq_classes(eq_c)
    next_lower_scores = {eq:score_eq_class(eq_c) if eq_c is not None else None for (eq, eq_c) in next_lowers.items()}
    score_differences =  {eq:base_score-eq_s if eq_s is not None else None for (eq, eq_s) in next_lower_scores.items()}

    #print("Base Score: ", base_score)
    #print("Next Lowers: ", next_lowers)
    #print("Next lower scores: ", next_lower_scores)

    maxes_lists = []
    for eq in next_lowers:
        maxes_lists.append(eq_class_max_subvectors[eq][eq_d[eq]])

    candidate_maxes = product(*maxes_lists)
    for candidate_max in candidate_maxes:
        distances = severity_distance(v, "/".join(candidate_max))
        if not any([d < 0 for d in distances.values()]):
            break
    
    #print("Distances: ", distances)

    eq_severity_distance = {}
    for eq in eq_d:
        eq_severity_distance[eq] = 0
        for metric in eq_class_metrics[eq]:
            eq_severity_distance[eq] += distances[metric]
    
    #print("eq_severity_distance ", eq_severity_distance)
    max_dists = {eq:eq_class_max_distance[eq][eq_d[eq]] for eq in eq_d}
    #print("max_dists", max_dists)

    #print("Available Distance", score_differences)

    perc_eq_severity_distance = {}
    for eq,d in eq_severity_distance.items():
        perc_eq_severity_distance[eq] = d/max_dists[eq]

    #print("Perc_eq_severity_dist", perc_eq_severity_distance)

    adjustments = {}
    for eq,p in perc_eq_severity_distance.items():
        if score_differences[eq] is not None:
            adjustments[eq] = p*score_differences[eq]
        else:
            adjustments[eq] = None

    #print("Adjustments: ", adjustments)

    adjustments_to_mean = [a for a in adjustments.values() if a is not None]
    if len(adjustments_to_mean) == 0:
        total_adjustment = 0.0
    else:
        total_adjustment = mean(adjustments_to_mean)

    #print("Total Adjustments: ", total_adjustment)

    return round(base_score-total_adjustment, 1)
    
    

