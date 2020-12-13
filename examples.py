from sage.all import *
from pprint import pprint
from gns import *

from gns.SimultaneousSemiRadixSystem import SimultaneousSemiRadixSystem

rs =SimultaneousSemiRadixSystem([
    RadixSystem([[2, -1], [1, 2]], RadixSystemAdjointDigits()),
    RadixSystem([[3, -1], [1, 3]], RadixSystemAdjointDigits())
])

pprint(rs.digits)
d2 =[[x[0], x[1], x[0], x[1]] for x in [Matrix(ZZ, [[2, -1], [1, 2]]) * vector(d2) + vector(d1)
                           for d2 in [[0, 0], [1, 0], [-1, -1], [0, -1], [1, -1], [1, 2], [-1, 1], [0, 1], [1, 1], [-1, 0]]
                           for d1 in [[0, 0], [1, 0], [0, -1], [0, 1], [-1, 0]]]]
pprint(d2)
import sys
sys.exit(0)


print("==== Getting Started ====")
rs = RadixSystem([[0, -3], [1, 2]], [[0, 0], [1, 0], [2, 0]])
print(rs.is_gns())

print("==== Digit Generators ====")
rs = RadixSystem([[0, -7], [1, -7]], RadixSystemCanonicalDigits())
print(rs.get_digits(), rs.is_gns())

rs = RadixSystem([[0, -7], [1, -7]], RadixSystemSymmetricDigits())
print(rs.get_digits(), rs.is_gns())

print("==== Phi function ====")

rs = RadixSystem([[0, -7], [1, -7]], RadixSystemSymmetricDigits())
print(rs.phi_function([2, 3]))
print(rs.get_orbit_from([6, 3]))

print("==== Cycle search ====")

print("Cycles:")
for cycle in rs.get_cycles():
    print(cycle)

print("==== Optimizing ====")

# Optimize at most 30 seconds
optimizedVol, optimizeVolT = rs.optimize(return_transformation_also=True, timeout=30)

optimizedPhi, optimizePhiT = rs.optimize(
    target_function=lambda act_val, t: phi_optimize_target_function(act_val, t, optimizeVolT.inverse()),
    return_transformation_also=True, debug=False, timeout=None)

print("Original Volume")
print(rs.get_cover_box_volume())
print("Optimized Volume")
print(optimizedVol.get_cover_box_volume())

print("Base")
print(rs.get_base())
print("Opt vol transform")
print(optimizeVolT)
print("New base for vol optimized")
print(optimizedVol.get_base())
print("Opt phi transform")
print(optimizePhiT)
print("New base for phi optimized")
print(optimizedPhi.get_base())

optVolPoints = optimizedVol.get_points_in_box()
for i in range(3):
    print("Get point from vol optimized:")
    point = random.choice(optVolPoints)
    print(point)
    print("Transform to the other system")
    print(optimizeVolT.inverse() * optimizePhiT)
    print("The point", point, optimizeVolT.inverse(), optimizePhiT)
    newPoint = optimizeVolT.inverse() * optimizePhiT * vector(point)
    print(newPoint)
    print("Calculate Phi")
    print(optimizedPhi.phi_function(newPoint))
    print("The orbit Phi")
    print(optimizedPhi.get_orbit_from(newPoint))

print("==== Drawing ====")
rs = RadixSystem([[0, -3], [1, 2]], RadixSystemCanonicalDigits())
dr = RadixSystemDrawer()
g = dr.get_phi_orbit_graph(rs)
g.save("test.svg", figsize=16)
# g.show()

