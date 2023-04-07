from sage.all import *

from math import floor


class DigitsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Digits(object):
    def get_congruent_element(self, v, rs):
        """
        Computes the congruent element for a given point v
        """
        res = 0
        i = rs.dimension - 1
        smith_diagonal = rs.get_smith_diagonal_list()
        smith_u = rs.get_smith_u()
        while i >= 0 and smith_diagonal[i] > 1:
            s = 0
            for j in range(rs.dimension):
                s = s + smith_u[i, j] * v[j]
            res = res * smith_diagonal[i] + (s % smith_diagonal[i])
            i = i - 1
        return copy(rs.get_digit_hash()[res])

    def __init__(self, digits=None):
        self.digits = digits

    def get_digit_set(self, rs):
        if self.digits is not None:
            return self.digits
        else:
            raise DigitsException("You must implement the getDigitSet method for a digit generator.")


class SymmetricDigits(Digits):
    def __init__(self, j=1):
        super(Digits, self).__init__()
        self.j = j

    def get_digit_set(self, rs):
        return [[a - floor(rs.abs_determinant / 2) if b == self.j - 1 else 0 for b in range(rs.dimension)] for a in
                range(rs.abs_determinant)]


class CanonicalDigits(Digits):
    def __init__(self, j=1):
        super(Digits, self).__init__()
        self.j = j

    def get_digit_set(self, rs):
        return [[a if b == self.j - 1 else 0 for b in range(rs.dimension)] for a in range(rs.abs_determinant)]


class ShiftedCanonicalDigits(Digits):
    def __init__(self, j=1, shift=0):
        super(Digits, self).__init__()
        self.j = j
        self.shift = shift

    def get_digit_set(self, rs):
        if self.shift > rs.abs_determinant - 1 or self.shift < 0:
            raise DigitsException("You can't shift bigger than the abs of the determinant - 1!")
        return [[a - self.shift if b == self.j - 1 else 0 for b in range(rs.dimension)] for a in
                range(rs.abs_determinant)]


class AdjointDigits(Digits):
    def get_digit_set(self, rs):
        # first generating a complete residue system to cr_set
        smith_u = rs.get_smith_u()
        smith_diagonal = rs.get_smith_diagonal_list()

        insm_u = smith_u.inverse()
        cr_set = []
        v = [0] * rs.dimension
        j = 0
        finished = 0
        while finished == 0 and j < rs.abs_determinant:
            cr_set.append((insm_u * vector(v)).list())
            i = rs.dimension - 1
            while i >= 0 and v[i] == smith_diagonal[i] - 1:
                v[i] = 0
                i = i - 1
            if i >= 0:
                v[i] = v[i] + 1
                j = j + 1
            else:
                finished = 1
        # second producing the adjoint type complete residue system
        bs = []
        for i in cr_set:
            if i == [0] * rs.dimension:
                bs.append(i)
            else:
                bs.append(self.get_congruent_element(i,rs))
        return bs
    def get_congruent_element(self, v, rs):
        """
        Computes the congruent class of a given vector v using the Adjoint method
        """
        def get_symmetric_modulo(num, mod):
            return Mod(num, mod).lift_centered()

        if not hasattr(rs,'adjoint_m'):
            rs.adjoint_m = rs.get_base().adjugate()

        v1 = []
        for i in range(rs.dimension):
            s = 0
            for j in range(rs.dimension):
                s = (s + rs.adjoint_m[i, j] * v[j])
            s = get_symmetric_modulo(s, rs.determinant)
            v1.append(s)
        return list(rs.get_base() * vector(v1)/rs.determinant)

class DenseDigits(AdjointDigits):
    def get_digit_set(self, rs):
        bset = super(DenseDigits, self).get_digit_set(rs)
        tempset = []

        operator_matrix = rs.get_operator().operator
        while tempset != bset:
            tempset = bset
            bset = []
            for v in tempset:
                nor = (operator_matrix * vector(v)).norm()
                for i in range(rs.dimension):
                    v[i] = v[i] + rs.abs_determinant
                    ok = 1
                    while (operator_matrix * vector(v)).norm(Infinity) < nor:
                        v[i] = v[i] + rs.abs_determinant
                        nor = (operator_matrix * vector(v)).norm(Infinity)
                        ok = 0
                    if ok == 1:
                        v[i] = v[i] - 2 * rs.abs_determinant
                        while (operator_matrix * vector(v)).norm(Infinity) < nor:
                            v[i] = v[i] - rs.abs_determinant
                            nor = (operator_matrix * vector(v)).norm(Infinity)
                            ok = 0
                        v[i] = v[i] + rs.abs_determinant
                    else:
                        v[i] = v[i] - rs.abs_determinant
                bset.append(v)
        return bset
