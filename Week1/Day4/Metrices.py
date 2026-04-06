import numpy as np
A = np.array([[1, 2], [3, 4]])
print(A)

B = np.array([[5, 6], [7, 8]])
print(B)

## Matrix Addition
C = A + B
print(C)

##Matrix Multiplication
D = A @ B ## np.dot(A, B)
print(D)

A_T = A.T
print(A_T)

A_inv = np.linalg.inv(A)
print(A_inv)

