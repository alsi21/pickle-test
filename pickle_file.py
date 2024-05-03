
import unittest
import pickle
import numpy as np
from math import pi
from copy import deepcopy
from numpy.testing import assert_array_equal
import sys
import os
import pandas as pd

versionName = 'test'

n = len(sys.argv)
for i in range(1, n):
    print(sys.argv[i], end = " ")


test_case_dict = {"int": 3786587, "float": float(10/11), "float_nan": float('nan'), "float_inf": float('inf'), "complex": complex(5,3), 
                  "string": "test\n\t\r", "f_string": f"fstring", "r_string": r"rstring", "b_string": b"bstring",
                  "tuple": (1, (2)), "frozenset": frozenset([1,2,3,4]), "range": range(8), 
                  "bytes": bytes(5), "False": False, "None": None}


directory = "PickleFileV" + versionName
try:
    os.mkdir(directory) 
except:
    pass

hashes = {"key": [], "hash": []}
for key, value in test_case_dict.items():

    with open(f'{directory}/{key}','wb') as p_file:
        pickle.dump(value, p_file)
    hashes["key"].append(key)
    hashes["hash"].append(hash(value))
    
df = pd.DataFrame.from_dict(hashes)
df.to_csv(f'{directory}/hashes.csv')


