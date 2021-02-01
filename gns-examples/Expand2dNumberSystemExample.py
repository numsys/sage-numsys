from sage.all import *
from gns import *
import itertools
import colorsys

# {"base": [[-2,-1],[1,-1]],"digits": [[0,0],[1,0],[2,0]]}

m = Matrix(ZZ, [[-2, -1], [1, -1]])
digits = [[0, 0], [1, 0], [2, 0]]
ns = SemiRadixSystem(m, digits)

z_vectors = itertools.permutations(range(-10, 11), 2)

def get_hls_color(pair):
    if pair[0] != 0 & pair[1] != 0:
        return colorsys.rgb_to_hls(n[0], n[1], .1)
    else:
        return colorsys.rgb_to_hls(n[0] + .1, n[1] + .1, .1)


plot = Graphics()
for n in z_vectors:
    plot += arrow(n, ns.phi_function(n), color=get_hls_color(n))

plot.save("hue_colored_phi.svg", figsize=16)
