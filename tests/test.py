import json
from cvss4py import score_vector
from cvss4py.data import test_vectors

for d in test_vectors:
    pyscore = score_vector(d['vector'], warn_modified=False)
    if pyscore != d['official_score']:
        print(d['vector'] + " mismatch! cvss4py score: " + pyscore + ", official score: " + d['official_score'])