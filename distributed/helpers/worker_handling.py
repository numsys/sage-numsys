import json
import socket
import time
import datetime
import subprocess

from sage.all import *

from distributed.base import BASE_URL
from distributed.server_connection import call_server, ServerJsonEncoder


def get_actual_date_time_string():
    return '{date:%Y-%m-%d %H:%M:%S}'.format(date=datetime.datetime.now())

from gns import CanonicalDigits, SymmetricDigits, Digits, SemiRadixSystem, AlwaysExceptionOperator


def create_radix_system(data):
    digits = []
    if data['digits'] == "canonical":
        digits = CanonicalDigits()
    elif data['digits'] == "symmetric":
        digits = SymmetricDigits()
    else:
        digits = Digits(data['digits'])

    m = Matrix(ZZ, data['base'])
    ns = SemiRadixSystem(m, digits, AlwaysExceptionOperator())
    return ns


def run_work(callback, url=BASE_URL + "list", data: dict=None):
    radix_systems = call_server(url, data)
    progressed = []
    for data in radix_systems:
        if len(data['base']) < 2:
            continue

        ns = create_radix_system(data)
        print("Progress:", data["id"], len(data['base']), get_actual_date_time_string())
        callback(data, ns)
        progressed.append(data)
    return progressed

def get_in_progress_value() -> str:
    ret = socket.gethostname()
    if 'SUBHOST' in os.environ:
        ret += " / " + os.environ['SUBHOST']

    ret += " at " + get_actual_date_time_string()

    return ret



def start_processor(callback, job_name, conditions=None):
    if conditions is None:
        conditions = {}

    base_timeout = 2
    max_timeout = 60
    try_counter = 0
    while True:
        processed = None
        lock_prop_name = f'progress_{job_name}'
        done_prop_name = f'done_{job_name}'
        while processed == None or len(processed) > 0:
            print("PROCESSSS", get_actual_date_time_string())

            query_data = {
                "." + done_prop_name: "null",
                "." + lock_prop_name: "null",
                "propertyName": lock_prop_name,
                "propertyValue": get_in_progress_value(),
            }
            if job_name != 'basic_calculations':
                query_data.update({
                    ".volume": "<>null",
                    "sort_property": "volume",
                    "sort_direction": "asc",
                })

            query_data.update(conditions)
            print(query_data)
            processed = run_work(callback, BASE_URL + "set-property-for-first", query_data)
            # In Theory it is only ONE:)
            for processed_rs in processed:
                call_server(BASE_URL + "add-properties",
                            {},
                            {
                                'RSId': processed_rs["id"],
                                'properties': json.dumps({
                                    done_prop_name: 1,
                                }, cls=ServerJsonEncoder),
                                'token': 'asdasd',
                            }
                            )
                call_server(BASE_URL + "remove-property", {}, {"id": processed_rs["id"], "propertyName": lock_prop_name})

            if len(processed):
                try_counter = 0

        try_counter += 1

        actual_wait = min(max_timeout, pow(base_timeout, try_counter))
        print("No job! Waiting " + str(actual_wait) + " sec.", get_actual_date_time_string())
        time.sleep(actual_wait)
