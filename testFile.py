import unittest
from DuoBuddy import get_input


class TestFileName(unittest.TestCase):
    def test_get_input(self):
        x = get_input()
        self.assertNotEqual(x[0], None)
        
if __name__ == '__main__':
    unittest.main()