## library for fast numerical computation using arrays
## instead of python lists, we can use numpy arrays which are more efficient for numerical operations
import numpy as np
arr = np.array([1,2,3,4,5])
print(arr)
print(type(arr))#check type of arr
# Methematical operations on numpy arrays
print(arr + 2)#add 2 to each element
print(arr * 3)#multiply each element by 3
print(arr ** 2)#square each element
print(arr / 2)#divide each element by 2
print(np.mean(arr))#calculate mean of arr
print(np.median(arr))#calculate median of arr
print(np.min(arr))#calculate minimum of arr
print(np.max(arr))#calculate maximum of arr

##2D array
a = np.array([[1,2],[3,4]])
print(a)
print(a.shape)#check shape of a
print(a[0,0])#access element at row 0, column 0
