import json
import sys

from distributed.helpers.download import download_raw_by_filters
from gns import SemiRadixSystem, CanonicalDigits, Drawer, SymmetricDigits
from sage.all import *

#original_base = [[0, -2], [1, 2]]
#rs = SemiRadixSystem(original_base, CanonicalDigits())
rs = SemiRadixSystem([[0, -5], [1, -4]], SymmetricDigits())

rs2 = rs.optimize()
print(rs.get_cover_box_volume())
print(rs2.get_cover_box_volume())

print(rs2.get_base().eigenvectors_left())

sys.exit()
'''
LLL_result = rs.get_base().LLL(transformation=True)
LLL_transform = LLL_result[1]
new_digits = [(LLL_transform * vector(d)).list() for d in rs.get_digits()]
rs2 = SemiRadixSystem(LLL_transform * rs.get_base() * LLL_transform.inverse(), new_digits)

print('Original base:')
print(rs.get_base())
print('Original inverse:')
print(rs.get_inverse_base())
print('LLL Transform:')
print(LLL_transform)
print('New Base (LLL_transform * original base):')
print(rs2.get_base())
print('New Digits:')
print(rs2.get_digits())
print('New inverse:')
print(rs2.get_inverse_base())
print(rs2.get_cover_box_volume())
sys.exit()
'''

results = []
c = 0
for r in download_raw_by_filters('.done_optimization=1&.dimension=2',100000):
    print(r)
    rs = SemiRadixSystem(r['base'], r['digits'])

    '''
    LLL_result = rs.get_base().LLL(transformation=True)
    LLL_transform = LLL_result[1]

    new_digits = [(LLL_transform * vector(d)).list() for d in rs.get_digits()]
    rs2 = SemiRadixSystem(LLL_transform * rs.get_base(), new_digits)
    print('calc volumes, original:', r['properties']['optimize:complex:volume'])
    original_volume = rs.get_cover_box_volume()
    print(f'{original_volume=}')
    LLL_volume = rs2.get_cover_box_volume()
    print(f'{LLL_volume=}')
    results.append({
        'originalVolume':original_volume,
        'LLLVolume':LLL_volume,
        'ComplexVolume':r['properties']['optimize:complex:volume'],
    })
    print(results[-1])
    '''

    c += 1
    if c > 10:
        break