import json

from distributed.base import BASE_URL
from distributed.server_connection import call_server, ServerJsonEncoder


def calculate_basics(data, rs):
    volume = rs.get_cover_box_volume()
    dim = rs.get_dimension()
    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps({
                        'volume': volume,
                        'dimension': dim
                    }, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )
