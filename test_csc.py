import numpy as np
from scipy.sparse import identity
from scipy.sparse import csc_matrix

x = identity(4)
print(x)
y = csc_matrix(np.diff(x, n=2))
print(y)