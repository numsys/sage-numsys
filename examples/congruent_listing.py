from sage.all import *

from distributed.optimizing import coef_string_to_polynom
from gns import *
import sys
import itertools

from gns import create_companion_matrix_from_polynom

poly = '-2 0 0 0 0 1'
p = coef_string_to_polynom(poly)
m = create_companion_matrix_from_polynom(p)
rs = SemiRadixSystem(m, CanonicalDigits())
print(rs.get_digits())

#groups = {key: [] for key in rs.get_digits()}
for c in itertools.product([0,1],repeat=5):
    print(c,rs.digit_object.get_congruent_element(c,rs))
