from sage.all import *
from gns import *
from parameterized import parameterized

import unittest


class PhiTestCase(unittest.TestCase):

    @parameterized.expand([
        ([-6, 5], [0, 0]),
        ([-6, 4], [-2, 3]),
        ([-6, 3], [-2, 2])
    ])
    def test_phi_function_P1(self, from_, expected):
        m = Matrix(ZZ, [[2, -1], [1, 2]])
        digits = Digits([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function(from_), expected)

    @parameterized.expand([
        ([3, 2], [2, 0]),
        ([1, 3], [2, 1]),
        ([4, 3], [3, 0])
    ])
    def test_phi_function_P2(self, from_, expected):
        m = Matrix(ZZ, [[1, -2], [1, 1]])
        digits = Digits([[0, 0], [1, 0], [-1, 0]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function(from_), expected)

    @parameterized.expand([
        ([3, 2], [2, 0]),
        ([1, 3], [2, 1]),
        ([4, 3], [3, 0])
    ])
    def test_phi_function_P3_symmetric_digits(self, from_, expected):
        m = Matrix(ZZ, [[1, -2], [1, 1]])
        digits = SymmetricDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function(from_), expected)

    @parameterized.expand([
        ([3, 2], [0, -2]),
        ([1, 3], [1, -2]),
        ([4, 3], [0, -3])
    ])
    def test_phi_function_P4(self, from_, expected):
        m = Matrix(ZZ, [[-1, -1], [1, -1]])
        digits = Digits([[0, 0], [1, 0]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function(from_), expected)

    @parameterized.expand([
        ([-1, -1], [-1, -1]),
        ([-1, 0], [0, -1]),
    ])
    def test_phi_function_P5_canonical_digits(self, from_, expected):
        m = Matrix(ZZ, [[0, 2], [1, 0]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function(from_), expected)

    def _test_phi_function_P6_canonical_digits(self):
        m = Matrix(ZZ, [[20, 463], [1, 21]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function([-1, 0]), [21, -1])

    @parameterized.expand([
        ([1], [1]),
        ([0], [0]),
    ])
    def test_phi_function_P7(self, from_, expected):
        m = Matrix(ZZ, [[3]])
        digits = Digits([[-2], [0], [2]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function(from_), expected)


if __name__ == '__main__':
    unittest.TextTestRunner(sys.stderr, True, 1, False, False, None).run(
        unittest.TestLoader().loadTestsFromTestCase(PhiTestCase))
