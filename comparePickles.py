import unittest
import pickle
import sys
import os
import platform
import json
from pathlib import Path

local_dir = "Pickles"
operation_system = platform.system()
if operation_system == "Darwin":
    operation_system = "MacOS"
python_version = sys.version.split()[0]

error_dict = {}

my_path = Path(f"{local_dir}/{operation_system}/{python_version}")
print(my_path)

class Class1:
    x = 5
    string = "Hello"

class Class2:
    nan = float('nan')

class Class3:
    child1 = Class1()
    child2 = Class2()

class Class4:
    dictionary = {"child3": Class1(), "child4": Class2()}

test_case_dict = {"int": 3786587, "float": float(10/11), "float_nan": float('nan'), "float_inf": float('inf'), "complex": complex(5,3), 
                  "string": "test\n\t\r", "f_string": f"fstring", "r_string": r"rstring", "b_string": b"bstring",
                  "tuple": (1, (2)), "frozenset": frozenset([1,2,3,4]), "range": range(8), 
                  "bytes": bytes(5), "False": False, "None": None, "list": [1, "2", True, ((4, 5), 6)], "list_in_list": [[], [[]]], 
                  "dict": {"value_here": 1, "dict_in_dict_in_dict": {"Not_empty": "David är elak mot mig :("}}, "set": {"Sebbe", "David", "Albin"}, 
                  "byte_array": bytearray("We are not alergic to peanuts", 'utf-8'),
                  "class1": Class1(), "class2": Class2(), "class3": Class3(), "class4": Class4()}



my_unpacked = {}
my_binary = {}
my_obj_hash = {}
for test in test_case_dict:
    with open(Path(f"{my_path}/{test}.pkl"), "rb") as f:
        my_unpacked[test] = pickle.load(f)
    with open(Path(f"{my_path}/{test}.pkl"), "rb") as f:
        my_binary[test] = hash(f.read())
    with open(Path(f"{my_path}/{test}.pkl"), "rb") as f:
        try:
            my_obj_hash[test] = hash(pickle.load(f))
        except:
            pass


master = {}
for (dirpath, dirnames, filenames) in os.walk(local_dir):
    if operation_system == "Windows":
        dirpath_list = dirpath.split("\\")
    else:
        dirpath_list = dirpath.split("/")
    print(dirpath)
    if len(dirpath_list) < 2:
        continue
    if len(filenames) == 0:
        continue
    print(dirpath)
    other_os = dirpath_list[-2]
    other_python_version = dirpath_list[-1]
    other_unpacked = {}
    other_binary = {}
    other_obj_hash = {}
    for test in test_case_dict:
        with open(Path(f"{dirpath}/{test}.pkl"), "rb") as f:
            other_unpacked[test] = pickle.load(f)
        with open(Path(f"{dirpath}/{test}.pkl"), "rb") as f:
            other_binary[test] = hash(f.read())
        with open(Path(f"{dirpath}/{test}.pkl"), "rb") as f:
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


class test_compare_datatype(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_obj_equality(self):
        global error_dict
        for operating_sys in master:
            for version in master[operating_sys]:
                for test in master[operating_sys][version]["unpacked"]:
                    msg = f'os:{operation_system} vs. {operating_sys}, py-ver:{python_version} vs. {version}'
                    with self.subTest(msg=msg):
                        try:
                            self.assertEqual(master[operating_sys][version]["unpacked"][test], my_unpacked[test])
                        except:
                            error_key = f"object_equality-{test}"
                            if error_key not in error_dict.keys():
                                error_dict[error_key] = []
                            error_dict[error_key].append(f'{msg} | values: {master[operating_sys][version]["unpacked"][test]} != {my_unpacked[test]}')
                        

    def test_binary_hash(self):
        global error_dict
        for operating_sys in master:
            for version in master[operating_sys]:
                for test in master[operating_sys][version]["binary"]:
                    msg = f'os:{operation_system} vs. {operating_sys}, py-ver:{python_version} vs. {version}'
                    with self.subTest(msg=msg):
                        try:
                            self.assertEqual(master[operating_sys][version]["binary"][test], my_binary[test])
                        except:
                            error_key = f"pickle_hash-{test}"
                            if error_key not in error_dict.keys():
                                error_dict[error_key] = []
                            error_dict[error_key].append(f'{msg} | values: {master[operating_sys][version]["binary"][test]} != {my_binary[test]}')

    def test_obj_hash(self):
        global error_dict
        for operating_sys in master:
            for version in master[operating_sys]:
                for test in master[operating_sys][version]["obj_hash"]:
                    msg = f'os:{operation_system} vs. {operating_sys}, py-ver:{python_version} vs. {version}'
                    with self.subTest(msg=msg):
                        try:
                            self.assertEqual(master[operating_sys][version]["obj_hash"][test], my_obj_hash[test])
                        except:
                            error_key = f"object_hash-{test}"
                            if error_key not in error_dict.keys():
                                error_dict[error_key] = []
                            error_dict[error_key].append(f'{msg} | values: {master[operating_sys][version]["obj_hash"][test]} != {my_obj_hash[test]}')

if __name__ == '__main__':

    try:
        with open('error_dict.txt', 'r') as f: 
            error_dict = json.load(f)
    except:
        pass

    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_compare_datatype)

    # with open("log_dump.txt", "w") as f:
    test_runner = unittest.TextTestRunner()

    test_runner.run(test_suite)
    print('Master')
    print(master)
    print('My...')
    print(my_unpacked)
    print(my_binary)
    print(my_obj_hash)

    print('Errors')
    print(error_dict)
    with open('error_dict.txt', 'w') as f: 
        f.write(json.dumps(error_dict))