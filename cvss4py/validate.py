from .data import metric_categories, metric_values
from .classes import UnknownMetric, UnknownMetricValue, MissingMetric
from .transform import vector_str_to_object

def is_valid_vector(vector, default_is_valid = True, verbose = False):
    if isinstance(vector, str):
        vector = vector_str_to_obj(vector, validate_vector=False, warn_modified=False)
    
    is_valid = True
    for (met, val) in vector.items():
        if (met not in metric_values) and verbose:
            raise UnknownMetric(f"Metric '{met}' in vector, but is not a recognized metric")
        if val not in metric_values[met]:
            is_valid = False
            if verbose:
                raise UnknownMetricValue(f"Metric '{met}' has unrecognized value '{val}'. Valid values are {metric_values[met]}")
        else:
            if (val=='X') and not default_is_valid:
                is_valid = False
                if verbose:
                    raise UserWarning(f"Metric {met} has default value 'X', and 'default_is_valid==False'.")
    
    required_mets = metric_categories['base'] + ["CVSS", "E", "CR", "IR", "AR"]
    missing_metrics = set(required_mets).issubset(set(validated_obj.keys()))
    if missing_metrics:
        is_valid=False
        if verbose:
            raise MissingMetric(f"Missing required metrics: {missing_metrics}")
    return is_valid