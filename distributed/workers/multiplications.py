from sage.all import *

from distributed.base import BASE_URL
from distributed.helpers.worker_handling import create_radix_system
from distributed.server_connection import call_server
from gns import SemiRadixSystem, AlwaysExceptionOperator


def generate_multiplications(data, ns):
    radix_systems = call_server(BASE_URL + "list", {".dimension": ns.getDimension()})
    for data2 in radix_systems:
        print("====================")
        if len(data2['base']) < 2:
            continue
        ns2 = create_radix_system(data2)
        multi_base = ns.get_base() * ns2.get_base()
        print(ns.get_base())
        print(ns2.get_base())
        digits1 = ns.get_digits()
        digits2 = ns2.get_digits()
        print("--A")
        print(ns.get_base())
        print("--")
        print(digits1)
        print("--")
        print("--B")
        print(ns2.get_base())
        print("--")
        print(digits2)
        print("--")
        new_digits = [vector(digits1[d1It]) + ns.get_base() * vector(digits2[d2It]) for d1It in range(len(digits1))
                     for d2It in range(len(digits2))]
        print(new_digits)
        print(multi_base)
        try:
            ns3 = SemiRadixSystem(multi_base, new_digits, AlwaysExceptionOperator())
            generatedBy = str(data["id"]) + "," + str(data2["id"])
            # upload_rs(ns3,"multiplication2",generatedBy,generatedBy,generatedBy)
        except Exception as e:
            print(e)
