import warnings
from .data import metric_categories, metric_values, metric_defaults

def vector_str_to_object(vector_str):
    raw_obj = dict([met_val.split(":") for met_val in vector_str.split("/")])
    validated_obj = {}
    modified_mets = {}
    # Loop through the string and make sure all the metrics and objects are valid
    # We'll save off the modified metrics and overwrite later
    for (met, val) in raw_obj.items():
        assert met in metric_values
        assert val in metric_values[met]
        if met.startswith("M"):
            modified_mets[met] = val
        else:
            validated_obj[met] = val
    
    # Include modified versions, warn if both metric and modified version and included
    for met,val in modified_mets.items():
        new_met = met[1:]
        if new_met in validated_obj:
            # Maybe shouldn't warn here.
            warnings.warn(f"Metric {new_met} and modified metric {met} both included in vector string, using {met} value {val}")
        validated_obj[new_met] = val

    # Now let's check to see if the metrics with defaults are included and insert defaults if needed
    for met in metric_defaults:
        # If it's included and is X or isn't in there
        if validated_obj.get(met, "X") == "X":
            validated_obj[met] = metric_defaults[met]
    
    # Make sure we've got everything we need to score.
    required_mets = metric_categories['base'] + ["CVSS", "E", "CR", "IR", "AR"]
    assert set(required_mets).issubset(set(validated_obj.keys()))

    return validated_obj