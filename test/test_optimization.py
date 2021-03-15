import unittest
from sage.all import *
from gns import *


def two_step_optimization(rs):
    optimized_vol, optimized_volume_t = rs.optimize(return_transformation_also=True, timeout=30)

    optimized_phi, optimized_volt_t = rs.optimize(
        target_function=lambda act_val, transformation_matrix: phi_optimize_target_function(act_val,
                                                                                            transformation_matrix,
                                                                                            optimized_volume_t.inverse()),
        return_transformation_also=True, debug=False, timeout=None)

    transform_matrix = optimized_volt_t * optimized_volume_t.inverse()

    return optimized_phi.decide_gns(start_point_source=optimized_vol,
                                    point_transform=transform_matrix)

class OptimizationTestCase(unittest.TestCase):
    def test_simple_optimization_1(self):
        rs = SemiRadixSystem([[0, -7], [1, -7]], SymmetricDigits())
        optimized_vol = rs.optimize()

        self.assertFalse(optimized_vol.decide_gns())

    def test_simple_optimization_2(self):
        rs = SemiRadixSystem([[0, 0, -2], [1, 0, -2], [0, 1, -2]], [[0, 0, 0], [1, 0, 0]])
        optimized_vol = rs.optimize()

        self.assertTrue(optimized_vol.decide_gns())

    def test_two_step_optimization_1(self):
        rs = SemiRadixSystem([[0, -7], [1, -7]], SymmetricDigits())
        self.assertFalse(two_step_optimization(rs))

    def test_two_step_optimization_2(self):
        rs = SemiRadixSystem([[0, 0, -2], [1, 0, -2], [0, 1, -2]], [[0, 0, 0], [1, 0, 0]])

        self.assertTrue(two_step_optimization(rs))


if __name__ == '__main__':
    unittest.TextTestRunner(sys.stderr, True, 1, False, False, None).run(
        unittest.TestLoader().loadTestsFromTestCase(OptimizationTestCase))
