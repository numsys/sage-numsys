from sage.all import *
from pprint import pprint
from gns import *

print("==== Getting Started ====")
rs = SemiRadixSystem([[0, -2], [1, 2]], [[0, 0], [1, 0]])


print(rs.get_orbit_from([1,1]))
print(rs.get_orbit_from([-1,-1]))
print(rs.get_orbit_from([-1,0]))