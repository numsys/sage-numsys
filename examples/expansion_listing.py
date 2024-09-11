from sage.all import *
from gns import *
import sys
import itertools

rs = SemiRadixSystem([[0, -2], [1, -2]], CanonicalDigits())
print(rs.get_digits())


for c in itertools.product([-1,0,1],repeat=2):
    print(c, rs.get_expansion(c))

print(rs.get_base() ** 2)
print(rs.get_base() ** 3)
print(rs.get_base() ** 4)