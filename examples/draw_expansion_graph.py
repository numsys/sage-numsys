from sage.all import *
from gns import *

print("==== Drawing ====")
rs = SemiRadixSystem([[0, -7], [1, -7]], SymmetricDigits())
dr = Drawer()
g = dr.get_phi_orbit_graph(rs)
g.save("numsys_expansion.png", figsize=20)
g.show()

