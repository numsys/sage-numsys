from sage.all import *


def create_companion_matrix_from_polynom(p):
    """
    >>> ZZ['x']([1,2,3])
    3*x^2 + 2*x + 1
    >>> ZZ['x']([3,2,1])
    x^2 + 2*x + 3
    >>> create_companion_matrix_from_polynom(ZZ['x']([1,2,1]))
    [ 0 -1]
    [ 1 -2]
    >>> create_companion_matrix_from_polynom(ZZ['x']([2,1]))
    [-2]
    >>> create_companion_matrix_from_polynom(ZZ['x']([5,3,4,5,1]))
    [ 0  0  0 -5]
    [ 1  0  0 -3]
    [ 0  1  0 -4]
    [ 0  0  1 -5]
    """
    n = p.degree()
    m = Matrix(ZZ, n)
    coefs = p.coefficients(sparse=False)
    for a in range(n):
        if a < n - 1:
            m[a + 1, a] = 1
        m[a, n - 1] = -coefs[a]
    return m


def coefficient_string_to_polynom(coefString):
    """
    >>> coefficient_string_to_polynom('1 2 1')
    x^2 + 2*x + 1
    >>> coefficient_string_to_polynom('5 3 4 5 1')
    x^4 + 5*x^3 + 4*x^2 + 3*x + 5
    """
    return ZZ['x'](coefString.split(" "))
