import numpy as np
import scipy.sparse as sparse
from scipy.sparse import identity
# x = np.array([65,  72,  76,  79,  95, 115, 119, 124, 128, 134, 138, 139, 139,
#               139, 140, 141, 138, 135, 125, 118, 122, 114,  89,  52,  45,  40,
#               40,  45,  48,  47,  46,  48,  49,  50,  52,  58,  62,  62,  61,
#               67,  78,  87,  87,  87,  93, 102, 108, 116, 101, 102, 113, 111])

x = np.array([65,  72,  76,  79,  95, 115])

# d=2

def derivative_matrix(x, d=1):
    num_pts = len(x)
    if d == 0:
        return np.identity(num_pts)
    dx = x[d:] - x[:-d]
    V = np.diag(1.0 / dx)
    D_diff = np.diff(derivative_matrix(x, d - 1), axis=0)
    print(d)
    print(V)
    D = d * V @ D_diff
    return D

y = derivative_matrix(x, d=2)
print(y)

def mytest(x, d=1):
    num_pts = len(x)
    if d == 0:
        return np.identity(num_pts)
    dx = x[d:] - x[:-d]
    V = np.diag(1.0 / dx)
    D_diff = np.diff(mytest(x, d - 1), axis=0)
    
    m = len(x)
    shape = (m-d, m)
    diagonals = np.zeros(2*d + 1)
    diagonals[d] = 1.
    for i in range(d):
        diff = diagonals[:-1] - diagonals[1:]
        diagonals = diff
    offsets = np.arange(d+1)    
    D_diff = sparse.diags(diagonals, offsets, shape, format="csc")
    
    print(d)
    print(V)
    D = d * V @ D_diff
    return D

ym = mytest(x, d=2)
print(ym)
