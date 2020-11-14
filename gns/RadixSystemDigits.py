from sage.all import *

from math import floor


class RadixSystemDigitsException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RadixSystemDigits(object):
    def __init__(self, digits=None):
        self.digits = digits

    def get_digit_set(self, rs):
        if self.digits is not None:
            return self.digits
        else:
            raise RadixSystemDigitsException("You must implement the getDigitSet method for a digit generator.")


class RadixSystemSymmetricDigits(RadixSystemDigits):
    def __init__(self, j=1):
        super(RadixSystemDigits, self).__init__()
        self.j = j

    def get_digit_set(self, rs):
        return [[a - floor(rs.abs_determinant / 2) if b == self.j - 1 else 0 for b in range(rs.dimension)] for a in
                range(rs.abs_determinant)]


class RadixSystemCanonicalDigits(RadixSystemDigits):
    def __init__(self, j=1):
        super(RadixSystemDigits, self).__init__()
        self.j = j

    def get_digit_set(self, rs):
        return [[a if b == self.j - 1 else 0 for b in range(rs.dimension)] for a in range(rs.abs_determinant)]


class RadixSystemShiftedCanonicalDigits(RadixSystemDigits):
    def __init__(self, shift, j=1):
        super(RadixSystemDigits, self).__init__()
        self.j = j
        self.shift = shift

    def get_digit_set(self, rs):
        if self.shift > rs.abs_determinant - 1 or self.shift < 0:
            raise RadixSystemDigitsException("You can't shift bigger than the abs of the determinant - 1!")
        return [[a - self.shift if b == self.j - 1 else 0 for b in range(rs.dimension)] for a in
                range(rs.abs_determinant)]


class RadixSystemAdjointDigits(RadixSystemDigits):
    def get_digit_set(self, rs):
        # first generating a complete residue system to cr_set
        insm_u = rs.smithU.inverse()
        cr_set = []
        v = [0] * rs.dimension
        j = 0
        finished = 0
        while finished == 0 and j < rs.abs_determinant:
            cr_set.append((insm_u * vector(v)).list())
            i = rs.dimension - 1
            while i >= 0 and v[i] == rs.smith_diagonal[i] - 1:
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
                bs.append([x / rs.determinant for x in rs.base * vector(rs.get_adjoint_congruent_class(i))])
        return bs


class RadixSystemDenseDigits(RadixSystemAdjointDigits):
    def get_digit_set(self, rs):
        bset = super(RadixSystemDenseDigits, self).get_digit_set(rs)
        tempset = []

        while tempset != bset:
            tempset = bset
            bset = []
            for v in tempset:
                nor = (rs.oper_s * vector(v)).norm()
                for i in range(rs.dimension):
                    v[i] = v[i] + rs.abs_determinant
                    ok = 1
                    while (rs.oper_s * vector(v)).norm(Infinity) < nor:
                        v[i] = v[i] + rs.abs_determinant
                        nor = (rs.oper_s * vector(v)).norm(Infinity)
                        ok = 0
                    if ok == 1:
                        v[i] = v[i] - 2 * rs.abs_determinant
                        while (rs.oper_s * vector(v)).norm(Infinity) < nor:
                            v[i] = v[i] - rs.abs_determinant
                            nor = (rs.oper_s * vector(v)).norm(Infinity)
                            ok = 0
                        v[i] = v[i] + rs.abs_determinant
                    else:
                        v[i] = v[i] - rs.abs_determinant
                bset.append(v)
        return bset
