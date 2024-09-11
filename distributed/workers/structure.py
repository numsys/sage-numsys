import json
import sys

from distributed.server_connection import ServerJsonEncoder, call_server_add_property
from gns import SemiRadixSystem


def investigate_structure(data, ns, verbose=False):
    state_matrix, cycle_lengths, cycles, orbit_lengths, source_distances = count_orbits(ns)
    if verbose:
        print("STATE")
        print(state_matrix)
        print("cycle_lengths")
        print(cycle_lengths)
        print("CYCLES")
        print(cycles)
        print("orbit_lengths")
        print(orbit_lengths)
        print("source_distances")
        print(source_distances)

    is_gns_actual = 1 if len(cycle_lengths) == 1 else 0

    if data['properties']['gns'] != str(is_gns_actual):
        print(data['properties']['gns'])
        print(cycle_lengths)
        print(is_gns_actual)
        raise Exception(f'GNS property mismatch for id {data["id"]}')

    props = {
        'periodic_cycle_lengths': json.dumps(cycle_lengths, cls=ServerJsonEncoder),
        'periodic_cycle_count': len(cycle_lengths),
    }

    for cycle_it in range(len(cycles)):
        print(cycles[cycle_it])
        props["period" + str(cycle_it)] = json.dumps(cycles[cycle_it], cls=ServerJsonEncoder)
        props["period" + str(cycle_it) + "_length"] = len(cycles[cycle_it])
        props["period" + str(cycle_it) + "_orbit_lengths"] = json.dumps(orbit_lengths[cycle_it], cls=ServerJsonEncoder)
        props["period" + str(cycle_it) + "_source_distances"] = json.dumps(source_distances[cycle_it],
                                                                        cls=ServerJsonEncoder)

    print(props)
    call_server_add_property(data['id'], props)


def get_ndim_matrix_element_by_position_list(l, selector):
    inner_select = l[selector[0]]
    if isinstance(inner_select, list):
        return get_ndim_matrix_element_by_position_list(inner_select, selector[1:])
    else:
        return inner_select


def set_ndim_matrix_element_by_position_list(l, selector, setTo):
    innerSelect = l[selector[0]]
    if isinstance(innerSelect, list):
        return set_ndim_matrix_element_by_position_list(innerSelect, selector[1:], setTo)
    else:
        oldValue = l[selector[0]]
        l[selector[0]] = setTo
        return oldValue


def minus_coord_by_coord(a, b):
    return [a[i] - b[i] for i in range(len(a))]


def addCoordByCoord(a, b):
    return [a[i] + b[i] for i in range(len(a))]


def smallerEqCoordByCoord(a, b):
    for i in range(len(a)):
        if a[i] > b[i]:
            return False
    return True


def between_coord(a, b, c):
    return smallerEqCoordByCoord(a, b) and smallerEqCoordByCoord(b, c)


def count_orbits(rs: SemiRadixSystem, start_points=None):
    import copy

    cover_box = rs.get_cover_box()
    lower_bound = [cover_box[0][i] for i in range(len(cover_box[0]))]
    sizes = [cover_box[1][i] - cover_box[0][i] + 1 for i in range(len(cover_box[0]))]
    state_matrix = [(None, None)] * sizes[len(sizes) - 1]
    for i in range(rs.get_dimension() - 2, -1, -1):
        tempMatrix = []
        for j in range(sizes[i]):
            tempMatrix.append(copy.deepcopy(state_matrix))
        state_matrix = tempMatrix

    periodic_points = [[0] * rs.get_dimension()]
    periodic_cycles = [[[0] * rs.get_dimension()]]
    cycle_lengths = [1]
    orbit_lengths = [{0: 1}]
    source_distances = [{0: 1}]
    set_ndim_matrix_element_by_position_list(state_matrix, minus_coord_by_coord([0] * rs.get_dimension(), lower_bound), (0, 0))

    def increment_list_on_position(target_list, position_to_increment):
        if position_to_increment not in target_list:
            target_list[position_to_increment] = 0
        target_list[position_to_increment] += 1

    def inner_step(val):
        if get_ndim_matrix_element_by_position_list(state_matrix, minus_coord_by_coord(val, lower_bound))[0] == None:
            actual_orbit = []
            periodic_point_id = None
            period_found = False
            actual_point = val
            orbit_end_distance_from_periodic_point = 0
            while not period_found:
                # print("orbit act point",actual_point)
                for periodic_cycles_it in range(len(periodic_cycles)):
                    if actual_point in periodic_cycles[periodic_cycles_it]:
                        periodic_point_id = periodic_cycles_it
                        period_found = True

                if between_coord(cover_box[0], actual_point, cover_box[1]):
                    state_matrix_val_at_actual_point = get_ndim_matrix_element_by_position_list(state_matrix,
                                                                                           minus_coord_by_coord(actual_point, lower_bound))
                    if state_matrix_val_at_actual_point[0] != None:
                        periodic_point_id = state_matrix_val_at_actual_point[1]
                        orbit_end_distance_from_periodic_point = state_matrix_val_at_actual_point[0]
                        period_found = True

                actual_orbit.append(actual_point)
                actual_point = rs.phi_function(actual_point)

                if actual_point in actual_orbit:
                    actual_orbit = actual_orbit[:actual_orbit.index(actual_point) + 1]
                    period_found = True

            # print("orbit",actual_orbit)

            if periodic_point_id == None:
                periodic_points.append(actual_orbit[-1])
                periodic_point_id = len(periodic_points) - 1

                new_cycle = rs.get_orbit_from(actual_orbit[-1])[:-1]
                periodic_cycles.append(new_cycle)
                cycleLength = len(new_cycle)
                cycle_lengths.append(cycleLength)
                orbit_lengths.append({0: cycleLength})
                source_distances.append({})
                for cycle_point in new_cycle:
                    increment_list_on_position(source_distances[periodic_point_id], max([abs(x) for x in cycle_point]))
                    set_ndim_matrix_element_by_position_list(state_matrix, minus_coord_by_coord(cycle_point, lower_bound), (0, periodic_point_id))

            # print("periodic_point_id",periodic_point_id)
            for actual_orbit_it in range(len(actual_orbit) - 1):
                if between_coord(cover_box[0], actual_orbit[actual_orbit_it], cover_box[1]):
                    try:
                        distance_from_periodic_point = (
                                    len(actual_orbit) - 1 - actual_orbit_it + orbit_end_distance_from_periodic_point)
                        # print("distance_from_periodic_point",distance_from_periodic_point)
                        set_ndim_matrix_element_by_position_list(state_matrix, minus_coord_by_coord(actual_orbit[actual_orbit_it], lower_bound),
                                                                 (distance_from_periodic_point, periodic_point_id))
                        cycle_lengths[periodic_point_id] += 1
                        increment_list_on_position(orbit_lengths[periodic_point_id], distance_from_periodic_point)
                        increment_list_on_position(source_distances[periodic_point_id], max([abs(x) for x in actual_orbit[actual_orbit_it]]))

                    except (ValueError, IndexError):
                        print("NEMJOOO")
                        print(actual_orbit[actual_orbit_it])
                        print(cover_box)
                        print(smallerEqCoordByCoord(cover_box[0], actual_orbit[actual_orbit_it]))
                        print(smallerEqCoordByCoord(actual_orbit[actual_orbit_it], cover_box[1]))

            # print("state_matrix",state_matrix)
            # print("orbit_lengths",orbit_lengths)
            # print("source_distances",source_distances)

    if start_points == None:
        act = rs.get_points_in_box_start_val()
        while not act["finished"]:
            inner_step(act["val"])
            act = rs.get_points_in_box_step_val(act)
    else:
        for act in start_points:
            inner_step(act)

    def number_key_dict_to_array(d):
        temp = []
        for i in range(max(d) + 1):
            temp.append(d[i] if i in d else 0)
        return temp

    orbit_lengths_list = [number_key_dict_to_array(x) for x in orbit_lengths]
    source_distances_list = [number_key_dict_to_array(x) for x in source_distances]

    return state_matrix, cycle_lengths, periodic_cycles, orbit_lengths_list, source_distances_list
