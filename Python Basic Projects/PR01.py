class Parking_system:
    def __init__(self,Vehicle_number, Type, Entry_time, Exit_time):
        self.Vehicle_number = Vehicle_number
        self.Type = Type
        self.Entry_time = Entry_time
        self.Exit_time = Exit_time


    def lot_rules(self):
        if self.Type == self.car:
            slots = [1,2,3,4,5,6]
            parked_slots_car = []
            for i in slots:
                a= input("Select Your Parking Slot: ")
                if a == i:
                    parked_slots_car = parked_slots_car + i
                    print(f"Your Parking Slot is, {parked_slots_car}")
                else:
                    print("Slots not Availiable")
        elif self.Type == self.bike:
            slots = [1, 2, 3, 4, 5, 6,7,8,9,10]
            parked_slots_bike = []
            for i in slots:
                a = input("Select Your Parking Slot: ")
                if a == i:
                    parked_slots_bike = parked_slots_bike + i
                    print(f"Your Parking Slot is, {parked_slots_bike}")
                else:
                    print("Slots not Availiable")
        elif self.Type == self.truk:
            slots = [1, 2, 3]
            parked_slots_truk = []
            for i in slots:
                a = input("Select Your Parking Slot: ")
                if a == i:
                    parked_slots_truk = parked_slots_truk + i
                    print(f"Your Parking Slot is, {parked_slots_truk}")
                else:
                    print("Slots not Availiable")








