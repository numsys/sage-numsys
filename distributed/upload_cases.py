import datetime
import socket
import json

from distributed.base import BASE_URL
from gns import complex_target_function, dimension_target_function, calculate_volume, Timer, Drawer
from orbit_count import count_orbits
from sage.all import *
from gns.SemiRadixSystem import SemiRadixSystem
from gns.digits import ShiftedCanonicalDigits, CanonicalDigits, SymmetricDigits, Digits
from gns.Operator import AlwaysExceptionOperator
from server_connection import call_server, ServerJsonEncoder
from optimizing import phi_optimize_target_function, coef_string_to_polynom, create_companion_matrix_from_polynom


def upload_rs(rs: SemiRadixSystem, group, baseGeneratedBy, digitGeneratedBy, source="manual"):
    if rs.get_dimension() < 2:
        print(rs.get_base(), "Dropped because of the small dimension.")
    else:
        print("----------------")
        print(rs.get_base(), rs.get_digits())

        encodedBase = json.dumps(rs.get_base(), cls=ServerJsonEncoder)
        encodedDigits = json.dumps(rs.get_digits(), cls=ServerJsonEncoder)

        alreadyExistingVersionResponse = call_server(BASE_URL + "search-by-base-and-digit-set", {}, {
            'base': encodedBase,
            'digits': encodedDigits,
        })

        print("Existing Test:", alreadyExistingVersionResponse)

        response = call_server(BASE_URL + "add",
                               {},
                               {
                                   'base': encodedBase,
                                   'digits': encodedDigits,
                                   'group': group,
                                   'baseGeneratedBy': baseGeneratedBy,
                                   'digitsGeneratedBy': digitGeneratedBy,
                                   'source': source,
                                   'priority': 100,
                                   'token': 'asdasd',
                               }
                               )

        if alreadyExistingVersionResponse["result"] == "NOT_FOUND":
            call_server(BASE_URL + "add-properties",
                        {},
                        {
                            'RSId': response["id"],
                            'properties': json.dumps({
                                'block': "waiting for operator test"
                            }, cls=ServerJsonEncoder),
                            'token': 'asdasd',
                        }
                        )


def upload_cases(fname, group, base_generated_by, digits_generated_by, min_size=2, max_size=40, per_dimension_max=None):
    lines = [line.rstrip('\n') for line in open(fname)]

    for testCase in lines:
        dimensionCounter = {x: 0 for x in range(min_size, max_size + 1)}
        # print(testCase)
        p = coef_string_to_polynom(testCase)
        # print(p.degree())
        if p.degree() <= max_size and p.degree() >= min_size and (
                per_dimension_max == None or dimensionCounter[p.degree()] < per_dimension_max):
            dimensionCounter[p.degree()] += 1
            m = create_companion_matrix_from_polynom(p)
            try:
                if not isinstance(digits_generated_by, list):
                    digits_generated_by = [digits_generated_by]

                for digitsGeneratedByOne in digits_generated_by:
                    if digitsGeneratedByOne == 'canonical':
                        digits = CanonicalDigits()
                    elif digitsGeneratedByOne == 'symmetric':
                        digits = SymmetricDigits()
                    elif digitsGeneratedByOne.startswith("canonical"):
                        digits = ShiftedCanonicalDigits(shift=int(digitsGeneratedByOne[10:]))
                    else:
                        raise Exception("Unknown digits generator")

                    rs = SemiRadixSystem(m, digits, AlwaysExceptionOperator())
                    upload_rs(rs, group, base_generated_by, digitsGeneratedByOne)

            except Exception as e:
                print("'", testCase, "\tfailed\t", e)


if sys.argv[1] == "garsia":
    upload_cases("sortedGreppedInput.txt", "garsia", 'garsia', 'canonical', 2, 5)
elif sys.argv[1] == "det3":
    upload_cases("c3deg10SortedGrepped.txt", "det3", 'det3', ['canonical', 'symmetric', 'canonical-2'], 2, 5)
elif sys.argv[1] == "det5":
    #        upload_cases("c5deg8SortedGrepped.txt","det5",'det5',['canonical','canonical-1','canonical-2','canonical-3','canonical-4'],5,5)
    upload_cases("c5deg8SortedGrepped.txt", "det5", 'det5', ['canonical'], 2, 5)
elif sys.argv[1] == "det7":
    #        upload_cases("c7deg6SortedGrepped.txt","det7",'det7',['canonical', 'canonical-1', 'canonical-2', 'canonical-3', 'canonical-4', 'canonical-5', 'canonical-6'],5,5)
    upload_cases("c7deg6SortedGrepped.txt", "det7", 'det7', ['canonical'], 2, 3)