# =====================================
# Vehicle Rental System (HGO)
# =====================================

class Vehicle:
    def __init__(self, vehicle_id, brand, price_per_day):
        self.vehicle_id = vehicle_id
        self.brand = brand
        self.price_per_day = price_per_day
        self.__is_available = True

    def is_available(self):
        return self.__is_available

    def rent(self):
        if self.__is_available:
            self.__is_available = False
            return True
        return False

    def return_vehicle(self):
        self.__is_available = True

    def calculate_rent(self, days):
        raise NotImplementedError("Subclasses must implement rent calculation")


# -------------------------------------

class Car(Vehicle):
    def calculate_rent(self, days):
        return self.price_per_day * days


# -------------------------------------

class Bike(Vehicle):
    def calculate_rent(self, days):
        return (self.price_per_day * days) * 0.8  # discounted rate


# -------------------------------------

class RentalService:
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def rent_vehicle(self, vehicle, days):
        if vehicle.is_available():
            vehicle.rent()
            amount = vehicle.calculate_rent(days)
            print(f"{vehicle.brand} rented for {days} days. Rent: ₹{amount}")
        else:
            print("Vehicle is currently not available.")

    def return_vehicle(self, vehicle):
        vehicle.return_vehicle()
        print(f"{vehicle.brand} returned successfully.")

    def show_available_vehicles(self):
        print("\nAvailable Vehicles:")
        for vehicle in self.vehicles:
            if vehicle.is_available():
                print(f"{vehicle.vehicle_id} - {vehicle.brand}")


# -------------------------------------
# Main Execution
# -------------------------------------
if __name__ == "__main__":

    service = RentalService()

    car1 = Car(1, "Honda City", 1500)
    bike1 = Bike(2, "Yamaha", 500)

    service.add_vehicle(car1)
    service.add_vehicle(bike1)

    service.show_available_vehicles()

    service.rent_vehicle(car1, 3)
    service.rent_vehicle(car1, 2)  # already rented

    service.return_vehicle(car1)
    service.rent_vehicle(car1, 2)

    service.show_available_vehicles()
