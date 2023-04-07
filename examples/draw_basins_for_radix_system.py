import matplotlib.pyplot as plt

from gns import SemiRadixSystem
import requests
import sys
from sage.all import *

to_draw_ids = [468,474, 1313, 1606]

for rs_id in to_draw_ids:
    resp = requests.get(f'http://numsys.info/radix-system/list?id={rs_id}')
    result = resp.json()

    r = result[0]
    rs = SemiRadixSystem(r['base'],r['digits'])
    print("vol",rs.get_cover_box_volume())
    cycles = rs.get_cycles()

    trivial_cycle_index = 0
    for i, cycle in enumerate(cycles):
        if cycle[0] == [0 for j in range(rs.get_dimension())]:
            trivial_cycle_index = i
            break
    cycles.insert(0, cycles.pop(trivial_cycle_index))

    cycle_main_points = [c[0] for c in cycles]

    def find_cycle(cycle_main_points, orbit):
        for i,val in enumerate(cycle_main_points):
            if val in orbit:
                return i

        return -1

    cycle_basin_list = [[] for i in range(len(cycle_main_points))]
    j = 0
    for start_point in rs.get_points_in_box():
        orbit = rs.get_orbit_from(start_point)
        cycle_index = find_cycle(cycle_main_points,orbit)
        print(start_point, orbit[-4:-1], cycle_index, cycle_main_points[cycle_index])
        cycle_basin_list[cycle_index].append(start_point)
        j += 1

    plots = []
    colors = [(0,1,0),(1,0,0),(0,0,1),(1,1,1),(1,1,0),(0,1,1)]
    print(cycle_basin_list)
    for i, basin_list in enumerate(cycle_basin_list):
        print("draw",i,cycle_main_points[i],colors[i])
        plots.append(point(basin_list, rgbcolor=colors[i], size=40 if rs.get_dimension() == 3 else 100))
    image_filename = f'numsys_basin_distribution_id{rs_id}.png'
    sum(plots).save(image_filename, figsize=16)

    from PIL import Image

    im = Image.open(image_filename)
    im2 = im.crop((400,400,1200,1200))
    im2.save(f'{image_filename}')