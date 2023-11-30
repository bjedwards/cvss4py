import warnings

from .data import metric_defaults, metric_categories, metric_values, eq_class_values
from .classes import UnknownMetric, UnknownMetricValue, MissingMetric

def is_valid_vector(vector, default_is_valid = True, verbose = False):
    if isinstance(vector, str):
        try:
            vector = dict([met_val.split(":") for met_val in vector.split("/")])
        except:
            warnings.warn("Unable to parse vector string", SyntaxWarning)
            return False

    if default_is_valid:
        for met in metric_defaults:
            # If it's included and is X or isn't in there
            if vector.get(met, "X") == "X":
                vector[met] = metric_defaults[met]
    
    for (met, val) in vector.items():
        if (met not in metric_values) and verbose:
            warnings.warn(f"Metric '{met}' in vector, but is not a recognized metric", UnknownMetric)
        else:
            if val not in metric_values[met]:
                if verbose:
                    warnings.warn(f"Metric '{met}' has unrecognized value '{val}'. Valid values are {metric_values[met]}", UnknownMetricValue)
                return False

            else:
                if (val=='X') and not default_is_valid:
                    if verbose:
                        warnings.warn(f"Metric {met} has default value 'X', and 'default_is_valid==False'.", UserWarning)
                    return False

    
    required_mets = metric_categories['base'] + ["CVSS", "E", "CR", "IR", "AR"]
    
    missing_metrics = set(required_mets).difference(set(vector.keys()))
    if missing_metrics:
        if verbose:
            warnings.warn(f"Missing required metrics: {missing_metrics}", MissingMetric)
        return False
    return True

def vector_str_to_object(vector_str, validate_vector=True, warn_modified=True, replace_default=True):
    try:
        raw_obj = dict([met_val.split(":") for met_val in vector_str.split("/")])
    except:
        raise SyntaxError("Unable to parse vector string")

    if validate_vector:
        with warnings.catch_warnings():
            warnings.simplefilter("error", category=UnknownMetricValue)
            warnings.simplefilter("error", category=MissingMetric)
            is_valid = is_valid_vector(raw_obj, verbose=True)
    
    final_obj = {}
    modified_mets = {}

    # We'll save off the modified metrics and overwrite later
    for (met, val) in raw_obj.items():
        if met.startswith("M"):
            modified_mets[met] = val
        else:
            final_obj[met] = val
    
    # Include modified versions, warn if both metric and modified version and included
    for met,val in modified_mets.items():
        new_met = met[1:]
        if (new_met in final_obj) and warn_modified:
            # Maybe shouldn't warn here.
            warnings.warn(
                f"Metric {new_met} and modified metric {met} both included in vector string, using {met} value {val}",
                UserWarning
            )
        final_obj[new_met] = val

    # Now let's check to see if the metrics with defaults are included and insert defaults if needed
    for met in metric_defaults:
        # If it's included and is X or isn't in there
        if (final_obj.get(met, "X") == "X") and replace_default:
            final_obj[met] = metric_defaults[met]
    


    return final_obj

def vector_to_equivalence_class(vector):
    if isinstance(vector, str):
        vector = vector_str_to_object(vector)
    
    if vector['AV'] == "N" and\
       vector["PR"] == "N" and\
       vector["UI"] == "N":
        eq1 = 0
    elif vector["AV"] != "P" and\
         (vector["AV"] == "N" or\
          vector["PR"] == "N" or\
          vector["UI"] == "N"):
        eq1 = 1
    else:
        eq1 = 2

    if vector['AC'] == "L" and\
       vector['AT'] == "N":
       eq2 = 0
    else:
        eq2 = 1
    
    if vector["VC"] == "H" and\
       vector["VI"] == "H":
        eq3 = 0
    elif vector["VC"] == "H" or\
         vector["VI"] == "H" or\
         vector["VA"] == "H":
        eq3 = 1
    else:
        eq3 = 2
    
    if vector["SI"] == "S" or\
       vector["SA"] == "S":
        eq4 = 0
    elif vector["SC"] == "H" or\
         vector["SI"] == "H" or\
         vector["SA"] == "H":
        eq4 = 1
    else:
        eq4 = 2

    if vector["E"] == "A":
        eq5 = 0
    elif vector["E"] == "P":
        eq5 = 1
    else:
        eq5 = 2
    
    if (vector["CR"] == "H" and vector["VC"] == "H") or\
       (vector["IR"] == "H" and vector["VI"] == "H") or\
       (vector["AR"] == "H" and vector["VA"] == "H"):
        eq6 = 0
    else:
        eq6 = 1
    
    return "".join(map(str, [eq1, eq2, eq3, eq4, eq5, eq6]))

def is_valid_eq_class(eq_class):
    eq_list = [int(eq_c) for eq_c in eq_class]
    valid_values = all([(eq_c in eq_class_values[i]) for (i, eq_c) in enumerate(eq_list)])
    return valid_values and not (eq_list[2]==2 and eq_list[5]==0)