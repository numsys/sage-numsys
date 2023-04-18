import json

from sage.all import *
from distributed.base import BASE_URL
from distributed.server_connection import call_server, ServerJsonEncoder


def recursive_numerical_approx(obj):
    if type(obj) in [type([]), type((1, 2, 3))]:
        return [recursive_numerical_approx(x) for x in obj]
    else:
        numerical_approx = getattr(obj, "numerical_approx", None)
        if callable(numerical_approx):
            return obj.numerical_approx()
        else:
            return obj


def calculate_eigenvalues(data, rs):
    eigenvals = rs.get_base().eigenvalues()
    print(eigenvals)
    #        print([method_name for method_name in dir(eigenvals[0]) if callable(getattr(eigenvals[0], method_name))])
    eigenvals = [x.numerical_approx() for x in eigenvals]
    eigenvals.sort()
    eigenvectors = rs.get_base().eigenvectors_right()
    eigenvectors = recursive_numerical_approx(eigenvectors)
    eigenvalue_norms = [abs(x) for x in eigenvals]
    eigenvalue_norms.sort()
    print(type(eigenvals[0]))
    print(str(eigenvals[0]), abs(eigenvals[0]))
    print(str(eigenvals[-1]), abs(eigenvals[-1]))
    print("Vectors")
    print(str(eigenvectors))
    call_server(BASE_URL + "add-properties",
                {},
                {
                    'RSId': data["id"],
                    'properties': json.dumps({
                        'eigenvalues': str(eigenvals),
                        'eigenvectors': str(eigenvectors),
                        'eigenvalue_norms': str(eigenvalue_norms),
                        'eigenvalue_min': str(eigenvals[0]),
                        'eigenvalue_max': str(eigenvals[-1]),
                        'eigenvalue_norm_min': str(eigenvalue_norms[0]),
                        'eigenvalue_norm_max': str(eigenvalue_norms[-1]),
                    }, cls=ServerJsonEncoder),
                    'token': 'asdasd',
                }
                )
