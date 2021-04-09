from sage.all import *
from gns import *

import unittest


class CoverBoxTestCase(unittest.TestCase):

    def test_cover_box_CB1(self):
        m = Matrix(ZZ, [[2, -1], [1, 2]])
        digits = Digits([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.compute_cover_box(), ([-2, -6], [2, 1]))

    def test_cover_box_CB2(self):
        m = Matrix(ZZ, [[1, -2], [1, 1]])
        digits = Digits([[0, 0], [1, 0], [-1, 0]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.compute_cover_box(), ([-1, -1], [1, 1]))

    def test_cover_box_CB3_symmetric_digits(self):
        m = Matrix(ZZ, [[1, -2], [1, 1]])
        digits = SymmetricDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.compute_cover_box(), ([-1, -1], [1, 1]))

    def test_cover_box_CB4(self):
        m = Matrix(ZZ, [[-1, -1], [1, -1]])
        digits = Digits([[0, 0], [1, 0]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.compute_cover_box(), ([-1, -1], [1, 1]))

    def test_cover_box_CB5(self):
        m = Matrix(ZZ, [[3]])
        digits = Digits([[-2], [0], [2]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.compute_cover_box(), ([-1], [1]))

    def test_cover_box_CB6_canonical_digits(self):
        m = Matrix(ZZ, [[0, -2], [1, -2]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.compute_cover_box(), ([-1, -1], [2, 1]))


if __name__ == '__main__':
    unittest.TextTestRunner(sys.stderr, True, 1, False, False, None).run(
        unittest.TestLoader().loadTestsFromTestCase(CoverBoxTestCase))
