class Calc:
    @staticmethod
    def add(a, b):
        return a + b

res = Calc.add(2, 3)
print(res)

'''A static method in Python is a method defined inside a class that does not depend on any instance or class data. 
It is used when a function logically belongs to a class but does not need access to self or cls. 
Static methods help organize related utility functions inside a class without creating objects.'''