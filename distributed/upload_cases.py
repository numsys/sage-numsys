import datetime
import socket
import json
import pandas as pd

from distributed.base import BASE_URL
from gns import complex_target_function, dimension_target_function, calculate_volume, Timer, Drawer, NumsysException
from orbit_count import count_orbits
from sage.all import *
from gns.SemiRadixSystem import SemiRadixSystem
from gns.digits import ShiftedCanonicalDigits, CanonicalDigits, SymmetricDigits, Digits
from gns.Operator import AlwaysExceptionOperator, Operator
from server_connection import call_server, ServerJsonEncoder
from optimizing import phi_optimize_target_function, coef_string_to_polynom, create_companion_matrix_from_polynom


def upload_rs(case: str, rs: SemiRadixSystem, group, base_generated_by, digit_generated_by, source="manual"):
    if rs.get_dimension() < 2:
        print(rs.get_base(), "Dropped because of the small dimension.")
        return

    print("----------------")
    print(rs.get_base(), rs.get_digits())

    encoded_base = json.dumps(rs.get_base(), cls=ServerJsonEncoder)
    encoded_digits = json.dumps(rs.get_digits(), cls=ServerJsonEncoder)

    alreadyExistingVersionResponse = call_server(BASE_URL + "search-by-base-and-digit-set", {}, {
        'base': encoded_base,
        'digits': encoded_digits,
    })

    print("Existing Test:", alreadyExistingVersionResponse)

    if alreadyExistingVersionResponse["result"] == "NOT_FOUND":
        response = call_server(BASE_URL + "add",
                               {},
                               {
                                   'base': encoded_base,
                                   'digits': encoded_digits,
                                   'group': group,
                                   'baseGeneratedBy': base_generated_by,
                                   'digitsGeneratedBy': digit_generated_by,
                                   'source': source,
                                   'priority': 100,
                                   'token': 'asdasd',
                               }
                               )
        call_server(BASE_URL + "add-properties",
                    {},
                    {
                        'RSId': response["id"],
                        'properties': json.dumps({
                            'digit_generator': digit_generated_by,
                            'charpoly': case
                        }, cls=ServerJsonEncoder),
                        'token': 'asdasd',
                    }
                    )


rs_counter = 0
ok_counter = 0
df_dict = []
def upload_cases(file_name, verbose = False):
    global rs_counter, ok_counter, df_dict
    lines = [line.rstrip('\n') for line in open(file_name)][:2]

    for case in lines:
        p = coef_string_to_polynom(case)
        m = create_companion_matrix_from_polynom(p)
        degree = p.degree()
        c = abs(p[0])
        if verbose:
            print('--------------')
            print(case)
            print(p)
            print(c)
            print(degree)
            print(m)
            restored_polynom = ' '.join([str(x) for x in m.charpoly().coefficients(sparse=False)])
            print(restored_polynom)
            print(restored_polynom == case)

        for shift in range(c):
            for j in range(degree):
                try:
                    digits = ShiftedCanonicalDigits(j=j+1, shift=shift)
                    rs = SemiRadixSystem(m, digits, Operator(), check_crs_property=True, check_expansivity_property=True)
                    #print(rs.get_digits())
                    #print('----->ok')
                    ok_counter += 1
                    if ok_counter % 100 == 0:
                        print(ok_counter,rs_counter)

                    #df_dict.append({'case':case,'constant':c, 'j':j,'shift':shift})

                    #if len(df_dict) % 5000 == 0:
                    #    pd.DataFrame.from_records(df_dict).to_csv('tested_systems.csv')
                    upload_rs(case, rs, 'basic', 'companion', f'shifted_pos{j+1}_shift{shift}')
                except NumsysException as e:
                    print("'", case, "\tfailed\t", e)

        rs_counter += 1


if __name__ == '__main__':
    upload_cases('../polynoms/c0-5d0-6.txt')
    print(f'{ok_counter} candidate from {rs_counter} base')