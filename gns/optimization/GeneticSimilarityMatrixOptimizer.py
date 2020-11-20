from sage.all import *

import random
from gns.helper import Timer


class GeneticSimilarityMatrixOptimizer(object):
    def __init__(self, debug=False):
        self.debug = debug
        self.timeout_timer = Timer()

    def mutate(self, start_val, i, j, t, target_function, transform_function):
        import copy
        vol = target_function(start_val, t)
        # Increment
        u = copy.deepcopy(t)
        vol_u = vol
        improvement = True
        while improvement:
            u[i, j] = u[i, j] + 1
            vol2 = target_function(transform_function(start_val, u), u)
            improvement = vol2 < vol_u
            vol_u = min(vol_u, vol2)
        u[i, j] = u[i, j] - 1
        # Decrement
        v = copy.deepcopy(t)
        vol_v = vol
        improvement = True
        while improvement:
            v[i, j] = v[i, j] - 1
            vol2 = target_function(transform_function(start_val, v), v)
            improvement = vol2 < vol_v
            vol_v = min(vol_v, vol2)
        v[i, j] = v[i, j] + 1

        ret = []
        if u[i, j] != t[i, j]:
            ret.append([u, vol_u, [(i, j)]])  # We don't have to mutate again this coord with this matrix
        if v[i, j] != t[i, j]:
            ret.append([v, vol_v, [(i, j)]])

        if self.debug:
            print(ret)
        return ret

    def recombinate(self, start_val, a, b, target_function):
        n = a.nrows()
        c = matrix(n)
        for i in range(n):
            for j in range(n):
                if random.randint(0, 1) == 0:
                    c[i, j] = a[i, j]
                else:
                    c[i, j] = b[i, j]
        return [[c, target_function(start_val, c), []]]

    def default_transform_function(self, start_val, t):
        return t * start_val[0] * t.inverse(), t * start_val[1], start_val[2]

    def genetic(self, start_val, number_of_candidates, number_of_candidates_to_mutate, mutate_num, iterate_num, target_function, recombination=0,
                timeout=None):

        n = start_val[0].nrows()
        candidates = [[matrix.identity(n), target_function(start_val, matrix.identity(n)), []]]
        best = None
        for iteration in range(iterate_num):
            if self.debug:
                print("------------------------------------------------------")
                print("--------iterate" + str(iteration) + "----------------------")
                print("------------------------------------------------------")
                for candidate in candidates:
                    print(candidate)
                    print("-")

            candidate_number_iterate_begin = min(len(candidates), number_of_candidates_to_mutate)
            for l in range(candidate_number_iterate_begin):
                if self.debug:
                    print("------Begin mutate of-----------")
                    print(candidates[l])
                    print("---------")

                for k in range(int(min(n * (n - 1) / 2, mutate_num * (number_of_candidates - candidate_number_iterate_begin + 1)))):
                    if len(candidates[l][2]) >= n * (n - 1) / 2:
                        break  # If we tried every mutate position, we skip it

                    while True:
                        i = random.randint(0, n - 2)
                        j = random.randint(i + 1, n - 1)

                        if (i, j) not in candidates[l][2]:
                            break

                    candidates[l][2].append((i, j))
                    if self.debug:
                        print(i, j, candidates[l][2])

                    new_candidates = self.mutate(start_val, i, j, candidates[l][0], target_function,
                                                 self.default_transform_function)
                    candidates = candidates + new_candidates
                    if timeout is not None and self.timeout_timer.get_time() > timeout:
                        break
                if timeout is not None and self.timeout_timer.get_time() > timeout:
                    break

            for i in range(recombination):
                i = random.randint(0, n - 2)
                j = random.randint(i + 1, n - 1)
                candidates = candidates + self.recombinate(start_val, candidates[i][0], candidates[j][0], target_function)
                if timeout is not None and self.timeout_timer.get_time() > timeout:
                    break

            candidates = sorted(candidates, key=lambda x: x[1])

            # Merge up duplicates (use the sorted list, the similar matrices must be next to each other)
            i = 0
            while i < len(candidates) - 1:
                # compare the volume first before full matrix compare (speed)
                if candidates[i][1] == candidates[i + 1][1] and candidates[i][0] == candidates[i + 1][0]:
                    candidates[i][2] = candidates[i][2] + candidates[i + 1][2]
                    del candidates[i + 1]
                else:
                    i = i + 1

            best = candidates[0]

            if timeout is not None and self.timeout_timer.get_time() > timeout:
                break

            if self.debug:
                print("--------iterate" + str(iteration) + " END----------------------")
                for candidate in candidates:
                    print(candidate)
                    print("-")
            candidates = candidates[0:min(number_of_candidates, len(candidates))]
        return best
