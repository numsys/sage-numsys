import socket
import time
import datetime

from sage.all import *

from distributed.base import BASE_URL
from distributed.server_connection import call_server

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
    if data is None:
        data = {}
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


def build_request_data(job_name : str, extra_query_data):
    if extra_query_data is None:
        extra_query_data = {}

    lock_name = f'progress_{job_name}'

    query_data = {
        "propertyName": lock_name,
        "propertyValue": "in progress by " + socket.gethostname(),
        "sort_property": "volume",
        "sort_direction": "asc",
        "." + lock_name: "null",
    }

    query_data.update(extra_query_data)
    return query_data


def start_processor(callback, lock_name, conditions=None, input_run_work=run_work):
    if conditions is None:
        conditions = {}

    base_timeout = 2
    max_timeout = 60
    try_counter = 0
    while True:
        processed = None
        while processed == None or len(processed) > 0:
            print("PROCESSSS", get_actual_date_time_string())
            queryData = build_request_data(lock_name, conditions)
            processed = input_run_work(callback, BASE_URL + "set-property-for-first", queryData)
            for processed_rs in processed:
                call_server(BASE_URL + "remove-property", {}, {"id": processed_rs["id"], "propertyName": lock_name})

            if len(processed):
                try_counter = 0

        try_counter += 1

        actual_wait = min(max_timeout, pow(base_timeout, try_counter))
        print("No job! Waiting " + str(actual_wait) + " sec.", get_actual_date_time_string())
        time.sleep(actual_wait)
