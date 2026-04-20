from abc import ABC, abstractmethod

class Car(ABC):

    @abstractmethod
    def mileage(self):
        pass

class BMW(Car):
    def mileage(self):
        print("BMW mileage is 15 km/l")

class Audi(Car):
    def mileage(self):
        print("Audi mileage is 12 km/l")
obj1 = BMW()
obj2 = Audi()

obj1.mileage()
obj2.mileage()