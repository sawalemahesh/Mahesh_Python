RESULT_FILE = "results.txt"
PASS_FILE = "passed.txt"
FAIL_FILE = "failed.txt"

PASS_MARKS = 40

def process_results():
    passed_count = 0
    failed_count = 0

    try:
        with open(RESULT_FILE, "r") as file, \
             open(PASS_FILE, "w") as pass_file, \
             open(FAIL_FILE, "w") as fail_file:

            for line in file:
                name, marks = line.strip().split(",")
                marks = int(marks)

                if marks >= PASS_MARKS:
                    pass_file.write(f"{name},{marks}\n")
                    passed_count += 1
                else:
                    fail_file.write(f"{name},{marks}\n")
                    failed_count += 1

        print("Passed Students:", passed_count)
        print("Failed Students:", failed_count)

    except FileNotFoundError:
        print("Result file not found.")
    except ValueError:
        print("Invalid data format in file.")


process_results()
