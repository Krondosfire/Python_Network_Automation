# The __init__ method in Python is a special method used to initialize newly created objects of a class. 
# It is often referred to as the "initializer" and is automatically called when an instance of a class is created. 


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

person1 = Person("Javor", 48)
print(person1.name)  # Output: Javor
print(person1.age)   # Output: 49
