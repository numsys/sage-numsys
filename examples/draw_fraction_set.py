from sage.all import *
from gns import *

print("==== Drawing ====")
rs = SemiRadixSystem([[0, -5], [1, -4]], SymmetricDigits())
dr = Drawer()
g = dr.get_fractions_set_plot(rs,iter_num=7)
g.show()
g.save("numsys_fraction2.png", figsize=8)
