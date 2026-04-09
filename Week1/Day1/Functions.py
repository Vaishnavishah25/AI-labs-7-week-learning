##01/04/26

print("##functions")
def greet(name):
    print("Hello, " + name + "!")
greet("Alice")
greet("Bob")

def add(a, b):
    return a + b
result = add(5, 3)
print("The sum is:", result)

##lamda function - anonymous function defined using the lambda keyword
square = lambda x: x * x    
print(square(5))

add = lambda x, y: x + y
print(add(5,3))

multiply = lambda x, y: x * y
print(multiply(2,5))

##Recursion - a function that calls itself
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
print(factorial(5))

def print_numbers(n):
    if n > 0:
        print_numbers(n - 1)
        print(n)
print_numbers(5)

def sum(n):
    if n == 0:
        return 0
    else:
        return n +sum(n-1)
print(sum(5))

