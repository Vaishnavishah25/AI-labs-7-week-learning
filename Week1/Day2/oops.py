###02/01/26
## class - blueprint of an object
## object - instance of a class
##constructor - method which is automatically called when an object is created
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print(f"Name: {self.name}, Age: {self.age}")


## 4 pillars of OOP
## 1. Encapsulation - bundling data and methods that operate on the data within one unit (class)
##(data hiding) - restricting access to certain components of an object
class Bank:
    def __init__(self,balance):
        self.balance = balance 
    
    def get_balance(self):
        return self.balance
    
b = Bank(1000)
print(b.get_balance())#access balance using method 

##Abstraction - hiding complex implementation details and showing only the necessary features of an object
class Car:
    def start(self):
        print("Car started")

c = Car()
c.start()#user only needs to know how to start the car, not how it works

## 3. Inheritance - mechanism where a new class (child class) inherits properties and behaviors from an existing class (parent class)
class Animal:
    def eat(self):
        print("Animal is eating")       
class Dog(Animal):
    def bark(self):
        print("Dog is barking") 

d = Dog()
d.eat()#inherited method from Animal class
d.bark()#method defined in Dog class

## 4. Polymorphism - ability of different classes to be treated as instances of the same class through a common interface
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2
shapes = [Rectangle(4, 5), Circle(3)]