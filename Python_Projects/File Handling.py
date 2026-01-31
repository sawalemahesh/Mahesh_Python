FILE_NAME = "students.txt"

def add_student():
    roll = input("Enter Roll Number: ")
    name = input("Enter Name: ")
    marks = input("Enter Marks: ")

    with open(FILE_NAME, "a") as file:
        file.write(f"{roll},{name},{marks}\n")

    print("Student record added successfully.\n")


def display_students():
    try:
        with open(FILE_NAME, "r") as file:
            print("Student Records:")
            for line in file:
                roll, name, marks = line.strip().split(",")
                print(f"Roll: {roll}, Name: {name}, Marks: {marks}")
            print()
    except FileNotFoundError:
        print("No records found.\n")


def search_student():
    search_roll = input("Enter Roll Number to search: ")
    found = False

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                roll, name, marks = line.strip().split(",")
                if roll == search_roll:
                    print(f"Record Found → Roll: {roll}, Name: {name}, Marks: {marks}\n")
                    found = True
                    break

        if not found:
            print("Student record not found.\n")

    except FileNotFoundError:
        print("File does not exist.\n")


def average_marks():
    total = 0
    count = 0

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                _, _, marks = line.strip().split(",")
                total += int(marks)
                count += 1

        if count > 0:
            print(f"Average Marks: {total / count:.2f}\n")
        else:
            print("No student records available.\n")

    except FileNotFoundError:
        print("File does not exist.\n")


# Menu-driven program
while True:
    print("1. Add Student")
    print("2. Display Students")
    print("3. Search Student")
    print("4. Average Marks")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()
    elif choice == "2":
        display_students()
    elif choice == "3":
        search_student()
    elif choice == "4":
        average_marks()
    elif choice == "5":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Try again.\n")
