##date : 31/03/26

print("hello")
print("world "*5)
a = 3
b = 5
print("a + b =", a + b)
print("a - b =", a - b)
print("a * b =", a * b)
print("a / b =", a / b)
print("a % b =", a % b)
print("a ** b =", a ** b)#power
print("a // b =", a // b)#floor division

print("##list #mutable #changable")
my_list = [1, 2, 3, 4, 5]
print(my_list)
my_list.append(6)#at last element
print(my_list)
my_list.insert(4,10)#at index 4 and element 10
print(my_list)
my_list.remove(3)#remove element 3
print(my_list)
my_list.pop()#remove last element   
print(my_list)
my_list.pop(2)#remove element at index 2
print(my_list)
print(my_list+[7, 8, 9])#concatenate two lists
print(my_list*2)#repeat list twice
my_list.sort()#sort list in ascending order
print(my_list)
my_list2 = ["Apple", "Banana", "Cherry"]
print(my_list2)
print(len(my_list2))#length of list
print(max(my_list2))#maximum element in list
print(min(my_list2))#minimum element in list
my_list2[2] = "Orange"#change element at index 2
print(my_list2)
print(my_list[0:2])#slice list from index 0 to 1

print("##tuples #immutable #unchangable")   
my_tuple = (1, 2, 3, 4, 5)
print(my_tuple)
my_tuple2 = ("Apple", "Banana", "Cherry")
print(my_tuple2)
print(len(my_tuple2))#length of tuple
print(max(my_tuple2))#maximum element in tuple
print(min(my_tuple2))#minimum element in tuple

print("##Dictionaries #mutable #changable")
my_dict = {"Ram": 25, "Shyam": 30, "Sita": 28}
print(my_dict)
print(my_dict["Ram"])#access value by key
my_dict["Gita"] = 35#add new key-value pair
print(my_dict)
my_dict["Ram"] = 26#change value of existing key
print(my_dict)
print(my_dict.keys())#get all keys
print(my_dict.values())#get all values
print(my_dict.items())#get all key-value pairs
my_dict.pop("Shyam")#remove key-value pair by key
print(my_dict)
my_dict.clear()#remove all key-value pairs
print(my_dict)

print("##typecasting (conversion of data types)")
a = 5
print(type(a))#check type of a
print(type(str(a)))#check type of str(a)
float(a)#convert to float
print(float(a))
print(type(float(a)))#check type of float(a)
print(str(a))#convert to string
b = "10"
print(int(b))#convert to integer

print("##list to tuple")
my_list = [1, 2, 3, 4, 5]
my_tuple = tuple(my_list)
print(my_tuple)
print(type(my_tuple))#check type of my_tuple
print("##tuple to list")
my_tuple = (1, 2, 3, 4, 5)
my_list = list(my_tuple)
print(my_list)
print(type(my_list))#check type of my_list
print("##list to set")
my_list = [1, 2, 3, 4, 5]
my_set = set(my_list)
print(my_set)
print(type(my_set))#check type of my_set
print("##set to list")
my_set = {1, 2, 3, 4, 5}
my_list = list(my_set)
print(my_list)
print(type(my_list))#check type of my_list

