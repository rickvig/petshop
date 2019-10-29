import unittest

def soma(x, y):
    return x + y

class Test(unittest.TestCase):
    
    def test_1(self):
        print('Test exemplo 1')
        self.assertEqual(4, soma(2, 2))

    def test_2(self):
        print('Test exemplo 2')
        self.assertEqual(4444, soma(2222, 2222))