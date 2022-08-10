import numpy as np
from scipy.sparse.linalg import splu
from scipy.sparse import identity
import scipy.sparse as sparse
import matplotlib.pyplot as plt
from scipy.sparse import csc_matrix


y = np.array([118, 121, 121, 122, 125, 130, 137, 130, 122, 117, 115, 115, 114,
        112, 110, 108, 108, 100,  88,  87,  91,  85,  86,  86,  81,  72,
          72,  86, 108, 125, 144, 144, 143, 139, 138, 144, 151, 151, 147,
        143, 136, 132, 130, 130, 130, 129, 129, 130, 132, 126, 119, 122,
        112,  87,  43,  34,  29,  28,  27,  25,  24,  26,  27,  36,  43,
          45,  46,  50,  52,  53,  59,  74,  89,  93,  91,  90,  90,  89,
          91,  88, 100, 115, 123, 131, 130, 118, 106, 100,  99,  90,  77,
          73,  69,  57,  56,  55,  56,  61,  67,  70,  73,  76,  83,  83,
          86,  84,  83,  91, 102, 102, 103, 102, 105, 111, 119, 123, 122,
        120, 122, 127, 132, 135, 140, 141, 127, 108,  88,  82,  77,  71,
          67,  66,  69,  73,  77,  87,  81,  66,  62,  63,  72,  86, 101])
# y = np.array([118, 121, 121, 122, 125, 130, 137])
d=2
lmbd = 30


m = len(y)
E = identity(m)
# D = csc_matrix(np.diff(E, n=d))

def speyediff(N, d, format='csc'):
    """
    (utility function)
    Construct a d-th order sparse difference matrix based on 
    an initial N x N identity matrix
    
    Final matrix (N-d) x N
    """
    
    assert not (d < 0), "d must be non negative"
    shape     = (N-d, N)
    diagonals = np.zeros(2*d + 1)
    diagonals[d] = 1.
    for i in range(d):
        diff = diagonals[:-1] - diagonals[1:]
        diagonals = diff
    offsets = np.arange(d+1)
    spmat = sparse.diags(diagonals, offsets, shape, format=format)
    return spmat

D = speyediff(m, d)
# E = identity(m).toarray()

coefmat = E + lmbd * D.T @ D
z1 = splu(coefmat).solve(y)
plt.plot(y)
plt.plot(z1)