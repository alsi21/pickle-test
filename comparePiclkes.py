import pickle
import sys
import os
import platform

local_dir = "Pickles"
operation_system = platform.system()
if operation_system == "Darwin":
    operation_system = "MacOS"
python_version = sys.version.split()[0]

my_path = f"{local_dir}/{operation_system}/{python_version}"

test_case_dict = {"int": 3786587, "float": float(10/11), "float_nan": float('nan'), "float_inf": float('inf'), "complex": complex(5,3), 
                  "string": "test\n\t\r", "f_string": f"fstring", "r_string": r"rstring", "b_string": b"bstring",
                  "tuple": (1, (2)), "frozenset": frozenset([1,2,3,4]), "range": range(8), 
                  "bytes": bytes(5), "False": False, "None": None, "list": [1, "2", True, ((4, 5), 6)], "list_in_list": [[], [[]]], 
                  "dict": {"value_here": 1, "dict_in_dict_in_dict": {"Not_empty": "David är elak mot mig :("}}}

my_unpacked = {}
my_binary = {}
my_obj_hash = {}
for test in test_case_dict:
    with open(f"{my_path}/{test}.pkl", "rb") as f:
        my_unpacked[test] = pickle.load(f)
        my_binary[test] = hash(f.read())
        try:
            my_obj_hash[test] = hash(pickle.load(f))
        except:
            pass


master = {}
for (dirpath, dirnames, filenames) in os.walk(local_dir):
    print(f"Path: {dirpath}; dirs: {dirnames}; files: {filenames}")
    other_os = dirpath.split("/")[-2]
    other_python_version = dirpath.split("/")[-1]
    other_unpacked = {}
    other_binary = {}
    other_obj_hash = {}
    for file in filenames:
        for test in test_case_dict:
            with open(f"{my_path}/{test}.pkl", "rb") as f:
                other_unpacked[test] = pickle.load(f)
                other_binary[test] = hash(f.read())
                try:
                    other_obj_hash[test] = hash(pickle.load(f))
                except:
                    pass
    if other_os not in master.keys():
        master[other_os] = {}
    if other_python_version not in master[other_os].keys():
        master[other_os][other_python_version] = {}
    master[other_os][other_python_version]["unpacked"] = other_unpacked
    master[other_os][other_python_version]["binary"] = other_binary
    master[other_os][other_python_version]["obj_hash"] = other_obj_hash

print(master)


