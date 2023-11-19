import json
import pkgutil

data_dir = pkgutil.get_data("cvss4py", "data")

with open(data_dir + "metric_data.json", "r") as f:
    metric_data = json.load(f)

