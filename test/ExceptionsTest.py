from sage.all import *
from gns import *

import unittest


class ExceptionsTest(unittest.TestCase):
    def setUp(self):
        self.debug = True

    def test_FullResidueSystemException_2d_4digits(self):
        with self.assertRaises(FullResidueSystemException):
            m = Matrix(ZZ, [[2, -1], [1, 2]])
            digits = [[0, 0], [1, 0], [0, 1], [0, -1]]
            SemiRadixSystem(m, digits, operator=AlwaysExceptionOperator(), check_crs_property=True)

    def test_FullResidueSystemException_2d_5digits(self):
        with self.assertRaises(FullResidueSystemException):
            m = Matrix(ZZ, [[1, -3], [1, 2]])
            digits = [[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]]
            SemiRadixSystem(m, digits, operator=AlwaysExceptionOperator(), check_crs_property=True)

    def test_ExpansivityException(self):
        with self.assertRaises(ExpansivityException):
            m = Matrix(ZZ, [[0, -1], [1, 2]])
            digits = [[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]]
            SemiRadixSystem(m, digits, operator=AlwaysExceptionOperator(), check_expansivity_property=True)

    def test_UnitConditionException(self):
        with self.assertRaises(UnitConditionException):
            m = Matrix(ZZ, [[0, 2], [1, 0]])
            digits = [[0, 0], [1, 0]]
            SemiRadixSystem(m, digits, operator=AlwaysExceptionOperator(), check_unit_condition=True)


if __name__ == "__main__":
    unittest.TextTestRunner(sys.stderr, True, 1, False, False, None).run(
        unittest.TestLoader().loadTestsFromTestCase(ExceptionsTest))
