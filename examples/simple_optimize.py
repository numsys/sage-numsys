from sage.all import *
from gns import *
import sys

dr = Drawer()

def rectangle(a,b):
    return line([a,[a[0],b[1]],b,[b[0],a[1]],a])

rs = SemiRadixSystem([[2, -1], [1, 2]], CanonicalDigits())
print(rs.get_cover_box_volume())
cover_box = rs.get_cover_box()
print(cover_box)
g = dr.get_fractions_set_plot(rs) + rectangle(cover_box[0],cover_box[1])
g.save("numsys_optimize_fraction_pre.png", figsize=8)

optimized_rs= rs.optimize()

print(optimized_rs.get_cover_box_volume())
cover_box = optimized_rs.get_cover_box()
g = dr.get_fractions_set_plot(optimized_rs) + rectangle(cover_box[0],cover_box[1])
g.save("numsys_optimize_fraction_post.png", figsize=8)

print(optimized_rs.get_base())
print(optimized_rs.get_digits())
print(optimized_rs.decide_gns())