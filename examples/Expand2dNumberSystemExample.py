from sage.all import *
from gns import *

# {"base": [[-2,-1],[1,-1]],"digits": [[0,0],[1,0],[2,0]]}

m = Matrix(ZZ, [[-2, -1], [1, -1]])
digits = [[0, 0], [1, 0], [2, 0]]
ns = SemiRadixSystem(m, digits)

drawer = Drawer()
plot = Drawer.get_two_dimension_numbersystem_expansion_plot(drawer, ns, -10, 11)
plot.save("hue_colored_phi.svg", figsize=16)
