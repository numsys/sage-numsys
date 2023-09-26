import itertools

from gns.digits import *
from gns.exceptions import *
from gns.helper.matrix_sparse_dense_converting import to_sparse, to_dense
from gns.helper.polynom_base import coefficient_string_to_polynom, create_companion_matrix_from_polynom
from gns.optimization.GeneticSimilarityMatrixOptimizer import *
from gns.Operator import *
from gns.optimization.optimizing_tools import *
import random


class SemiRadixSystem(object):
    def phi_function(self, v, return_digit=False):
        """
        Computes the Phi function for a given point v
        """
        digit = self.digit_object.get_congruent_element(v, self)
        result = (self.inverse_base * (vector(v) - vector(digit))).list()
        if return_digit:
            return result, digit
        else:
            return result

    def get_orbit_from(self, v, return_digits=False):
        """
        Computes the orbit from the starting point v
        """
        orbit = []
        digits = []
        step_from = v

        while step_from not in orbit:
            orbit.append(step_from)
            step_from, digit = self.phi_function(step_from, return_digit=True)
            if return_digits:
                digits.append(digit)

        orbit.append(step_from)

        if return_digits:
            return orbit, digits
        else:
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
        if hasattr(self, "cover_box_size"):
            return self.cover_box_size

        x = matrix.identity(self.dimension)
        local_minimum_vector = [0] * self.dimension
        global_minimum_vector = [0] * self.dimension
        local_maximum_vector = [0] * self.dimension
        global_maxium_vector = [0] * self.dimension

        while x.norm(Infinity) >= eps:
            x = x * self.inverse_base
            multiplied_digits = [x * vector(i) for i in self.get_digits()]

            for i in range(self.dimension):
                local_minimum_per_dimension = 0
                local_maximum_per_dimension = 0
                for j in multiplied_digits:
                    local_minimum_per_dimension = min(j[i], local_minimum_per_dimension)
                    local_maximum_per_dimension = max(j[i], local_maximum_per_dimension)
                local_minimum_vector[i] = local_minimum_per_dimension
                local_maximum_vector[i] = local_maximum_per_dimension
            global_minimum_vector = [local_minimum_vector[i] + global_minimum_vector[i] for i in range(len(local_minimum_vector))]
            global_maxium_vector = [local_maximum_vector[i] + global_maxium_vector[i] for i in range(len(local_maximum_vector))]
        temp_multiplier = 1 / (1 - x.norm(Infinity))
        local_maximum_vector = [-floor(x * temp_multiplier) for x in global_minimum_vector]
        local_minimum_vector = [-ceil(x * temp_multiplier) for x in global_maxium_vector]

        self.cover_box_size = (local_minimum_vector, local_maximum_vector)
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
                e = {d for d in [tuple(x) for x in self.get_digits()]}
                e2 = {}
                while e != e2:
                    e2 = {x for x in e}
                    for e in e2:
                        for d in self.get_digits():
                            e.add(tuple(self.phi_function(vector(e) + vector(d))))
                return e

            e = construct_set_e()
            b = {tuple([s if i == j else 0 for j in range(self.get_dimension())]) for i in range(self.get_dimension())
                 for s in [-1, 1]}
            for p in b.union(e):
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
        if not self.check_expansivity():
            return False
        if not self.check_unit_condition():
            return False
        try:
            self.check_crs_property_and_build_digits_hashes()
        except:
            return False
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

        raise SmartDecideTimeout("Too big case")

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
            if all([ceil(si) == si for si in s]) and not all([si == 0 for si in s]):
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
        return self.get_operator().norm(v)

    def optimize(self, cand_num=10, num_of_candidate_to_mutate=10, mutate_num=100,
                 iterate_num=500, target_function=None, recombination=0, return_transformation_also=False, debug=False,
                 timeout=None):

        optimizer = GeneticSimilarityMatrixOptimizer()

        if self.dimension == 1:
            raise OptimizationFailed("Can't optimize 1 sized matrix!")

        if target_function is None:
            target_function = calculate_volume

        # Prepare data for optimizing
        #        crs = matrix([vector(digit) for digit in self.get_digits()],sparse=self.sparseMode).transpose()
        crs = matrix([vector(digit) for digit in self.get_digits()]).transpose()
        start_val = (
            self.base.inverse(), crs, target_function((self.base.inverse(), crs), matrix.identity(self.base.nrows())))

        # Optimizing
        candidate = optimizer.genetic(start_val, cand_num, num_of_candidate_to_mutate, mutate_num, iterate_num,
                                      target_function, recombination, timeout)

        # Construct the new radix system parameters
        # new_m = MatrixSpace(self.base.base_ring(),self.base.nrows(),sparse=self.sparseMode)(candidate[0] * self.base * candidate[0].inverse())
        # new_digits = [(matrix(candidate[0],sparse=self.sparseMode) * vector(d)).list() for d in self.get_digits()]
        new_m = MatrixSpace(self.base.base_ring(), self.base.nrows(), self.base.ncols(), True, None)(
            matrix(candidate[0]) * self.base * matrix(candidate[0]).inverse())
        new_digits = [(matrix(candidate[0]) * vector(d)).list() for d in self.get_digits()]

        if return_transformation_also:
            return (SemiRadixSystem(new_m, new_digits, operator=AlwaysExceptionOperator()),
                    MatrixSpace(self.base.base_ring(), self.base.nrows(), self.base.ncols(), True, None)(candidate[0]))
        else:
            return SemiRadixSystem(new_m, new_digits, operator=AlwaysExceptionOperator())

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
        if len(self.get_digits()) != self.abs_determinant:
            raise FullResidueSystemException(
                "The digit set must be a full residue system, it should have |det(M)| elements...")
        digits_list = []
        self.digits_by_hash = []
        digits = self.get_digits()

        smith_diagonal = self.get_smith_diagonal_list()
        smith_u = self.get_smith_u()
        for v in digits:
            res = 0
            i = self.dimension - 1
            while i >= 0 and smith_diagonal[i] > 1:
                s = 0
                for j in range(self.dimension):
                    s = s + (smith_u[i, j] * v[j] % smith_diagonal[i])
                res = res * smith_diagonal[i] + (s % smith_diagonal[i])
                i = i - 1
            if res in digits_list:
                raise FullResidueSystemException(
                    "The digit set must be a full residue system, there are congruent elements...")
            else:
                digits_list.append(res)
        for i in range(len(digits_list)):
            self.digits_by_hash.append(digits[digits_list.index(i)])
        return True

    def __init__(self, m, digits=None, operator=None,
                 sparse_mode=False, check_unit_condition=False,
                 check_crs_property=False, check_expansivity_property=False):

        if isinstance(m,type("")):
           p = coefficient_string_to_polynom(m)
           m = create_companion_matrix_from_polynom(p)
        elif isinstance(m,list):
           m = matrix(m)

        self.sparse_mode = sparse_mode

        if isinstance(m,list):
            m = Matrix(ZZ, len(m), m)

        if self.sparse_mode:
            self.base = to_sparse(m)
        else:
            self.base = to_dense(m)

        self.determinant = self.base.det()
        self.abs_determinant = abs(self.determinant)

        if self.abs_determinant == 0:
            raise RegularityException("The operator must be regular")

        self.dimension = self.base.nrows()
        self.inverse_base = self.base.inverse()


        if check_unit_condition and self.check_unit_condition() == False:
            raise UnitConditionException("abs(det(M-I)) must be greater than one")

        if check_expansivity_property and self.check_expansivity() == False:
            raise ExpansivityException("The operator must be expansive")

        if operator is None:
            self.operator = AlwaysExceptionOperator()
        else:
            self.operator = operator

        if digits is None:
            self.digit_object = CanonicalDigits()
        elif isinstance(digits, list):
            self.digit_object = Digits(digits)
        else:
            self.digit_object = digits

        if check_crs_property:
            self.check_crs_property_and_build_digits_hashes()

    def get_base(self):
        return self.base

    def get_inverse_base(self):
        return self.inverse_base

    def get_operator_inverse(self):
        return self.inverse_base

    def get_digits(self):
        if not hasattr(self,'digits'):
            self.digits = self.digit_object.get_digit_set(self)
        return self.digits

    def get_digit_hash(self):
        if not hasattr(self,'digit_hash'):
            self.check_crs_property_and_build_digits_hashes()
        return self.digits_by_hash

    def calculate_smith_form(self):
        self.smith_d, self.smith_u, self.smith_v = to_dense(self.base).smith_form()
        if self.sparse_mode:
            self.smith_d = to_sparse(self.smith_d)
            self.smith_u = to_sparse(self.smith_u)
            self.smith_v = to_sparse(self.smith_v)

        self.smith_diagonal_list = [self.smith_d[i, i] for i in range(self.smith_d.nrows())]

    def get_smith_diagonal_list(self):
        if not hasattr(self, 'smith_diagonal'):
            self.calculate_smith_form()
        return self.smith_diagonal_list

    def get_smith_u(self):
        if not hasattr(self, 'smith_u'):
            self.calculate_smith_form()
        return self.smith_u

    def get_dimension(self):
        return self.dimension

    def get_operator(self):
        if not self.operator.is_initialized():
            self.operator.init_operator(self)
        return self.operator

    def get_expansion(self, c):
        orbit,digits = self.get_orbit_from(c,return_digits=True)
        if orbit[-1] != [0] * self.get_dimension():
            raise Exception(f'{c} does not have expansion.')

        return digits[:-1]