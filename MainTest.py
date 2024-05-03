import unittest
import pickle
from math import pi
from datetime import datetime
import sys

sys.set_int_max_str_digits = 10**1000000


# str
# int
# bool
# float
# tuple
# frozenset
# range

def function(lst: list):
    pass

class Class1():
    pass
    
class Class2():
    x = 1
    y = 2

class Class3():
    def classFunction():
        pass

class test_pickle_datatype(unittest.TestCase): #immutable går inte att hashea
    
    def test_hash(self):
        test_cases = [float(10/11), float(pi), 'Hello World', 'Test\n\t\r', f"", r"", b"", (1, 2), ((()),(),((()),())), 1, False, frozenset([1, 2, 3, 4]), range(8), complex(5, 3), None, float('nan'), float('inf'), float(100000**1000000/11), function([]), Class1(), Class2(), Class3(), range(10**100000)] #lägg in cases här

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
    
    def class_test(self):
        c = Class1()
        c.x = 1
        c.y = 2

        expected = hash(c)

        pickled = pickle.dumps(c)
        un_pickled = pickle.loads(pickled)
        
        actual = hash(un_pickled)
        self.assertEqual(expected, actual, f'class_test {c}')
    
    def test_object_in_list_permanence(self):
        lst = [1, "2", (3, 4), 5.6]
        pickled = pickle.dumps(lst)
        unpickled = pickle.loads(pickled)

        for i in range(len(lst)):
            excpected = hash(lst[i])
            value = hash(unpickled[i])
            self.assertEqual(excpected, value, f'{lst[i]}')

            


    def test_list_in_list(self):
        pass

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
        pass


    
    

if __name__ == '__main__':
    unittest.main()