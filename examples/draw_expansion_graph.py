from sage.all import *
from gns import *

print("==== Drawing ====")
rs = SemiRadixSystem([[-10]], CanonicalDigits())
print(rs.get_digits())
dr = Drawer()
g = dr.get_phi_orbit_graph(rs, points=[[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[-1],[-2],[-3],[-4],[-5],[-6],[-7],[-8],[-9]])
g.save("numsys_expansion_negadecimal.png", figsize=10)
g.show()

