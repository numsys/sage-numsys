from typing import Generator

import requests

from gns import SemiRadixSystem


def download_by_ids(id_list : list[int]):
    for rs_id in id_list:
        resp = requests.get(f'http://numsys.info/radix-system/list?id={rs_id}')
        result = resp.json()

        r = result[0]
        yield SemiRadixSystem(r['base'],r['digits'])


ONE_STEP_SIZE = 200
def download_by_filters(query_param: str, limit : int):
    for r in download_raw_by_filters(query_param,limit):
        yield SemiRadixSystem(r['base'],r['digits'])


def download_raw_by_filters(query_param: str, limit : int) -> Generator[dict, None, None]:
    offset = 0
    while True:
        resp = requests.get(f'http://numsys.info/radix-system/list?{query_param}&size={ONE_STEP_SIZE}&offset={offset}')
        result = resp.json()
        if len(result) == 0:
            break

        for r in result:
            if offset >= limit:
                return
            yield r

        offset += ONE_STEP_SIZE


