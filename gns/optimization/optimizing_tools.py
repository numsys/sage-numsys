from sage.all import *


def count_non_zeroes(m):
    count = 0
    for y in range(m.nrows()):
        for x in range(m.ncols()):
            if m[y][x] != 0:
                count = count + 1
    return count


def count_smith_weight(m):
    sm, sm_u, sm_v = m.smith_form()
    weight = 0
    for i in range(sm.nrows()):
        if sm[i, i] != 1:
            for j in range(sm.nrows()):
                if sm_u[i, j] != 0:
                    weight = weight + 1
    return weight


def calculate_volume(actual_value, transform=None, epsilon=0.01):
    n = actual_value[0].nrows()
    m_k = matrix.identity(n)
    lower = [0] * n
    upper = [0] * n
    while True:
        m_k = m_k * actual_value[0]
        crs_k = m_k * actual_value[1]
        minimum = [0] * n
        maximum = [0] * n
        for i in range(n):
            minimum[i] = min(crs_k[i])
            maximum[i] = max(crs_k[i])
        lower = [lower[i] + maximum[i] for i in range(n)]
        upper = [upper[i] + minimum[i] for i in range(n)]
        delta = m_k.norm(Infinity)
        if delta < epsilon:
            break
    coef = 1 / (1 - delta)
    vol = 1
    for j in range(n):
        lower[j] = ceil(-lower[j] * coef)
        upper[j] = floor(-upper[j] * coef)
        vol = vol * (upper[j] - lower[j] + 1)
    return vol


def dimension_target_function(actual_value, transform=None, epsilon=0.01):
    print("Start")
    n = actual_value[0].nrows()
    m_k = matrix.identity(n)
    lower = [0] * n
    upper = [0] * n
    while True:
        m_k = m_k * actual_value[0]
        crs_k = m_k * actual_value[1]
        minimum = [0] * n
        maximum = [0] * n
        for i in range(n):
            minimum[i] = min(crs_k[i])
            maximum[i] = max(crs_k[i])
        lower = [lower[i] + maximum[i] for i in range(n)]
        upper = [upper[i] + minimum[i] for i in range(n)]
        delta = m_k.norm(Infinity)
        if delta < epsilon:
            break
    coef = 1 / (1 - delta)
    distances = []

    for j in range(n):
        lower[j] = ceil(-lower[j] * coef)
        upper[j] = floor(-upper[j] * coef)
        distances.append(upper[j] - lower[j] + 1)
    ret = 1
    distance_log_sum = sum([log(x) for x in distances])
    for distance in distances:
        ret *= 1 + log(distance) / distance_log_sum
    print(ret)
    return ret


def complex_target_function(actual_value, transform, epsilon=0.01):
    m = actual_value[0].inverse()
    vol = calculate_volume(actual_value, transform)
    smith_w = count_smith_weight(m)
    inv_non_zeros = count_non_zeroes(actual_value[0])
    return vol * (inv_non_zeros + smith_w)


def phi_optimize_target_function(actual_value, transform, additional_transform=None):
    m = actual_value[0].inverse()
    smith_w = count_smith_weight(m)
    inv_non_zeros = count_non_zeroes(actual_value[0])
    if additional_transform is None:
        transform_non_zeros = count_non_zeroes(transform)
    else:
        transform_non_zeros = count_non_zeroes(transform * additional_transform)

    return inv_non_zeros + smith_w + transform_non_zeros


