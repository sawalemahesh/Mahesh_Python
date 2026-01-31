FILE_NAME = "tasks.txt"


def load_tasks():
    tasks = []
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                task, status = line.strip().split(" | ")
                tasks.append({"task": task, "status": status})
    except FileNotFoundError:
        pass
    return tasks


def save_tasks(tasks):
    with open(FILE_NAME, "w") as file:
        for t in tasks:
            file.write(f"{t['task']} | {t['status']}\n")


def add_task(tasks):
    task_name = input("Enter task description: ")
    tasks.append({"task": task_name, "status": "Pending"})
    save_tasks(tasks)
    print("✅ Task added successfully!")


def view_tasks(tasks):
    if not tasks:
        print("📭 No tasks available.")
        return

    print("\n--- To-Do List ---")
    for i, t in enumerate(tasks, start=1):
        print(f"{i}. {t['task']} [{t['status']}]")
    print()


def mark_task_done(tasks):
    view_tasks(tasks)
    try:
        task_no = int(input("Enter task number to mark as done: "))
        if 1 <= task_no <= len(tasks):
            tasks[task_no - 1]["status"] = "Done"
            save_tasks(tasks)
            print("✅ Task marked as done!")
        else:
            print("❌ Invalid task number.")
    except ValueError:
        print("❌ Please enter a valid number.")


def main():
    tasks = load_tasks()

    while True:
        print("\n===== TO-DO LIST MENU =====")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Done")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            mark_task_done(tasks)
        elif choice == "4":
            print("👋 Exiting... Tasks saved.")
            break
        else:
            print("❌ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
