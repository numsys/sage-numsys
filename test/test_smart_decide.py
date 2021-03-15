import unittest
from sage.all import *
from gns import *


class SmartDecideTestCase(unittest.TestCase):
    def test_not_smart_decide_1(self):
        rs = SemiRadixSystem([[0, -7], [1, -7]], SymmetricDigits())
        self.assertFalse(rs.smart_decide())

    def test_smart_decide_2(self):
        rs = SemiRadixSystem([[0, 0, -2], [1, 0, -2], [0, 1, -2]], [[0, 0, 0], [1, 0, 0]])
        self.assertTrue(rs.smart_decide())


if __name__ == '__main__':
    unittest.TextTestRunner(sys.stderr, True, 1, False, False, None).run(
        unittest.TestLoader().loadTestsFromTestCase(SmartDecideTestCase))
