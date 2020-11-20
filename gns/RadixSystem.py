import itertools

from gns.RadixSystemDigits import *
from gns.optimization.GeneticSimilarityMatrixOptimizer import *
from gns.RadixSystemOperator import *
from gns.optimization.optimizing_tools import *
import random


class RadixSystemException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class RadixSystemFullResidueSystemException(RadixSystemException):
    def __init__(self, value):
        self.value = value


class RadixSystemExpansivityException(RadixSystemException):
    def __init__(self, value):
        self.value = value


class RadixSystemUnitConditionException(RadixSystemException):
    def __init__(self, value):
        self.value = value


class RadixSystemRegularityException(RadixSystemException):
    def __init__(self, value):
        self.value = value


class RadixSystemOptimizationFailed(RadixSystemException):
    def __init__(self, value):
        self.value = value


class RadixSystemSmartDecideTimeout(RadixSystemException):
    def __init__(self, value):
        self.value = value


def get_symmetric_modulo(num, mod):
    return mod(num, mod).lift_centered()


def to_sparse(m):
    return m


#    if m.is_sparse():
#        return m
#    else:
#        return MatrixSpace(m.base_ring(),m.nrows(),sparse=True)(m)

def to_dense(m):
    return m


#    if m.is_dense():
#        return m
#    else: 
#        return MatrixSpace(m.base_ring(),m.nrows(),sparse=False)(m)


class RadixSystem(object):
    def get_congruent_element(self, v):
        """
        Computes the congruent element for a given point v
        """
        res = 0
        i = self.dimension - 1
        while i >= 0 and self.smith_diagonal[i] > 1:
            s = 0
            for j in range(self.dimension):
                s = s + self.smith_u[i, j] * v[j]
            res = res * self.smith_diagonal[i] + (s % self.smith_diagonal[i])
            i = i - 1
        return self.digitsHash[res]

    def get_adjoint_congruent_class(self, v):
        """
        Computes the congruent class of a given vector v using the Adjoint method
        """
        v1 = []
        for i in range(self.dimension):
            s = 0
            for j in range(self.dimension):
                s = (s + self.adjoint_m[i, j] * v[j])
            s = get_symmetric_modulo(s, self.determinant)
            v1.append(s)
        return v1

    def phi_function(self, v):
        """
        Computes the Phi function for a given point v
        """
        digit = self.get_congruent_element(v)
        return (self.inverse_base * (vector(v) - vector(digit))).list()

    def phi_function_with_digit(self, v):
        """
        Computes the Phi function for a given point v and gives back the congruent element as well
        """
        digit = self.get_congruent_element(v)
        return (self.inverse_base * (vector(v) - vector(digit))).list(), digit

    def get_orbit_from(self, v):
        """
        Computes the orbit from the starting point v
        """
        orbit = []
        step_from = v

        while step_from not in orbit:
            orbit.append(step_from)
            step_from = self.phi_function(step_from)

        orbit.append(step_from)

        return orbit

    def has_finite_expansion(self, v):
        temp = self.get_orbit_from(v)
        return temp[len(temp) - 1] == [0 for i in range(self.dimension)]

    def get_cover_box(self, eps=0.01):
        return self.compute_cover_box(eps)

    def get_covering_box(self, info=True, eps=0.01):
        return self.compute_cover_box(eps)

    def compute_cover_box(self, eps=0.01):
        """
        Computes the covering box of the fraction set
        The output is the coordinates of the lower and the upper corners of the box
        info - output to the screen, which can be True or False
        """
        if hasattr(self, "coverBoxSize"):
            return self.cover_box_size

        x = matrix.identity(self.dimension)
        v1 = [0] * self.dimension
        v2 = [0] * self.dimension
        v3 = [0] * self.dimension
        v4 = [0] * self.dimension

        while x.norm(Infinity) >= eps:
            x = x * self.inverse_base
            multiplied_digits = [x * vector(i) for i in self.digits]

            for i in range(self.dimension):
                y = 0
                z = 0
                for j in multiplied_digits:
                    y = min(j[i], y)
                    z = max(j[i], z)
                v1[i] = y
                v3[i] = z
            v2 = [v1[i] + v2[i] for i in range(len(v1))]
            v4 = [v3[i] + v4[i] for i in range(len(v3))]
        temp_multiplier = 1 / (1 - x.norm(Infinity))
        v3 = [-floor(x * temp_multiplier) for x in v2]
        v1 = [-ceil(x * temp_multiplier) for x in v4]

        self.cover_box_size = (v1, v3)
        return self.cover_box_size

    def get_cover_box_volume(self):
        cover_box = self.get_cover_box()
        s = 1
        for i in range(len(cover_box[0])):
            s = s * (abs(cover_box[0][i] - cover_box[1][i]) + 1)
        return s

    def get_points_in_box_start_val(self):
        low_box, up_box = self.compute_cover_box()
        return {"val": low_box[:], "low_box": low_box, "up_box": up_box, "finished": False}

    def get_points_in_box_step_val(self, val):
        i = 0
        new_val = val["val"][:]
        while i < self.dimension and new_val[i] == val["up_box"][i]:
            new_val[i] = val["low_box"][i]
            i = i + 1
        if i < self.dimension:
            new_val[i] = new_val[i] + 1
        else:
            val["finished"] = True
        return {"val": new_val, "low_box": val["low_box"], "up_box": val["up_box"], "finished": val["finished"]}

    class RadixSystemPointSource(object):
        def __init__(self, data):
            self.data = data
            self.pointer = 0

        def get_points_in_box_start_val(self):
            return {"val": self.data[0], "low_box": self.data[0], "up_box": self.data[len(self.data) - 1],
                    "finished": len(self.data) < 2}

        def get_points_in_box_step_val(self, val):
            self.pointer += 1
            if self.pointer < len(self.data):
                return {"val": self.data[self.pointer], "low_box": val["low_box"], "up_box": val["up_box"],
                        "finished": False}
            else:
                return {"val": self.data[len(self.data) - 1], "low_box": val["low_box"], "up_box": val["up_box"],
                        "finished": True}

    def get_points_in_box(self):
        act = self.get_points_in_box_start_val()
        start_points = []
        while not act["finished"]:
            start_points.append(act["val"])
            act = self.get_points_in_box_step_val(act)
        return start_points

    def get_cycles(self, gns_decide=False, start_points_in=None, point_limit=None, start_point_source=None,
                   point_transform=None):
        if start_points_in is None:
            if start_point_source is None:
                start_point_source_in = self
            else:
                start_point_source_in = start_point_source

            already_visited = []
            act = start_point_source_in.get_points_in_box_start_val()
            counter = 0
            li = []

            while not act["finished"]:
                l_list = []
                if point_transform is None:
                    a = act["val"]
                else:
                    a = list(point_transform * vector(act["val"]))

                while a not in already_visited:
                    if point_limit is not None and counter >= point_limit:
                        return None
                    counter = counter + 1
                    already_visited.append(a)
                    l_list.append(a)
                    a = self.phi_function(a)
                if a in l_list:
                    l_list.append(a)
                    li.append(l_list[l_list.index(a):len(l_list)])
                    if len(li) > 1 and gns_decide:
                        return False
                act = start_point_source_in.get_points_in_box_step_val(act)
            return li
        else:
            start_points = start_points_in
            counter = 0
            li = []
            while len(start_points) > 0:
                l_list = []
                a = start_points[0]
                while a in start_points:
                    if point_limit is not None and counter >= point_limit:
                        return None
                    counter = counter + 1
                    start_points.remove(a)
                    l_list.append(a)
                    a = self.phi_function(a)
                if a in l_list:
                    l_list.append(a)
                    li.append(l_list[l_list.index(a):len(l_list)])
                    if len(li) > 1 and gns_decide:
                        return False

            return li

    def is_gns(self):
        return self.decide_gns()

    def decide_gns(self, start_points=None, point_limit=None, start_point_source=None, point_transform=None,
                   algorithm="covering"):
        if algorithm == "covering":
            if point_transform is not None:
                point_transform = MatrixSpace(ZZ, self.dimension, self.dimension, True, None)(point_transform)

            temp = self.get_cycles(gns_decide=True, start_points_in=start_points, point_limit=point_limit,
                                   start_point_source=start_point_source, point_transform=point_transform)
            if temp == False:
                return False
            elif temp is None:
                return None
            else:
                return True
        else:
            def construct_set_e():
                e = {d for d in [tuple(x) for x in self.digits]}
                e2 = {}
                while e != e2:
                    e2 = {x for x in e}
                    for e in e2:
                        for d in self.digits:
                            e.add(tuple(self.phi_function(vector(e) + vector(d))))
                return e

            e = construct_set_e()
            b = {tuple([s if i == j else 0 for j in range(self.get_dimension())]) for i in range(self.get_dimension())
                 for s in [-1, 1]}
            for p in b.union(e):
                #                print(self.getOrbitFrom(p))
                #                print(self.getOrbitFrom(p)[-1])
                if self.get_orbit_from(p)[-1] != [0] * self.get_dimension():
                    return False
            return True

    def estimate_decide_time(self, estimate_point_number=5000, volume=None):
        covcover_box = self.get_cover_box()
        counter = 0
        t = Timer()
        act_start = [0] * self.get_dimension()
        while counter < estimate_point_number:
            for dim_it in range(self.get_dimension()):
                act_start[dim_it] = random.randint(covcover_box[0][dim_it], covcover_box[1][dim_it])
            self.phi_function(act_start)
            counter = counter + 1

        return t.get_time() * (self.get_cover_box_volume() if volume is None else volume) / counter

    def smart_decide(self, optimal_runtime=60, debug=False):
        actual_volume = self.get_cover_box_volume()
        if debug:
            print("Actual volume is ", actual_volume)
        if actual_volume < 100:
            return self.decide_gns()

        n_length_search_count = 1000
        digit_num = len(self.get_digits())
        find_period_round = floor(log((digit_num - 1) * n_length_search_count / digit_num + 1) / log(digit_num))
        if debug:
            print("Round to find periods", find_period_round)

        for i in range(1, find_period_round):
            res = self.find_n_length_cycle(i)
            # print("nlength",res)
            if len(res) > 0:
                return False

        prob_res = self.probability_gns_test()
        # print("Probability test result:",prob_res)
        if prob_res is not None:
            # print("prob_res",prob_res)
            return False

        estimated_decide_time = self.estimate_decide_time(min(actual_volume * 0.1, 5000))
        if debug:
            print("First runtime estimation", estimated_decide_time)

        optimized_vol, optimize_vol_t = self.optimize(return_transformation_also=True, timeout=optimal_runtime * 0.25)
        optimized_phi, optimize_phi_t = self.optimize(
            target_function=lambda act_val, t: phi_optimize_target_function(act_val, t, optimize_vol_t.inverse()),
            return_transformation_also=True, timeout=optimal_runtime * 0.25)

        transform_matrix = optimize_phi_t * optimize_vol_t.inverse()
        estimated_decide_time = optimized_phi.estimate_decide_time(min(actual_volume * 0.1, 5000),
                                                                 volume=optimized_vol.get_cover_box_volume())
        if debug:
            print("Second runtime estimation", estimated_decide_time)
        if estimated_decide_time < optimal_runtime:
            return optimized_phi.decide_gns(start_point_source=optimized_vol, point_transform=transform_matrix)

        raise RadixSystemSmartDecideTimeout("Too big case")

    def find_n_length_cycle(self, n):
        left_matrix = (matrix.identity(self.get_dimension()) - self.get_base() ** n).inverse()

        digits_as_vector = [vector(d) for d in self.get_digits()]

        digit_vector_combinations = itertools.product(digits_as_vector, repeat=n)
        for combination in digit_vector_combinations:
            s = None
            for i in range(n):
                d = combination[i]
                if s is not None:
                    s = self.get_base() * s + d
                else:
                    s = d
            s = left_matrix * s
            if all([isinstance(si, Integer) for si in s]) and not all([si == 0 for si in s]):
                return self.get_orbit_from(s)
        return []

    def probability_gns_test(self, number_of_tries=100):
        abs_constant_term = len(self.get_digits())
        n_shell = [x for x in
                  itertools.product(range(-abs_constant_term, abs_constant_term + 1), repeat=self.get_dimension())]
        for i in range(number_of_tries):
            random_point = random.choice(n_shell)
            orbit = self.get_orbit_from(random_point)
            if vector(orbit[-1]) != vector([0] * self.get_dimension()):
                return orbit[-1]

        return None

    def stepping_optimize(self):
        act = self
        counter = 0
        while counter < 100 and act.estimate_decide_time() > 60:
            act = act.optimize()
            counter = counter + 1

    def norm(self, v):
        return self.operator.norm(v)

    def optimize(self, cand_num=10, num_of_candidate_to_mutate=10, mutate_num=1,
                 iterate_num=10, target_function=None, recombination=0, return_transformation_also=False, debug=False,
                 timeout=None):

        optimizer = GeneticSimilarityMatrixOptimizer()

        if self.dimension == 1:
            raise RadixSystemOptimizationFailed("Can't optimize 1 sized matrix!")

        if target_function is None:
            target_function = calculate_volume

        # Prepare data for optimizing
        #        crs = matrix([vector(digit) for digit in self.digits],sparse=self.sparseMode).transpose()
        crs = matrix([vector(digit) for digit in self.digits]).transpose()
        start_val = (
            self.base.inverse(), crs, target_function((self.base.inverse(), crs), matrix.identity(self.base.nrows())))

        # Optimizing
        candidate = optimizer.genetic(start_val, cand_num, num_of_candidate_to_mutate, mutate_num, iterate_num,
                                      target_function, recombination, timeout)

        # Construct the new radix system parameters
        # new_m = MatrixSpace(self.base.base_ring(),self.base.nrows(),sparse=self.sparseMode)(candidate[0] * self.base * candidate[0].inverse())
        # new_digits = [(matrix(candidate[0],sparse=self.sparseMode) * vector(d)).list() for d in self.digits]
        new_m = MatrixSpace(self.base.base_ring(), self.base.nrows(), self.base.ncols(), True, None)(
            matrix(candidate[0]) * self.base * matrix(candidate[0]).inverse())
        new_digits = [(matrix(candidate[0]) * vector(d)).list() for d in self.digits]

        if return_transformation_also:
            return (RadixSystem(new_m, new_digits, operator=RadixSystemAlwaysExceptionOperator()),
                    MatrixSpace(self.base.base_ring(), self.base.nrows(), self.base.ncols(), True, None)(candidate[0]))
        else:
            return RadixSystem(new_m, new_digits, operator=RadixSystemAlwaysExceptionOperator())

    def check_expansivity(self):
        for i in [abs(p) for p in self.base.eigenvalues()]:
            if i <= 1:
                return False
        return True

    def check_unit_condition(self):
        cp = self.base.charpoly()
        if abs(cp.subs(x=1)) == 1:
            return False
        return True

    def check_crs_property_and_build_digits_hashes(self):
        if len(self.digits) != self.abs_determinant:
            raise RadixSystemFullResidueSystemException(
                "The digit set must be a full residue system, it should have |det(M)| elements...")
        digits_list = []
        self.digitsHash = []
        for v in self.digits:
            res = 0
            i = self.dimension - 1
            while i >= 0 and self.smith_diagonal[i] > 1:
                s = 0
                for j in range(self.dimension):
                    s = s + (self.smith_u[i, j] * v[j] % self.smith_diagonal[i])
                res = res * self.smith_diagonal[i] + (s % self.smith_diagonal[i])
                i = i - 1
            if res in digits_list:
                raise RadixSystemFullResidueSystemException(
                    "The digit set must be a full residue system, there are congruent elements...")
            else:
                digits_list.append(res)
        for i in range(len(digits_list)):
            self.digitsHash.append(self.digits[digits_list.index(i)])
        return True

    def __init__(self, m, digits=None, operator=RadixSystemAlwaysExceptionOperator(), safe_init=False,
                 sparse_mode=False, info_level=0, created_from=None):

        # if isinstance(m,type("")):
        #    p = coefStringToPolynom(m)
        #    m = createCompanionMatrixFromPolynom(p)
        # elif isinstance(m,list):
        #    m = matrix(m)
        # elif isinstance(m,Matrix):
        #    pass
        # else:
        #    raise Exception("You can pass m matrix as polynom string, list of list with the values of the matrix, or the Matrix class can be found in PythonMathBase")

        self.sparse_mode = sparse_mode
        self.created_from = created_from

        if type(m) == type([]):
            m = Matrix(ZZ, len(m), m)

        if self.sparse_mode:
            self.base = to_sparse(m)
        else:
            self.base = to_dense(m)

        self.determinant = self.base.det()
        self.abs_determinant = abs(self.determinant)

        if self.abs_determinant == 0:
            raise RadixSystemRegularityException("The operator must be regular")

        if self.check_unit_condition() == False:
            raise RadixSystemUnitConditionException("abs(det(M-I)) must be greater than one")

        if self.check_expansivity() == False:
            raise RadixSystemExpansivityException("The operator must be expansive")

        self.adjoint_m = self.base.adjugate()

        self.dimension = self.base.nrows()
        self.inverse_base = self.base.inverse()

        self.sm, self.smith_u, smV = to_dense(self.base).smith_form()

        if self.sparse_mode:
            self.sm = to_sparse(self.sm)
            self.smith_u = to_sparse(self.smith_u)

        self.smith_diagonal = [self.sm[i, i] for i in range(self.sm.nrows())]
        self.dense_inverse_m = to_dense(self.inverse_base)

        self.low_box = [0] * self.dimension
        self.up_box = [0] * self.dimension

        ##Set Norm Type
        if operator is None:
            self.operator = RadixSystemOperator()
        else:
            self.operator = operator

        self.operator.init_operator(self)

        if digits is None:
            self.digits = RadixSystemCanonicalDigits().get_digit_set(self)
        elif isinstance(digits, list):
            self.digits = digits
        else:
            self.digits = digits.get_digit_set(self)

        self.check_crs_property_and_build_digits_hashes()

    def get_base(self):
        return self.base

    def get_operator_inverse(self):
        return self.inverse_base

    def get_digits(self):
        return self.digits

    def get_smith_diag(self):
        return self.smith_diagonal

    def get_smith_u(self):
        return self.smith_u

    def get_dimension(self):
        return self.dimension

    def debug_info(self):
        print("Base:", self.base)
        print("Digit set:", self.digits)
        print("Dimension:", self.dimension)
        print("Determinant:", self.determinant)
        print("Smith U:", self.smith_u)
        print("Smith diagonal:", self.smith_diagonal)
