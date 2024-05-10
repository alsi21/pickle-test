import pickle
import sys
import os
import platform

local_dir = "Pickles"
operation_system = platform.system()
if operation_system == "Darwin":
    operation_system = "MacOS"
python_version = sys.version.split()[0]

test_case_dict = {"int": 3786587, "float": float(10/11), "float_nan": float('nan'), "float_inf": float('inf'), "complex": complex(5,3), 
                  "string": "test\n\t\r", "f_string": f"fstring", "r_string": r"rstring", "b_string": b"bstring",
                  "tuple": (1, (2)), "frozenset": frozenset([1,2,3,4]), "range": range(8), 
                  "bytes": bytes(5), "False": False, "None": None, "list": [1, "2", True, ((4, 5), 6)], "list_in_list": [[], [[]]], 
                  "dict": {"value_here": 1, "dict_in_dict_in_dict": {"Not_empty": "David är elak mot mig :("}}}


directory = f"{local_dir}"
try:
    os.mkdir(directory) 
except:
    pass

directory = f"{local_dir}/{operation_system}"
try:
    os.mkdir(directory) 
except:
    pass

directory = f"{local_dir}/{operation_system}/{python_version}"
try:    
    os.mkdir(directory) 
except:
    pass

for key, value in test_case_dict.items():
    with open(f'{local_dir}/{operation_system}/{python_version}/{key}.pkl','wb') as p_file:
        pickle.dump(value, p_file, protocol=5)