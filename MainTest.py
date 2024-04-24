import unittest
import pickle
from math import pi

class test_pickle_datatype(unittest.TestCase):

    def test_hash(self):
        test_cases = [10/11, pi, 'Hello World', 'Test\n\t\r', (1,2), ((()),(),((()),())), float('nan')] #lägg in cases här

        for test_case in test_cases:
            expected = hash(test_case)
            pickled = pickle.dumps(test_case)
            un_pickled = pickle.loads(pickled)
            actual = hash(un_pickled)
            self.assertEqual(expected, actual, f'{test_case}')
            #packa ned, packa upp, jämför hash
    
    def test_list_in_list(self):
        pass

    def test_nan_equivalent(self):
        # https://discuss.python.org/t/does-pickle-always-give-the-same-bytes/7468/4
        #>>> x = float('nan')
        # >>> y = x
        # >>> x == y
        #false

        #Värt att testa för andra typer?
        pass

    def test_numpy_array(self):
        #https://discuss.python.org/t/pickle-original-data-size-is-greater-than-deserialized-one-using-pickle-5-protocol/23327

        #Någonting händer med "äganderätten" hos arrayer i numpy tydligen. Vet inte om det reflekteras på hashen men värt att kolla
        pass

    
    

if __name__ == '__main__':
    unittest.main()