import json
from distributed.server_connection import ServerJsonEncoder
from gns import SemiRadixSystem


def calculate_signature(data, ns):
    state_matrix, signature, cycles, orbit_lengths, source_distances = count_orbits(ns)
    if False:
        print("STATE")
        print(state_matrix)
        print("SIGNATURE")
        print(signature)
        print("CYCLES")
        print(cycles)
        print("orbit_lengths")
        print(orbit_lengths)
        print("source_distances")
        print(source_distances)

    props = {
        'signature': json.dumps(signature, cls=ServerJsonEncoder),
        'periodic_cycle_count': len(signature),
        'gns': 1 if len(signature) == 1 else 0
    }

    for cycleIt in range(len(cycles)):
        props["period" + str(cycleIt)] = json.dumps(cycles[cycleIt], cls=ServerJsonEncoder)
        props["period" + str(cycleIt) + "_length"] = len(cycles[cycleIt])
        props["period" + str(cycleIt) + "_orbit_lengths"] = json.dumps(orbit_lengths[cycleIt], cls=ServerJsonEncoder)
        props["period" + str(cycleIt) + "_source_distances"] = json.dumps(source_distances[cycleIt],
                                                                        cls=ServerJsonEncoder)

    call_server_add_property(data['id'], props)


def selectByListFromList(l, selector):
    innerSelect = l[selector[0]]
    if isinstance(innerSelect, list):
        return selectByListFromList(innerSelect, selector[1:])
    else:
        return innerSelect


def setByListToList(l, selector, setTo):
    innerSelect = l[selector[0]]
    if isinstance(innerSelect, list):
        return setByListToList(innerSelect, selector[1:], setTo)
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


def betweenCoord(a, b, c):
    return smallerEqCoordByCoord(a, b) and smallerEqCoordByCoord(b, c)


def count_orbits(rs: SemiRadixSystem, startPoints=None):
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
    signature = [1]
    orbit_lengths = [{0: 1}]
    source_distances = [{0: 1}]
    setByListToList(state_matrix, minus_coord_by_coord([0] * rs.get_dimension(), lower_bound), (0, 0))

    def inc_with_add(target, newVal):
        if newVal not in target:
            target[newVal] = 0
        target[newVal] += 1

    def inner_step(val):
        if selectByListFromList(state_matrix, minus_coord_by_coord(val, lower_bound))[0] == None:
            # print("TRY",val)
            actualOrbit = []
            periodicPointId = None
            periodFound = False
            actualPoint = val
            orbitEndDistanceFromPeriodicPoint = 0
            while not periodFound:
                # print("orbit act point",actualPoint)
                for periodicCyclesIt in range(len(periodic_cycles)):
                    if actualPoint in periodic_cycles[periodicCyclesIt]:
                        periodicPointId = periodicCyclesIt
                        periodFound = True

                if betweenCoord(cover_box[0], actualPoint, cover_box[1]):
                    stateMatrixValAtActualPoint = selectByListFromList(state_matrix,
                                                                       minus_coord_by_coord(actualPoint, lower_bound))
                    if stateMatrixValAtActualPoint[0] != None:
                        periodicPointId = stateMatrixValAtActualPoint[1]
                        orbitEndDistanceFromPeriodicPoint = stateMatrixValAtActualPoint[0]
                        periodFound = True

                actualOrbit.append(actualPoint)
                actualPoint = rs.phi_function(actualPoint)

                if actualPoint in actualOrbit:
                    actualOrbit = actualOrbit[:actualOrbit.index(actualPoint) + 1]
                    periodFound = True

            # print("orbit",actualOrbit)

            if periodicPointId == None:
                periodic_points.append(actualOrbit[-1])
                periodicPointId = len(periodic_points) - 1

                newCycle = rs.get_orbit_from(actualOrbit[-1])[:-1]
                periodic_cycles.append(newCycle)
                cycleLength = len(newCycle)
                signature.append(cycleLength)
                orbit_lengths.append({0: cycleLength})
                source_distances.append({})
                for cyclePoint in newCycle:
                    inc_with_add(source_distances[periodicPointId], max([abs(x) for x in cyclePoint]))
                    setByListToList(state_matrix, minus_coord_by_coord(cyclePoint, lower_bound), (0, periodicPointId))

            # print("periodicPointId",periodicPointId)
            for actualOrbitIt in range(len(actualOrbit) - 1):
                if betweenCoord(cover_box[0], actualOrbit[actualOrbitIt], cover_box[1]):
                    try:
                        distanceFromPeriodicPoint = (
                                    len(actualOrbit) - 1 - actualOrbitIt + orbitEndDistanceFromPeriodicPoint)
                        # print("distanceFromPeriodicPoint",distanceFromPeriodicPoint)
                        setByListToList(state_matrix, minus_coord_by_coord(actualOrbit[actualOrbitIt], lower_bound),
                                        (distanceFromPeriodicPoint, periodicPointId))
                        signature[periodicPointId] += 1
                        inc_with_add(orbit_lengths[periodicPointId], distanceFromPeriodicPoint)
                        inc_with_add(source_distances[periodicPointId], max([abs(x) for x in actualOrbit[actualOrbitIt]]))

                    except (ValueError, IndexError):
                        print("NEMJOOO")
                        print(actualOrbit[actualOrbitIt])
                        print(cover_box)
                        print(smallerEqCoordByCoord(cover_box[0], actualOrbit[actualOrbitIt]))
                        print(smallerEqCoordByCoord(actualOrbit[actualOrbitIt], cover_box[1]))

            # print("state_matrix",state_matrix)
            # print("orbit_lengths",orbit_lengths)
            # print("source_distances",source_distances)

    if startPoints == None:
        act = rs.get_points_in_box_start_val()
        while not act["finished"]:
            inner_step(act["val"])
            act = rs.get_points_in_box_step_val(act)
    else:
        for act in startPoints:
            inner_step(act)

    def numberKeyDictToArray(d):
        temp = []
        for i in range(max(d) + 1):
            temp.append(d[i] if i in d else 0)
        return temp

    orbitLengthsList = [numberKeyDictToArray(x) for x in orbit_lengths]
    sourceDistancesList = [numberKeyDictToArray(x) for x in source_distances]

    return state_matrix, signature, periodic_cycles, orbitLengthsList, sourceDistancesList
