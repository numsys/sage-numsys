from sage.all import *
from gns.SemiRadixSystem import SemiRadixSystem
import collections
import colorsys


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def get_hls_color(pair):
    if pair[0] != 0 & pair[1] != 0:
        return colorsys.rgb_to_hls(pair[0], pair[1], .1)
    else:
        return colorsys.rgb_to_hls(pair[0] + .1, pair[1] + .1, .1)


class Drawer:
    def __init__(self):
        pass

    def get_fractions_set_plot(self, rs, iter_num=6, rgbcolor=(0, 0, 0), flag=-1):
        """
        Computes the set of points in the fraction set for plotting
        iterNum - the number of iterations, default is 7
        rgbcolor - the color, default is black
        flag - if it is 1 then the set of points of fractions are computed, if it is -1 then the opposite set, default is -1
        """
        fraction_points = [[0, 0]]
        for i in range(1, iter_num):
            old_k = fraction_points[:]
            for d in rs.get_digits():
                for k in old_k:
                    new_point = ((rs.get_inverse_base() ** i) * vector(d) + vector(k)).list()
                    if new_point not in fraction_points:
                        fraction_points.append(new_point)

        fraction_points = [(flag * vector(p)).list() for p in fraction_points]
        return points(fraction_points, rgbcolor=rgbcolor)

    def get_cover_box_plot(self, rs):
        cover = rs.get_cover_box()
        p = line([cover[0], [cover[0][0], cover[1][1]]])
        p += line([cover[0], [cover[1][0], cover[0][1]]])
        p += line([cover[1], [cover[0][0], cover[1][1]]])
        p += line([cover[1], [cover[1][0], cover[0][1]]])
        return p

    def get_cycles_plot(self, rs, color=(1, 0, 0)):
        p = Graphics()
        for cycle in rs.get_cycles():
            if cycle[0] != rs.getZero():
                for i in range(len(cycle) - 1):
                    p += arrow(cycle[i], cycle[i + 1], color=color)
        return p

    def get_phi_arrows_plot(self, rs: SemiRadixSystem):
        p = Graphics()
        act = rs.get_points_in_box_start_val()
        while not act["finished"]:
            p += arrow(act["val"], rs.phi_function(act["val"]))
            act = rs.get_points_in_box_step_val(act)
        return p

    def point_to_str(self, point):
        return ",".join([str(coordIt) for coordIt in point])

    def get_phi_orbit_graph(self, rs, user_options=None, points=None):
        def add_new_phi_step_with_orbit(rs, act_point, next_point, already_shown_points):
            new_edge = [
                self.point_to_str(act_point),
                self.point_to_str(next_point)
            ]
            if new_edge not in edges:
                edges.append(new_edge)
                already_shown_points.append(act_point)
                already_shown_points.append(next_point)
                act_point = next_point
                next_point = rs.phi_function(act_point)

                add_new_phi_step_with_orbit(rs, act_point, next_point, already_shown_points)

        from sage.graphs.graph_plot import GraphPlot
        edges = []
        already_shown_points = []
        already_finished = []
        if points is None:
            act = rs.get_points_in_box_start_val()
            while not act["finished"]:
                act_point = act["val"]
                next_point = rs.phi_function(act["val"])
                add_new_phi_step_with_orbit(rs, act_point, next_point, already_shown_points)

                act = rs.get_points_in_box_step_val(act)
        else:
            for point in points:
                act_point = point
                next_point = rs.phi_function(point)
                add_new_phi_step_with_orbit(rs, act_point, next_point, already_shown_points)

        g = DiGraph(edges, loops=True)
        options = {
            'vertex_size': 50 * rs.get_dimension(),
            'iterations': 250,
            'vertex_colors': {
                '#00ff00': [self.point_to_str([0] * rs.get_dimension())],
                '#008800': [self.point_to_str(point) for cycle in rs.get_cycles() for point in cycle]
            },
            'vertex_labels': True,
            'edge_colors': {
                'red': [(self.point_to_str(cycle[cycleIt]), self.point_to_str(cycle[(cycleIt + 1) % len(cycle)]))
                        for cycle in rs.get_cycles()
                        for cycleIt in range(len(cycle) - 1)]}
            #            'vertex_color':'green'
        }
        update(options, user_options if user_options is not None else {})
        gp = GraphPlot(g, options)
        return gp.plot()

    def get_two_dimension_numbersystem_expansion_plot(self, ns, lower_bound, upper_bound):
        import itertools

        z_vectors = itertools.permutations(range(lower_bound, upper_bound), 2)
        graphics = Graphics()

        for z in z_vectors:
            graphics += arrow(z, ns.phi_function(z), color=get_hls_color(z))

        return graphics
