import numpy as np
from scipy.sparse.linalg import splu
from scipy.sparse import identity
import scipy.sparse as sparse
import matplotlib.pyplot as plt

import timeit
start = timeit.default_timer()

y = np.random.rand(30)
d=2
lmbd = 10


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

def whihen(y, d, lmbd):
    m = len(y)
    E = identity(m)
    D = speyediff(m, d)
    coefmat = E + lmbd * D.T @ D
    z = splu(coefmat).solve(y)
    return z

result = whihen(y, d, lmbd)
plt.plot(y)
plt.plot(result)

stop = timeit.default_timer()
print('Time: ', stop - start)  