from sage.all import *

from distributed.helpers.download import download_raw_by_filters
from gns import *

for r in download_raw_by_filters('.done_optimization=1&.dimension=2',100000):
    print(r)
    rs = SemiRadixSystem(r['base'], r['digits'])

    dr = Drawer()

    cover_box = rs.get_cover_box()
    g = dr.get_fractions_set_plot(rs,iter_num=15)
    g.show()
    g.save(f"fractions/numsys_fraction{r['id']}.png", figsize=8)