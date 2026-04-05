## Function - reusable block of code 
def fun(parameters):
    result = parameters
    return result 
''' functions are used in ML pipelines to perform specific tasks such as data preprocessing, 
feature engineering, model training, and evaluation. They help in organizing code, 
improving readability, and promoting code reusability. By defining functions for different 
steps in the ML pipeline,we can easily modify and maintain the code, as well as collaborate with other developers.
Functions also allow us to break down complex tasks into smaller, manageable pieces, 
making it easier to debug and optimize our ML models.also used for API development,
 where they can be used to define endpoints and handle requests.
'''

'''Types of functions in Python:
1 no return value and no parameters
2 with return value and parameters
3 deault arguments'''

# 1 no return value and no parameters
def greet():
    print("hello")

# 2 with return value and parameters
def square(num):
    return num ** 2 # or return num * num

# 3 default arguments
def greet1(name = "Guest"):
    print(f"Hello, {name}!")

## lambda function
add = lambda a ,b :a + b

#### Practise Questionss::

#1 . check for Prime numbers 
def is_prime(num):
    if num < 2:
        return False

    for i in range(2, num):
        if num % i == 0:
            return False

    return True


# Testing
print(is_prime(5))   # True
print(is_prime(9))   # False

## max of 3 num 
def max(a,b,c):
    if(a>=b and a>=c):
        return a
    elif(b>=a and b>=c):
        return b
    else:
        return c
print(max(2,3,4))
print(max(2,2,4))
print(max(5,5,3))

###Function to count vowels in string
def count_vowels (string):
    count = 0
    string=string.lower()
    for i in str(string):
        if (i == "a" or i == "e" or i == "i" or i == "o" or i == "u"):
            count += 1 
    return count 
    
print (count_vowels("Hello"))


##Validate User input 

