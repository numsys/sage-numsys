from math import ceil
from math import floor
from sage.all import *


def count_non_zeros(M):
    count = 0
    for y in range(M.nrows()):
        for x in range(M.ncols()):
            if M[y,x] != 0:
                count = count + 1
    return count
    
def count_smith_weight(m):
    sm,smU,smV = m.smith_form()
    weight = 0
    for i in range(sm.nrows()):
        if sm[i,i] != 1:
            for j in range(sm.nrows()):
                if smU[i,j] != 0:
                    weight = weight + 1 
    return weight
    
def calculate_volume(actual_value, transformation_matrix=None, epsilon=0.01):
    dimension = actual_value[0].nrows()
    x = matrix.identity(dimension)
    v1 = [0] * dimension
    v2 = [0] * dimension
    v3 = [0] * dimension
    v4 = [0] * dimension

    while x.norm(Infinity) >= epsilon:
        x = x * actual_value[0]
        l = [x * vector(i) for i in actual_value[1]]

        for i in range(dimension):
            y = 0
            z = 0
            for j in l:
                y = min(j[i], y)
                z = max(j[i], z)
            v1[i] = y
            v3[i] = z
        v2 = [v1[i] + v2[i] for i in range(len(v1))]
        v4 = [v3[i] + v4[i] for i in range(len(v3))]
    tempMultiplier = 1 / (1 - x.norm(Infinity))
    v3 = [-floor(x * tempMultiplier) for x in v2]
    v1 = [-ceil(x * tempMultiplier) for x in v4]

    coverBox = (v1, v3)
    s = 1
    for i in range(len(coverBox[0])):
        s = s * (abs(coverBox[0][i] - coverBox[1][i]) + 1)
    return s

    
def complex_target_function(act_value, transformation_matrix, epsilon=0.01):
    m = act_value[0].inverse()
    vol = calculate_volume(act_value, transformation_matrix)
    smith_w = count_smith_weight(m)
    inv_non_zeros = count_non_zeros(act_value[0])
    return vol * (inv_non_zeros + smith_w)
    
    
    
def phi_optimize_target_function(actVal, transformation_matrix, additionalTransform=None):
    m = actVal[0].inverse()
    smithW = count_smith_weight(m)
    invNonZeros = count_non_zeros(actVal[0])
    if additionalTransform == None:
        transformNonZeros = count_non_zeros(transformation_matrix)
    else: 
        transformNonZeros = count_non_zeros(transformation_matrix * additionalTransform)
        
    return invNonZeros + smithW + transformNonZeros


def create_companion_matrix_from_polynom(p):
    n = p.degree()
    m = Matrix(ZZ,n)
    coefs = p.coefficients(sparse=False)
    for a in range(n):
        if a < n-1:
            m[a+1,a] = 1
        m[a,n-1] = -coefs[a];
    return m

def coef_string_to_polynom(coefString):
    R = ZZ['x']
    return R(coefString.split(" "))
