from parameterized import parameterized
from sage.all import *
from gns import *

import unittest


class OrbitTestCase(unittest.TestCase):

    def test_orbit_O1(self):
        m = Matrix(ZZ, [[2, -1], [1, 2]])
        digits = Digits([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.get_orbit_from([-6, 5]), [[-6, 3], [-2, 2], [1, -2],
                                                          [0, -1], [0, 0], [0, 0]])

    def test_orbit_O2(self):
        m = Matrix(ZZ, [[1, -2], [1, 1]])
        digits = Digits([[0, 0], [1, 0], [-1, 0]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.get_orbit_from([3, 1]), [[3, 1], [2, -1], [0, -1],
                                                         [-1, 0], [0, 0], [0, 0]])

    def test_orbit_O3_symmetric_digits(self):
        m = Matrix(ZZ, [[1, -2], [1, 1]])
        digits = SymmetricDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.get_orbit_from([3, 1]), [[3, 1], [2, -1], [0, -1],
                                                         [-1, 0], [0, 0], [0, 0]])

    def test_orbit_O4(self):
        m = Matrix(ZZ, [[-1, -1], [1, -1]])
        digits = Digits([[0, 0], [1, 0]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.get_orbit_from([3, 1]), [[3, 1], [-1, -2], [0, 2],
                                                         [1, -1], [-1, 0], [1, 1],
                                                         [0, -1], [0, 1], [1, 0],
                                                         [0, 0], [0, 0]])

    def test_orbit_O5_canonical_digits(self):
        m = Matrix(ZZ, [[0, -2], [1, -2]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.get_orbit_from([2, 1]), [[2, 1], [-1, -1],
                                                         [1, 1], [1, 0],
                                                         [0, 0], [0, 0]])

    def test_orbit_O6_canonical_digits(self):
        m = Matrix(ZZ, [[0, 2], [1, 0]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.get_orbit_from([-1, 0]), [[-1, 0], [0, -1], [-1, 0]])

    def test_orbit_O7_canonical_digits(self):
        m = Matrix(ZZ, [[20, 463], [1, 21]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.get_orbit_from([-1, 0]), [[-1, 0], [21, -1], [-1, 0]])

    @parameterized.expand([
        ([3], [[3], [1], [1]]),
        ([7], [[7], [3], [1], [1]]),
    ])
    def test_orbit_O8(self, from_, expected):
        m = Matrix(ZZ, [[3]])
        digits = Digits([[-2], [0], [2]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.get_orbit_from(from_), expected)

    def test_orbit_4_dimension_constant_base_and_digits(self):
        m = Matrix(ZZ, [[0, 0, 0, 0, -7], [1, 0, 0, 0, 6], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.get_orbit_from([0, 1, 2, 3, 4]),
                         [[0, 1, 2, 3, 4], [1, 2, 3, 4, 0],
                          [2, 3, 4, 0, 0], [3, 4, 0, 0, 0],
                          [4, 0, 0, 0, 0], [0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0]])


if __name__ == '__main__':
    unittest.TextTestRunner(sys.stderr, True, 1, False, False, None).run(
        unittest.TestLoader().loadTestsFromTestCase(OrbitTestCase))
