from sage.all import *
from gns import *

import unittest

from gns.SimultaneousSemiRadixSystem import SimultaneousSemiRadixSystem


class RadixSystemTest(unittest.TestCase):
    def setUp(self):
        self.debug = True

    def test_necessary_exception(self):
        with self.assertRaises(RadixSystemFullResidueSystemException):
            m = Matrix(ZZ, [[2, -1], [1, 2]])
            digits = [[0, 0], [1, 0], [0, 1], [0, -1]]
            ns1 = RadixSystem(m, digits, operator=RadixSystemAlwaysExceptionOperator())

        with self.assertRaises(RadixSystemExpansivityException):
            m = Matrix(ZZ, [[0, -1], [1, 2]])
            digits = [[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]]
            ns = RadixSystem(m, digits, operator=RadixSystemAlwaysExceptionOperator())

        with self.assertRaises(RadixSystemFullResidueSystemException):
            m = Matrix(ZZ, [[1, -3], [1, 2]])
            digits = [[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]]
            ns = RadixSystem(m, digits, operator=RadixSystemAlwaysExceptionOperator())

        with self.assertRaises(RadixSystemUnitConditionException):
            m = Matrix(ZZ, [[0, 2], [1, 0]])
            digits = [[0, 0], [1, 0]]
            ns = RadixSystem(m, digits, operator=RadixSystemAlwaysExceptionOperator())

    def test_phi_test(self):
        subjects = [
            {
                'm': Matrix(ZZ, [[2, -1], [1, 2]]),
                'digits': RadixSystemDigits([[0, 0], [1, 0], [0, 1], [0, -1], [-6, 5]]),
                'phiTests':
                    [
                        {'from': [-6, 5], 'to': [0, 0]},
                        {'from': [-6, 4], 'to': [-2, 3]},
                        {'from': [-6, 3], 'to': [-2, 2]}
                    ],
                'orbitTests':
                    [
                        {'from': [-6, 3], 'to': [[-6, 3], [-2, 2], [1, -2], [0, -1], [0, 0], [0, 0]]}
                    ],
                'coverBox': ([-2, -6], [2, 1])
            },
            {
                'm': Matrix(ZZ, [[1, -2], [1, 1]]),
                'digits': RadixSystemDigits([[0, 0], [1, 0], [-1, 0]]),
                'phiTests':
                    [
                        {'from': [3, 2], 'to': [2, 0]},
                        {'from': [1, 3], 'to': [2, 1]},
                        {'from': [4, 3], 'to': [3, 0]}
                    ],
                'orbitTests':
                    [
                        {'from': [3, 1], 'to': [[3, 1], [2, -1], [0, -1], [-1, 0], [0, 0], [0, 0]]}
                    ],
                'coverBox': ([-1, -1], [1, 1])
            },
            {
                'm': Matrix(ZZ, [[1, -2], [1, 1]]),
                'digits': RadixSystemSymmetricDigits(),
                'phiTests':
                    [
                        {'from': [3, 2], 'to': [2, 0]},
                        {'from': [1, 3], 'to': [2, 1]},
                        {'from': [4, 3], 'to': [3, 0]}
                    ],
                'orbitTests':
                    [
                        {'from': [3, 1], 'to': [[3, 1], [2, -1], [0, -1], [-1, 0], [0, 0], [0, 0]]}
                    ],
                'coverBox': ([-1, -1], [1, 1])
            },
            {
                'm': Matrix(ZZ, [[-1, -1], [1, -1]]),
                'digits': RadixSystemDigits([[0, 0], [1, 0]]),
                'phiTests':
                    [
                        {'from': [3, 2], 'to': [0, -2]},
                        {'from': [1, 3], 'to': [1, -2]},
                        {'from': [4, 3], 'to': [0, -3]}
                    ],
                'orbitTests':
                    [
                        {'from': [3, 1],
                         'to': [[3, 1], [-1, -2], [0, 2], [1, -1], [-1, 0], [1, 1], [0, -1], [0, 1], [1, 0], [0, 0],
                                [0, 0]]}
                    ],
                'coverBox': ([-1, -1], [1, 1])
            },
            {
                'm': Matrix(ZZ, [[0, -2], [1, -2]]),
                'digits': RadixSystemCanonicalDigits(),
                'orbitTests':
                    [
                        {'from': [2, 1], 'to': [[2, 1], [-1, -1], [1, 1], [1, 0], [0, 0], [0, 0]]}
                    ],
                'coverBox': ([-1, -1], [2, 1]),
                'assertVariable':
                    {
                        'digits': [[0, 0], [1, 0]]
                    }
            },
            {
                'm': Matrix(ZZ, [[3]]),
                'digits': RadixSystemDigits([[-2], [0], [2]]),
                'phiTests':
                    [
                        {'from': [1], 'to': [1]},
                        {'from': [0], 'to': [0]},
                    ],
                'orbitTests':
                    [
                        {'from': [3], 'to': [[3], [1], [1]]},
                        {'from': [7], 'to': [[7], [3], [1], [1]]}
                    ],
                'coverBox': ([-1], [1])
            },
            {
                'name': '4 dimension constans base and digits',
                'm': Matrix(ZZ, [[0, 0, 0, 0, -7], [1, 0, 0, 0, 6], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0]]),
                'digits': RadixSystemCanonicalDigits(),
                'assertVariable':
                    {
                        'digits': [[0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [2, 0, 0, 0, 0], [3, 0, 0, 0, 0], [4, 0, 0, 0, 0],
                                   [5, 0, 0, 0, 0], [6, 0, 0, 0, 0]],
                    },
                'orbitTests':
                    [
                        {'from': [0, 1, 2, 3, 4],
                         'to': [[0, 1, 2, 3, 4], [1, 2, 3, 4, 0], [2, 3, 4, 0, 0], [3, 4, 0, 0, 0], [4, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}
                    ],
            },
            {
                'name': 'Adjoint digits test',
                'm': Matrix(ZZ, [[2, -1], [1, 2]]),
                'digits': RadixSystemAdjointDigits(),
                'isGNS': True,
                'assertVariable':
                    {
                        'digits': [[0, 0], [1, 0], [0, -1], [0, 1], [-1, 0]]
                    },
            },
            {
                'm': Matrix(ZZ, [[3, -1], [1, 3]]),
                'digits': RadixSystemAdjointDigits(),
                'isGNS': True,
                'assertVariable':
                    {
                        'digits': [[0, 0], [1, 0], [-1, -1], [0, -1], [1, -1],
                                   [1, 2], [-1, 1], [0, 1], [1, 1], [-1, 0]]
                    },
            },
            {
                'm': Matrix(ZZ, [[2, -1, 0, 0], [1, 2, 0, 0], [0, 0, 3, -1], [0, 0, 1, 3]]),
                'digits': [[x[0], x[1], x[0], x[1]] for x in [Matrix(ZZ, [[2, -1], [1, 2]]) * vector(d2) + vector(d1)
                           for d2 in [[0, 0], [1, 0], [-1, -1], [0, -1], [1, -1], [1, 2], [-1, 1], [0, 1], [1, 1], [-1, 0]]
                           for d1 in [[0, 0], [1, 0], [0, -1], [0, 1], [-1, 0]]]],
                'isGNS': False,
            },
            {
                'numsys': SimultaneousSemiRadixSystem([
                    RadixSystem([[2, -1], [1, 2]],RadixSystemAdjointDigits()),
                    RadixSystem([[3, -1], [1, 3]], RadixSystemAdjointDigits())
                ]),
                'assertVariable':
                {
                    'digits': [[x[0], x[1], x[0], x[1]] for x in [Matrix(ZZ, [[2, -1], [1, 2]]) * vector(d2) + vector(d1)
                           for d2 in [[0, 0], [1, 0], [-1, -1], [0, -1], [1, -1], [1, 2], [-1, 1], [0, 1], [1, 1], [-1, 0]]
                           for d1 in [[0, 0], [1, 0], [0, -1], [0, 1], [-1, 0]]]],
                },
                'isGNS': False,
            },
            {
                'name' : 'M_A(0,2) ns',
                'm': Matrix(ZZ, [[0, -2, 0, 0], [2, -2, 0, 0], [0, 0, 1, -2], [0, 0, 2, -1]]),
                'digits': RadixSystemDigits([[0, 0, 0, 0], [1, 0, 1, 0], [0, 2, 0, 2], [1, 1, 1, 1],
                                             [-1, 0, -1, 0], [-2, 0, -2, 0], [-1, -1, -1, -1], [-2, -1, -2, -1],
                                             [2, -1, 2, -1],
                                             [-2, 1, -2, 1], [-1, -2, -1, -2], [-3, -3, -3, -3]]),
                'isGNS': True,
            },
            {
                'name': 'M_A(1,2) ns',
                'm': Matrix(ZZ, [[1, -2, 0, 0], [2, -1, 0, 0], [0, 0, 2, -2], [0, 0, 2, 0]]),
                'digits': RadixSystemDigits([[0, 0, 0, 0], [1, 0, 1, 0], [0, 2, 0, 2], [1, 1, 1, 1],
                                             [-1, 0, -1, 0], [1, -1, 1, -1], [0, -1, 0, -1], [-2, 0, -2, 0],
                                             [-1, -1, -1, -1], [2, -1, 2, -1], [-1, -2, -1, -2], [0, -3, 0, -3]]),
                'isGNS': True,
            },
            {
                'name' : 'M_B(-2,-1)',
                'm': Matrix(ZZ, [[-2, 1, 0, 0], [-1, -1, 0, 0], [0, 0, -2, -2], [0, 0, 0, -2]]),
                'digits': RadixSystemDigits([[0, 0, 0, 0], [1, 0, 1, 0], [0, 2, 0, 2], [0, 1, 0, 1],
                                             [-2, 1, -2, 1], [1, -2, 1, -2], [-3, -1, -3, -1], [-2, 0, 0, -2],
                                             [-1, -1, -1, -1], [-2, -1, -2, -1], [-1, -2, -1, -2], [-3, -3, -3, -3]]),
                'isGNS': True,
            },
            {
                'active': False,
                'name': 'M_A(1,1) simultaneous rs',
                'm': Matrix(ZZ, [[1, -1, 0, 0], [1, 1, 0, 0], [0, 0, 2, -1], [0, 0, 1, 2]]),
                'digits': RadixSystemDenseDigits(),
                'operator': RadixSystemOperator('jacobi'),
                'assertVariable':
                    {
                        'digits': [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 1, 1],
                                   [-1, 0, -1, 0], [0, -1, 0, -1], [-1, -1, -1, -1], [-1, 1, -1, 1], [1, -1, 1, -1],
                                   [-1, 2, -1, 2]],
                    },
                'phiTests':
                    [
                        {'from': [-1, -1, 0, 1], 'to': [-1, -1, 0, 1]},
                        {'from': [-1, 1, -1, 0], 'to': [-1, 1, -1, 0]},
                        {'from': [1, 1, 0, 1], 'to': [1, 1, 0, 1]},
                        {'from': [1, -1, 1, 0], 'to': [1, -1, 1, 0]},
                    ],
            },
            {
                'active': False,
                'name': 'M_B(-1,1) simultaneous rs',
                'm': Matrix(ZZ, [[-1, -1, 0, 0], [1, -1, 0, 0], [0, 0, -1, -2], [0, 0, 2, -1]]),
                'digits': RadixSystemDenseDigits(),
                'operator': RadixSystemOperator('jacobi'),
                'assertVariable':
                    {
                        'digits': [[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 1, 1],
                                   [-1, 0, -1, 0], [0, -1, 0, -1], [-1, -1, -1, -1], [-1, 1, -1, 1], [1, -1, 1, -1],
                                   [-2, -1, -2, 1]],
                    },
                'phiTests':
                    [
                        {'from': [-1, -1, 0, -1], 'to': [-1, 1, -1, 0]},
                        {'from': [-1, 1, -1, 0], 'to': [-1, 1, 0, 1]},
                        {'from': [1, 1, 0, 1], 'to': [1, -1, 1, 0]},
                        {'from': [1, -1, 1, 0], 'to': [-1, -1, 0, -1]},
                    ],
                'orbitTests':
                    [
                        {'from': [0, 1, 0, 0],
                         'to': [[0, 1, 0, 0], [0, -2, 0, 1], [-2, 1, -1, 0], [1, 0, 0, 0], [-1, -2, 0, 1],
                                [-1, -2, 0, 1], [0, 1, 0, 0]]},
                        {'from': [0, -1, 0, 0],
                         'to': [[0, -1, 0, 0], [-1, -1, 0, 0], [1, 2, 0, 1], [0, -1, 0, 0]]}
                    ],
            }
        ]
        for it, subject in enumerate(subjects):
            if 'active' in subject and subject['active'] == False:
                continue

            if self.debug:
                print('---------------------')
                print('Testing case ('+str(it)+')')
                if 'name' in subject:
                    print(subject['name'])
                if 'm' in subject:
                    print(subject['m'])
                # print(subject['digits'].digits)

            if 'numsys' not in subject:
                if 'operator' in subject:
                    subject['numsys'] = RadixSystem(subject['m'], subject['digits'], operator=subject['operator'])
                else:
                    subject['numsys'] = RadixSystem(subject['m'], subject['digits'],
                                                    operator=RadixSystemAlwaysExceptionOperator())

            if self.debug:
                print('digits:')
                print(subject['numsys'].get_digits())
                print('Testing phi from digits')

            for d in subject['numsys'].get_digits():
                self.assertEqual(subject['numsys'].phi_function(d), [0 for x in range(subject['numsys'].get_dimension())])

            # operator test....

            if 'phiTests' in subject:
                for test_case in subject['phiTests']:
                    if self.debug:
                        print('Phi test from', test_case['from'])

                    self.assertEqual(subject['numsys'].phi_function(test_case['from']), test_case['to'])

            if 'orbitTests' in subject:
                for test_case in subject['orbitTests']:
                    if self.debug:
                        print('Orbit test from', test_case['from'])

                    self.assertEqual(subject['numsys'].get_orbit_from(test_case['from']), test_case['to'])

            if 'coverBox' in subject:
                if self.debug:
                    print('Cover box test')

                self.assertEqual(subject['numsys'].compute_cover_box(), subject['coverBox'])

            if 'assertVariable' in subject:
                for assertation in subject['assertVariable']:
                    self.assertEqual(getattr(subject['numsys'], assertation), subject['assertVariable'][assertation])

            if 'isGNS' == subject:
                self.assertEqual(subject['numsys'].is_gns(), subject['isGNS'])

    def test_simple_optimization(self):
        rs = RadixSystem([[0, -7], [1, -7]], RadixSystemSymmetricDigits())

        optimized_vol = rs.optimize()
        self.assertFalse(optimized_vol.decide_gns())

        rs = RadixSystem([[0, 0, -2], [1, 0, -2], [0, 1, -2]], [[0, 0, 0], [1, 0, 0]])
        optimized_vol = rs.optimize()
        self.assertTrue(optimized_vol.decide_gns())

    def two_step_optimization(self, rs):
        optimized_vol, optimized_volume_t = rs.optimize(return_transformation_also=True, timeout=30)

        optimized_phi, optimized_volt_t = rs.optimize(
            target_function=lambda act_val, transformation_matrix: phi_optimize_target_function(act_val, transformation_matrix,
                                                                                                optimized_volume_t.inverse()),
            return_transformation_also=True, debug=False, timeout=None)

        transform_matrix = optimized_volt_t * optimized_volume_t.inverse()

        return optimized_phi.decide_gns(start_point_source=optimized_vol,
                                        point_transform=transform_matrix)

    def test_two_step_optimization(self):
        rs = RadixSystem([[0, -7], [1, -7]], RadixSystemSymmetricDigits())
        self.assertFalse(self.two_step_optimization(rs))

        rs = RadixSystem([[0, 0, -2], [1, 0, -2], [0, 1, -2]], [[0, 0, 0], [1, 0, 0]])
        self.assertTrue(self.two_step_optimization(rs))

    def test_smart_decide(self):
        rs = RadixSystem([[0, -7], [1, -7]], RadixSystemSymmetricDigits())
        self.assertFalse(rs.smart_decide())

        rs = RadixSystem([[0, 0, -2], [1, 0, -2], [0, 1, -2]], [[0, 0, 0], [1, 0, 0]])
        self.assertTrue(rs.smart_decide())


unittest.TextTestRunner(sys.stderr, True, 1, False, False, None).run(
    unittest.TestLoader().loadTestsFromTestCase(RadixSystemTest))


