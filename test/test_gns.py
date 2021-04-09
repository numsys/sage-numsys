from sage.all import *
from gns import *

import unittest


class GnsTestCase(unittest.TestCase):

    def test_is_not_gns_canonical_digits_1(self):
        m = Matrix(ZZ, [[0, 2], [1, 0]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)
        
        self.assertFalse(numsys.is_gns())

    def test_is_not_gns_canonical_digits_2(self):
        m = Matrix(ZZ, [[20, 463], [1, 21]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertFalse(numsys.is_gns())

    def test_is_not_gns_digits_1(self):
        m = Matrix(ZZ, [[2, -1, 0, 0], [1, 2, 0, 0], [0, 0, 3, -1], [0, 0, 1, 3]])
        digits = [
                    [x[0], x[1], x[0], x[1]]
                    for x in
                    [
                        Matrix(ZZ, [[2, -1], [1, 2]]) * vector(d2) + vector(d1)
                        for d2 in [
                            [0, 0], [1, 0], [-1, -1], [0, -1],
                            [1, -1], [1, 2], [-1, 1], [0, 1],
                            [1, 1], [-1, 0]
                        ]
                        for d1 in [
                            [0, 0], [1, 0], [0, -1], [0, 1], [-1, 0]
                        ]
                    ]
                ]
        numsys = SemiRadixSystem(m, digits)

        self.assertFalse(numsys.is_gns())

    def test_is_not_gns_2(self):
        m = Matrix(ZZ, [[3]])
        digits = Digits([[0], [7], [2]])
        numsys = SemiRadixSystem(m, digits)

        self.assertFalse(numsys.is_gns())

    def test_is_not_gns_simultaneous_number_system(self):
        numsys = SimultaneousSystem([
                        SemiRadixSystem([[2, -1], [1, 2]], AdjointDigits()),
                        SemiRadixSystem([[3, -1], [1, 3]], AdjointDigits())])

        self.assertFalse(numsys.is_gns())

    def test_is_gns_canonical_digits(self):
        m = Matrix(ZZ, [[-3, 1], [1, -2]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertTrue(numsys.is_gns())

    def test_is_gns_adjoint_digits_1(self):
        m = Matrix(ZZ, [[2, -1], [1, 2]])
        digits = AdjointDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertTrue(numsys.is_gns())

    def test_is_gns_M_A_0_2_ns(self):
        m = Matrix(ZZ, [[0, -2, 0, 0], [2, -2, 0, 0], [0, 0, 1, -2], [0, 0, 2, -1]])
        digits = Digits([[0, 0, 0, 0],      [1, 0, 1, 0],
                         [0, 2, 0, 2],      [1, 1, 1, 1],
                         [-1, 0, -1, 0],    [-2, 0, -2, 0],
                         [-1, -1, -1, -1],  [-2, -1, -2, -1],
                         [2, -1, 2, -1],    [-2, 1, -2, 1],
                         [-1, -2, -1, -2],  [-3, -3, -3, -3]])
        numsys = SemiRadixSystem(m, digits)

        self.assertTrue(numsys.is_gns())

    def test_is_gns_M_B_minus_2_minus_1_ns(self):
        m = Matrix(ZZ, [[-2, 1, 0, 0], [-1, -1, 0, 0], [0, 0, -2, 0], [0, 0, 0, -2]])
        digits =  Digits([[0, 0, 0, 0],     [1, 0, 1, 0],
                          [0, 2, 0, 2],     [0, 1, 0, 1],
                          [-2, 1, -2, 1],   [1, -2, 1, -2],
                          [-3, -1, -3, -1], [-2, 0, -2, 0],
                          [-1, -1, -1, -1], [-2, -1, -2, -1],
                          [-1, -2, -1, -2], [-3, -3, -3, -3]])
        numsys = SemiRadixSystem(m, digits)

        self.assertTrue(numsys.is_gns())

    def test_id_gns_symmetric_digits_1(self):
        m = Matrix(ZZ, [[0, 0, 0, -15], [1, 0, 0, -1], [0, 1, 0, -2], [0, 0, 1, -3]])
        digits = SymmetricDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertTrue(numsys.is_gns())

    def test_id_gns_symmetric_digits_2(self):
        m = Matrix(ZZ, [[0, 0, 0, 0, 0, 17], [1, 0, 0, 0, 0, 2],
                        [0, 1, 0, 0, 0,  2], [0, 0, 1, 0, 0, 1],
                        [0, 0, 0, 1, 0,  1], [0, 0, 0, 0, 1, 1]])
        digits = SymmetricDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertTrue(numsys.is_gns())


if __name__ == '__main__':
    unittest.TextTestRunner(sys.stderr, True, 1, False, False, None).run(
        unittest.TestLoader().loadTestsFromTestCase(GnsTestCase))
