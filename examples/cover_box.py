from sage.all import *
from gns import *

rs = SemiRadixSystem([[1, -2], [1, 1]], SymmetricDigits())

cover_box = rs.get_cover_box()
print(cover_box)


rs = SemiRadixSystem([[2, -1], [1, 2]], CanonicalDigits())

cover_box = rs.get_cover_box()
print(cover_box)
