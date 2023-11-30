__all__ = ["metric_values", "metric_categories", "metric_defaults", 
           "eq_class_values", "eq_class_scores", "eq_class_max_subvectors", "eq_class_metrics"]

def __dir__():
    return __all__

def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)
    return globals()[name]

import json
import pkgutil

raw_metric_data = pkgutil.get_data("cvss4py", "data/metric_data.json")

metric_data = json.loads(raw_metric_data)

metric_values = metric_data['metric_values']
metric_categories = metric_data['metric_categories']
metric_defaults = metric_data['metric_defaults']
metric_distances = metric_data['metric_distances']

raw_eq_data =  pkgutil.get_data("cvss4py", "data/eq_data.json")
eq_data = json.loads(raw_eq_data)

eq_class_metrics = eq_data['eq_class_metrics']
eq_class_max_subvectors = eq_data['eq_class_max_subvectors']
eq_class_values = eq_data['eq_class_values']
eq_class_scores = eq_data['eq_class_scores']
eq_class_max_distance = eq_data["eq_class_max_distances"]

