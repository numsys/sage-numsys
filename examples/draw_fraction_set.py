from sage.all import *
from gns import *

def rectangle(a,b):
    return line([a,[a[0],b[1]],b,[b[0],a[1]],a])

print("==== Drawing ====")
rs = SemiRadixSystem([[0, -5], [1, -4]], SymmetricDigits())
dr = Drawer()

cover_box = rs.get_cover_box()
g = dr.get_fractions_set_plot(rs,iter_num=7) + rectangle(cover_box[0],cover_box[1])
g.show()
g.save("numsys_fraction2.png", figsize=8)


