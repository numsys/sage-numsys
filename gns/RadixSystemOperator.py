from sage.all import *


class RadixSystemOperatorException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RadixSystemCantCreateOperator(Exception):
    pass


class RadixSystemOperator(object):
    def __init__(self, norm_type=None):
        self.norm_type = norm_type

    def init_operator(self, rs):
        if (self.norm_type == Infinity or self.norm_type is None) and rs.dense_inverse_m.norm(Infinity) < 1:
            self.norm_type = Infinity
        elif (self.norm_type == 1 or self.norm_type is None) and rs.dense_inverse_m.norm(1) < 1:
            self.norm_type = 1
        elif (self.norm_type == 2 or self.norm_type is None) and rs.dense_inverse_m.norm(2) < 1:
            self.norm_type = 2
        elif self.norm_type == "jacobi" or self.norm_type is None:
            self.norm_type = "jacobi"
            self.construct_operator_norm(rs)
        else:
            raise RadixSystemCantCreateOperator("Can't use the passed norm! " + str(self.norm_type))

    def norm(self, v):
        if self.norm_type == "jacobi":
            return (self.operator * v).norm(Infinity)
        elif self.norm_type == "frob":
            return (self.operator * v).norm('frob')
        elif self.norm_type is not None:
            return v.norm(self.norm_type)
        else:
            raise RadixSystemOperatorException("Operator not generated!")

    def construct_operator_norm(self, rs):
        jacobi, self.operator = rs.inverse_base.change_ring(QQbar).jordan_form(transformation=True)

        # Handle non-trivial cases
        n = self.operator.ncols()
        i = 0
        while i < n - 1:
            if jacobi[i, i + 1] != 0:
                # Calc mi
                mi = (1 - abs(jacobi[i, i])) / 2

                # Find multiplicity
                j = i + 1
                while j < n - 1 and jacobi[j, j + 1] != 0:
                    j = j + 1
                m = j - i

                # Fill them
                for k in range(m):
                    jacobi[i + k, i + 1 + k] = mi ^ (m - k - 1)
                    self.operator[i + k] = self.operator[i + k] * mi ^ (m - k - 1)

            i = i + 1


class RadixSystemAlwaysExceptionOperator(RadixSystemOperator):
    def init_operator(self, rs):
        pass

    def norm(self, v):
        raise RadixSystemOperatorException("RadixSystemAlwaysExceptionOperator used!")


def custom_optimizing(m, func, iterate_num=100):
    import random
    n = m.nrows()
    s = matrix.identity(n)

    nv = 1
    while nv <= iterate_num:
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)

        act_val = func(s * m * s.inverse())

        # Step up
        s[i, j] = s[i, j] + 1
        if s.determinant() == 0:
            s[i, j] = s[i, j] - 1
            continue

        new_val = func(s * m * s.inverse())
        if new_val < act_val:
            nv = nv + 1
            continue

        # Step down
        s[i, j] = s[i, j] - 2
        if s.determinant() == 0:
            s[i, j] = s[i, j] + 1
            continue

        new_val = func(s * m * s.inverse())

        if new_val >= act_val:
            s[i, j] = s[i, j] + 1
            nv = nv + 1
    return s


class RadixSystemFrobeniusOperator(RadixSystemOperator):
    def __init__(self, j=1):
        super().__init__()
        self.j = j
        self.norm_type = "frob"

    def init_operator(self, rs):
        if rs.dimension == 1:
            raise RadixSystemCantCreateOperator("Can't use Frobenius based operator in 1 dimension!")

        self.oper_s = custom_optimizing(rs.base, lambda new_m: new_m.norm('frob') ^ 2)

        if (self.oper_s * rs.base * self.oper_s.inverse()).norm('frob') >= 1:
            raise RadixSystemCantCreateOperator("Frobenius based operator creation failed!")
