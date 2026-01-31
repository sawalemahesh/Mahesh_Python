import json

# File name
file_name = "students.json"


# Function to load JSON data from file
def load_students():
    try:
        with open(file_name, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []  # Return empty list if file does not exist


# Function to save students data to JSON file
def save_students(students):
    with open(file_name, "w") as f:
        json.dump(students, f, indent=4)
    print("Data saved successfully!")


# Function to add a new student
def add_student(students):
    student_id = int(input("Enter student ID: "))
    name = input("Enter student name: ")
    grades = list(map(int, input("Enter grades separated by space: ").split()))
    is_active = input("Is student active? (yes/no): ").lower() == "yes"

    students.append({
        "id": student_id,
        "name": name,
        "grades": grades,
        "is_active": is_active
    })
    print("Student added successfully!")


# Function to search student by ID
def search_student(students):
    student_id = int(input("Enter student ID to search: "))
    for student in students:
        if student["id"] == student_id:
            print("Student found:")
            print(json.dumps(student, indent=4))
            return
    print("Student not found.")


# Function to update grades
def update_grades(students):
    student_id = int(input("Enter student ID to update grades: "))
    for student in students:
        if student["id"] == student_id:
            new_grade = int(input("Enter new grade: "))
            student["grades"].append(new_grade)
            print("Grade added successfully!")
            return
    print("Student not found.")


# Function to display average grades
def display_averages(students):
    print("\nAverage Grades:")
    for student in students:
        if student["grades"]:
            avg = sum(student["grades"]) / len(student["grades"])
            print(f"{student['name']} (ID: {student['id']}): {avg:.2f}")
        else:
            print(f"{student['name']} (ID: {student['id']}): No grades")


# Main program loop
def main():
    students = load_students()

    while True:
        print("\n--- Student Management ---")
        print("1. Add Student")
        print("2. Search Student")
        print("3. Update Grades")
        print("4. Display Average Grades")
        print("5. Save & Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student(students)
        elif choice == "2":
            search_student(students)
        elif choice == "3":
            update_grades(students)
        elif choice == "4":
            display_averages(students)
        elif choice == "5":
            save_students(students)
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
