import datetime
import socket
import json

from distributed.base import BASE_URL
from distributed.server_connection import call_server
from gns import complex_target_function, dimension_target_function, calculate_volume, Timer, Drawer, SemiRadixSystem
from sage.all import *

def generate_around_zero(n):
    for nonZeros in Combinations(range(n)):
        for plusOnes in Combinations(nonZeros):
            ret = [0] * n
            for nonZeroPos in nonZeros:
                ret[nonZeroPos] = 1 if nonZeroPos in plusOnes else -1

            if len(nonZeros) > 0:
                yield ret


def draw_rs(data, ns):
    arounder_points = [x for x in generate_around_zero(ns.get_dimension())]

    drawer = Drawer()
    drawer.get_phi_orbit_graph(ns, user_options={
        'vertex_size': 100 * ns.get_dimension(),
        'vertex_colors': {
            '#00ffff': [drawer.point_to_str(x) for x in arounder_points]
        },
        "iterations": 100
    }).save("drawings/" + str(data["id"]) + ".svg", figsize=15)

result = call_server(BASE_URL + "list", {"id": 1229})

for data in result:
    rs = SemiRadixSystem(data['base'],data['digits'])
    draw_rs(data, rs)
