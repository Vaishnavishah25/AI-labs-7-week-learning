import numpy as np
## 2x + y = 5
## x - y = 1

A = np.array([[2, 1], [1, -1]])
B = np.array([5, 1])
solution = np.linalg.solve(A,B)
print(solution)


#### y = Wx + b (y = W @ x + b)
## X - data 
## W - weights
## b - bias

x = np.array([[1,2],[3,4]])
W = np.array([[2],[1]])
b =1
y =x @ W + b
print(y)

## DOT product
x = np.array([1, 2, 3])
w =np.array([4,5,6])
dot_product = np.dot(x, w)
print(dot_product)