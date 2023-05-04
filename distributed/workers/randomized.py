import json

from distributed.base import BASE_URL
from distributed.server_connection import call_server, ServerJsonEncoder
from gns import SemiRadixSystem

'''
def calculate_basics(data, rs: SemiRadixSystem):
    rs.



    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps({
                        'volume': volume,
                        'dimension': dim,
                        'determinant': determinant,
                        'abs_determinant': abs_determinant,
                    }, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )
'''