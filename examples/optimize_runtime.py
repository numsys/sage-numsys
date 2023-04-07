from sage.all import *

from distributed.download import download_by_ids, download_by_filters
from gns import *
import sys

from gns import Timer

for rs in download_by_filters('.dimension=2', 2):
    print(rs)
    timer = Timer()
    print(rs.decide_gns())
    timer.measure_time('decide1')
    print(rs.get_cover_box_volume())
    optimized_rs= rs.optimize()

    timer.start_timer()
    print(rs.decide_gns())
    timer.measure_time('decide2')
    print(optimized_rs.get_cover_box_volume())


    print(timer.get_data())