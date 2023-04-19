import json

from distributed.base import BASE_URL
from distributed.server_connection import call_server, ServerJsonEncoder


def calculate_basics(data, rs):
    volume = rs.get_cover_box_volume()
    dim = rs.get_dimension()
    determinant = rs.determinant
    abs_determinant = rs.abs_determinant
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
