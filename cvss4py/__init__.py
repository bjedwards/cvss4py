import json
import pkgutil

metric_fname = pkgutil.get_data("data", "metric_data.json")

with open(metric_fname, "r") as f:
    metric_data = json.load(f)

