# =========================================
# Hospital Appointment Management System
# =========================================

class Doctor:
    def __init__(self, doctor_id, name, specialization):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.__schedule = {}  # time_slot : Appointment

    def is_available(self, time_slot):
        return time_slot not in self.__schedule

    def add_appointment(self, time_slot, appointment):
        self.__schedule[time_slot] = appointment

    def remove_appointment(self, time_slot):
        if time_slot in self.__schedule:
            del self.__schedule[time_slot]

    def show_schedule(self):
        print(f"\nDoctor {self.name}'s Schedule:")
        if not self.__schedule:
            print("No appointments scheduled.")
        for slot, appt in self.__schedule.items():
            print(f"{slot} - Patient: {appt.patient.name}")


# -----------------------------------------

class Patient:
    def __init__(self, patient_id, name):
        self.patient_id = patient_id
        self.name = name
        self.__appointments = []

    def add_appointment(self, appointment):
        self.__appointments.append(appointment)

    def remove_appointment(self, appointment):
        self.__appointments.remove(appointment)

    def show_appointments(self):
        print(f"\nAppointments for {self.name}:")
        if not self.__appointments:
            print("No appointments.")
        for appt in self.__appointments:
            print(f"{appt.time_slot} with Dr. {appt.doctor.name}")


# -----------------------------------------

class Appointment:
    def __init__(self, doctor, patient, time_slot):
        self.doctor = doctor
        self.patient = patient
        self.time_slot = time_slot


# -----------------------------------------

class Hospital:
    def __init__(self):
        self.doctors = []
        self.patients = []
        self.__appointments = []

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def add_patient(self, patient):
        self.patients.append(patient)

    def book_appointment(self, doctor, patient, time_slot):
        if doctor.is_available(time_slot):
            appointment = Appointment(doctor, patient, time_slot)
            doctor.add_appointment(time_slot, appointment)
            patient.add_appointment(appointment)
            self.__appointments.append(appointment)
            print(f"Appointment booked for {patient.name} with Dr. {doctor.name} at {time_slot}")
        else:
            print("Selected time slot is not available.")

    def cancel_appointment(self, appointment):
        appointment.doctor.remove_appointment(appointment.time_slot)
        appointment.patient.remove_appointment(appointment)
        self.__appointments.remove(appointment)
        print("Appointment cancelled.")


# -----------------------------------------
# Main Execution
# -----------------------------------------
if __name__ == "__main__":

    hospital = Hospital()

    doc1 = Doctor(1, "Dr. Sharma", "Cardiology")
    doc2 = Doctor(2, "Dr. Rao", "Orthopedics")

    pat1 = Patient(101, "Mahesh")
    pat2 = Patient(102, "Amit")

    hospital.add_doctor(doc1)
    hospital.add_doctor(doc2)

    hospital.add_patient(pat1)
    hospital.add_patient(pat2)

    hospital.book_appointment(doc1, pat1, "10:00 AM")
    hospital.book_appointment(doc1, pat2, "10:00 AM")  # conflict
    hospital.book_appointment(doc1, pat2, "11:00 AM")

    doc1.show_schedule()
    pat1.show_appointments()
    pat2.show_appointments()
