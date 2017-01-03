from collections import OrderedDict


def recursive_dict_update(original, new):
    for key, value in original.items(): 
        if not key in new:
            new[key] = value
        elif isinstance(value, dict):
            value = OrderedDict(sorted(value.items()))
            recursive_dict_update(value, new[key])

    return new