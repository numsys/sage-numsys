from sage.all import *
from gns import *
import sys

# Kanonikus jegy generálás
rs = SemiRadixSystem([[0, -7], [1, -7]], CanonicalDigits())
print(rs.get_digits())
# Eredmény: [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0]]

# Szimmetrikus jegy generálás
rs = SemiRadixSystem([[0, -7], [1, -7]], SymmetricDigits(2))
print(rs.get_digits())
# Eredmény: [[0, -3], [0, -2], [0, -1], [0, 0], [0, 1], [0, 2], [0, 3]]

# Eltolt szimmetrikus jegy generálás
rs = SemiRadixSystem([[0, -7], [1, -7]], ShiftedCanonicalDigits(2, 5))
print(rs.get_digits())
# Eredmény: [[0, -5], [0, -4], [0, -3], [0, -2], [0, -1], [0, 0], [0, 1]]

# Szomszédos jegyhalmaz
rs = SemiRadixSystem([[0, -7], [1, -7]], AdjointDigits())
print(rs.get_digits())
# Eredmény: [[0, 0], [-1, -1], [-2, -2], [-3, -3], [3, 3], [2, 2], [1, 1]]

# Sűrű jegyhalmaz
rs = SemiRadixSystem([[0, -7], [1, -7]], DenseDigits(),operator=Operator('jacobi'))
print(rs.get_digits())
# Eredmény: [[0, 0], [-1, -1], [5, -9], [4, -10], [-4, 10], [-5, 9], [1, 1]]