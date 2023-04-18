import json

from sage.all import *
from distributed.base import BASE_URL
from distributed.orbit_count import count_orbits
from distributed.server_connection import ServerJsonEncoder, call_server


def calculate_signature(data, ns):
    stateMatrix, signature, cycles, orbitLengths, sourceDistances = count_orbits(ns)
    if False:
        print("STATE")
        print(stateMatrix)
        print("SIGNATURE")
        print(signature)
        print("CYCLES")
        print(cycles)
        print("orbitLengths")
        print(orbitLengths)
        print("sourceDistances")
        print(sourceDistances)

    props = {
        'signature': json.dumps(signature, cls=ServerJsonEncoder),
        'periodicPointCount': len(signature),
        'gns': 1 if len(signature) == 1 else 0
    }

    for cycleIt in range(len(cycles)):
        #           if cycleIt > 0:
        props["period" + str(cycleIt)] = json.dumps(cycles[cycleIt], cls=ServerJsonEncoder)
        props["period" + str(cycleIt) + "Length"] = len(cycles[cycleIt])
        props["period" + str(cycleIt) + "orbitLengths"] = json.dumps(orbitLengths[cycleIt], cls=ServerJsonEncoder)
        props["period" + str(cycleIt) + "sourceDistances"] = json.dumps(sourceDistances[cycleIt],
                                                                        cls=ServerJsonEncoder)

    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps(props, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )
