from sage.all import *
from gns import *
import sys

rs = SemiRadixSystem([[0, -7], [1, -7]], SymmetricDigits())
print(rs.get_cycles())
print(rs.find_n_length_cycle(1))
print(rs.find_n_length_cycle(2))
print(rs.find_n_length_cycle(3))