import unittest
import pickle
import numpy as np
from math import pi
from copy import deepcopy
from numpy.testing import assert_array_equal
import random
import sys

# str
# int
# bool
# float
# tuple
# frozenset
# range


def function():
    pass

class Class1():
    pass


class test_pickle_datatype(unittest.TestCase): #immutable går inte att hasha
    
    def test_hash(self):
        test_cases = [float(10/11), float(pi), 'Hello World', 'Test\n\t\r', f"", r"", b"", (1, 2), ((()),(),((()),())), 1, False, frozenset([1, 2, 3, 4]), range(8), complex(5, 3), None, float('nan'), float('inf'), float(1e1000), function(), range(10**10), bytes(5), function] #lägg in cases här

        for i, test_case in enumerate(test_cases):
            with self.subTest(msg=f'{test_case}', i=i):

                expected = hash(test_case)
                
                # Packa ned
                pickled = pickle.dumps(test_case)
                
                # Packa upp
                un_pickled = pickle.loads(pickled)
                
                # Jämför
                actual = hash(un_pickled)
                self.assertEqual(expected, actual, f'{test_case}')
    
    
    def test_object_in_list_permanence(self):
        lst = [1, "2", (3, 4), 5.6]
        pickled = pickle.dumps(lst)
        unpickled = pickle.loads(pickled)

        for i in range(len(lst)):
            excpected = hash(lst[i])
            value = hash(unpickled[i])
            self.assertEqual(excpected, value, f'{lst[i]}')

            
    def test_list_equivalence(self):
        test_case_dict = {"simple list" : [1, "2", (3, 4), 5.6], "list with list" : [[], [[], []]], "really big list": random.sample(range(1, 100000000), 10000000)}
        # l = [1, 2, 3]
        # l.append(l)
        # test_case_dict["list containing itself"] = l

        for key, value in test_case_dict.items():
            pickled_list = pickle.dumps(value)
            unpickled = pickle.loads(pickled_list)
            self.assertEqual(value, unpickled, key)


    def test_nan_equivalent(self):
        # https://discuss.python.org/t/does-pickle-always-give-the-same-bytes/7468/4
        #>>> x = float('nan')
        # >>> y = x
        # >>> x == y
        #false

        x = float('nan')
        y = x

        x_hash = hash(pickle.loads(pickle.dumps(x)))
        y_hash = hash(pickle.loads(pickle.dumps(y)))

        self.assertEqual(x_hash, y_hash)
        self.assertEqual(hash(x), hash(y))


    def test_numpy_array(self):
        #https://discuss.python.org/t/pickle-original-data-size-is-greater-than-deserialized-one-using-pickle-5-protocol/23327

        #Någonting händer med "äganderätten" hos arrayer i numpy tydligen. Vet inte om det reflekteras på hashen men värt att kolla
        #LIKT FÖLJANDE:
        # array = np.array([1, 2, 3] * 10000)

        # packed_data = pkl.dumps(array)
        # unpacked_data = pkl.loads(packed_data)

        # array[0] = 1111111111111

        # print(array)
        # [1111111111111             2             3 ...             1             2
        #             3]
        # print(unpacked_data)
        # [1 2 3 ... 1 2 3]

        # print(sys.getsizeof(array))
        # # 240112
        # print(sys.getsizeof(unpacked_data))
        # # 112
        # print(all(np.equal(array, unpacked_data)))
        # False
        
        array = np.array([1, 2, 3] * 10000)
        packed_data = pickle.dumps(array)
        unpacked_data = pickle.loads(packed_data)

        assert_array_equal(array, unpacked_data, verbose=False)
        self.assertEqual(array.flags.owndata, unpacked_data.flags.owndata)


    
    

if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(test_pickle_datatype)

    # Create a test runner and specify the output file
    with open("test_results.txt", "w") as f:
        test_runner = unittest.TextTestRunner(stream=f, verbosity=2)
        
        # Run the test suite with the specified test runner
        result = test_runner.run(test_suite)