from sage.matrix.matrix_space import MatrixSpace

def to_sparse(m):
    if m.is_sparse():
        return m
    else:
        return MatrixSpace(m.base_ring(),m.nrows(),sparse=True)(m)


def to_dense(m):
    if m.is_dense():
        return m
    else:
        return MatrixSpace(m.base_ring(),m.nrows(),sparse=False)(m)