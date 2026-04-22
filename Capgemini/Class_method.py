from datetime import date

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_birth_year(cls, name, year):
        return cls(name, date.today().year - year)

p = Person.from_birth_year("Mahesh", 1999)
print(p.name)
print(p.age)

'''The classmethod() is an inbuilt function in Python, which returns a class method for a given function. 
This means that classmethod() is a built-in Python function that transforms a regular method into a class method. 
When a method is defined using the @classmethod decorator (which internally calls classmethod()), the method is bound to the class and not to an instance of the class. 
As a result, the method receives the class (cls) as its first argument, rather than an instance (self)'''