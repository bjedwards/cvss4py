def vector_str_to_object(vector_str):
    raw_obj = dict([met_val.split(":") for met_val in vector_str.split("/")])
    return raw_obj