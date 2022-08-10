import numpy as np
from scipy.sparse import identity

x = np.array([1, 1, 2, 3, 5, 8, 13, 21])
y = np.diff(x)

# print(x)
# print(y)

# y #data
# lamb # smooth parameter
# d # order of difference
# A = np.array([[1, 0, 1], [0, 2, 0], [1, 0, 3]])
# print(A)
# print(L)
# output
# z
# cve
# h
lamb = 10
d = 1
m = y.size
E = identity(m).toarray()
D = np.diff(E, n=d)
print(D)
print(D.T.shape)
print(D.shape)
# print(D.T*D)
# C = np.linalg.cholesky(E + lamb*D.T*D)
# E = speye(m);
# D = diff(E, d);
# C = chol(E + lambda * D' * D);
# z = C \ (C' \ y);

u = np.zeros((3, 7))

# print(E)
# print(D)
# print(u)
# print(u.size)