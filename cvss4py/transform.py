from .data import metric_defaults
from .classes import UnknownMetric, UnknownMetricValue, MissingMetric

def vector_str_to_object(vector_str, validate_vector=True, warn_modified=True, replace_default=True):
    raw_obj = dict([met_val.split(":") for met_val in vector_str.split("/")])
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
            raise UserWarning(f"Metric {new_met} and modified metric {met} both included in vector string, using {met} value {val}")
        final_obj[new_met] = val

    # Now let's check to see if the metrics with defaults are included and insert defaults if needed
    for met in metric_defaults:
        # If it's included and is X or isn't in there
        if (final_obj.get(met, "X") == "X") and replace_default:
            final_obj[met] = metric_defaults[met]
    
    if validate_vector:
        with warnings.catch_warnings():
            warnings.filterwarnings("error", UnknownMetricValue)
            warnings.filterwarnings("error", MissingMetric)
            is_valid = is_valid_vector(final_obj, verbose=True)

    return final_obj