import numpy as np
from scipy.sparse.linalg import splu
from scipy.sparse import identity
import scipy.sparse as sparse
from scipy.sparse import spdiags
import matplotlib.pyplot as plt

from scipy.sparse import random
from scipy import stats
from numpy.random import default_rng
import pandas as pd
from numpy import nan

import timeit
start = timeit.default_timer()

# y = 10*(np.random.rand(100))
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

y1 = np.array([143, 136, 132, 130, 130, 130, 129, 129, 130, 132, 126, 119, 122,
        112,  87,  43,  nan,  nan,  nan,  nan,  nan,  nan,  nan,  nan,  nan,  nan,
          45,  46,  50,  52,  53,  59,  74,  89,  93,  91,  90,  90,  89,
          91,  88, 100, 115, 123, 131, 130, 118, 106, 100,  99,  90,  77])

y2 = np.array([143, 136, 132, 130, 130, 130, 129, 129, 130, 132, 126, 119, 122,
        112,  87,  43,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          45,  46,  50,  52,  53,  59,  74,  89,  93,  91,  90,  90,  89,
          91,  88, 100, 115, 123, 131, 130, 118, 106, 100,  99,  90,  77])

y=y1

d=3
lmbd = 100
def whihen(y, d, lmbd):
    """
    Parameters
    ----------
    y : array_like
        The data to be smoothed
    d : int
        Order of the differences, 
    lmbd : float
        Lambda, the larger lambda is, the smoother the z will be.

    Returns
    -------
    z : array_like
        Smoothed series
        
    References
    ----------
    Eilers, Paul H. C. “A Perfect Smoother.” Analytical Chemistry, vol. 75, 
    no. 14, 30 May 2003, pp. 3631–3636, 10.1021/ac034173t. 
    Accessed 30 May 2022.

    """


    m = len(y)
    E = identity(m)
    """
    Calculate the d-th discrete difference in each row of the matrix.
    This part of the function is the same as numpy.diff() 
    However, numpy.diff() does not accept csc format, and resulting in slower
    execution.
    """

    shape = (m-d, m)
    diagonals = np.zeros(2*d + 1)
    diagonals[d] = 1.
    for i in range(d):
        diff = diagonals[:-1] - diagonals[1:]
        diagonals = diff
    offsets = np.arange(d+1)    
    D = sparse.diags(diagonals, offsets, shape, format="csc")

# """

# """

# rng = default_rng()
# rvs = stats.poisson(0, loc=1).rvs
# S = random(1, m, density=0.7, random_state=rng, data_rvs=rvs)
# S = S.A
# # print(S)
    S = np.where(np.isnan(y), y, 1)
    S = np.where(~np.isnan(S), S, 0)
    print(S)
    W = spdiags(S, 0, m, m).toarray()


    C = W + lmbd * D.T @ D
    
    y = np.where(~np.isnan(y), y, 0)
    z = splu(C).solve(y)
    print(z)
    return z

result = whihen(y, d, lmbd)

plt.plot(y, "*")
plt.plot(result)
plt.ylim(0)
stop = timeit.default_timer()
print('Time: ', stop - start)  