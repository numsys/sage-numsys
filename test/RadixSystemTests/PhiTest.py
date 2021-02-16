from sage.all import *
from gns import *

import unittest


class PhiTestCase(unittest.TestCase):

    # TODO Loggingot bevezetni (debug level) es ott kiirni a parametereket
    def test_phi_function_P1(self):
        m = Matrix(ZZ, [[2, -1], [1, 2]])
        digits = Digits([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function([-6, 5]), [0, 0])
        self.assertEqual(numsys.phi_function([-6, 4]), [-2, 3])
        self.assertEqual(numsys.phi_function([-6, 3]), [-2, 2])

    def test_phi_function_P2(self):
        m = Matrix(ZZ, [[1, -2], [1, 1]])
        digits = Digits([[0, 0], [1, 0], [-1, 0]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function([3, 2]), [2, 0])
        self.assertEqual(numsys.phi_function([1, 3]), [2, 1])
        self.assertEqual(numsys.phi_function([4, 3]), [3, 0])

    def test_phi_function_P3_symmetric_digits(self):
        m = Matrix(ZZ, [[1, -2], [1, 1]])
        digits = SymmetricDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function([3, 2]), [2, 0])
        self.assertEqual(numsys.phi_function([1, 3]), [2, 1])
        self.assertEqual(numsys.phi_function([4, 3]), [3, 0])

    def test_phi_function_P4(self):
        m = Matrix(ZZ, [[-1, -1], [1, -1]])
        digits = Digits([[0, 0], [1, 0]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function([3, 2]), [0, -2])
        self.assertEqual(numsys.phi_function([1, 3]), [1, -2])
        self.assertEqual(numsys.phi_function([4, 3]), [0, -3])

    def test_phi_function_P5_canonical_digits(self):
        m = Matrix(ZZ, [[0, 2], [1, 0]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function([-1, -1]), [-1, -1])
        self.assertEqual(numsys.phi_function([-1, 0]), [0, -1])

    @unittest.skip("not active")
    def _test_phi_function_P6_canonical_digits_not_active(self):
        m = Matrix(ZZ, [[20, 463], [1, 21]])
        digits = CanonicalDigits()
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function([-1, 0]), [21, -1])

    def test_phi_function_P7(self):
        m = Matrix(ZZ, [[3]])
        digits = Digits([[-2], [0], [2]])
        numsys = SemiRadixSystem(m, digits)

        self.assertEqual(numsys.phi_function([1]), [1])
        self.assertEqual(numsys.phi_function([0]), [0])


if __name__ == '__main__':
    unittest.TextTestRunner(sys.stderr, True, 1, False, False, None).run(
        unittest.TestLoader().loadTestsFromTestCase(PhiTestCase))
