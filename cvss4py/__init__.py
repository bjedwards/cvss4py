__all__ = [
    "data", 
    "vector_str_to_object", 
    "is_valid_vector", 
    "vector_to_equivalence_class",
    "is_valid_eq_class",
    "score_eq_class",
    "next_lower_eq_classes",
    "score_vector"
]

def __dir__():
    return __all__

def __getattr__(name):
    if name not in __all__:
        raise AttributeError(name)
    return globals()[name]

from .data import *
from .transform import *
from .score import *