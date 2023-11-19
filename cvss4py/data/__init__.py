__all__ = ["metric_values", "metric_categories", "metric_defaults"]

def __dir__():
    return __all__

def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)
    return globals()[name]

import json
import pkgutil

raw_data = pkgutil.get_data("cvss4py", "data/metric_data.json")

metric_data = json.loads(raw_data)

metric_values = metric_data['metric_values']
metric_categories = metric_data['metric_categories']
metric_defaults = metric_data['metric_defaults']