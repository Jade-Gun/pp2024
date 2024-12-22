import os
import re
import sys
import random
from textwrap import dedent

STUDENTS: list[dict[str, str | list[dict[str, str | float]]]] = []
COURSES: list[dict[str, str]] = []

class BCOLORS:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def get_user_selection(options: list[str], default: int = 0) -> int:
    for i, option in enumerate(options):
        print(f"{BCOLORS.OKGREEN}{i+1}. {option}{BCOLORS.ENDC}")
    choice = input(f"Choose one of the above options (default: {default+1}): ")
    while True:
        try:
            if choice == "":
                return default
            choice = int(choice)
            if choice not in range(1, len(options) + 1):
                raise ValueError
            return choice - 1
        except ValueError:
            choice = input(f"{BCOLORS.FAIL}Invalid choice, try again: {BCOLORS.ENDC}")

def get_user_input_number(prompt: str, default: int = 0) -> int:
    choice = input(f"{prompt} (default: {default}): ")
    while True:
        try:
            if choice == "":
                return default
            choice = int(choice)
            return choice
        except ValueError:
            choice = input(f"{BCOLORS.FAIL}Invalid choice, try again: {BCOLORS.ENDC}")

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def add_student() -> None:
    student_name = input("\nEnter student name: ")

    student_id = input("Enter student ID (e.g., 23BI12325): ")
    while True:
        if not re.match(r"^\d{2}BI\d{5}$", student_id):  # Updated regex for the new format
            student_id = input(f"{BCOLORS.FAIL}Invalid ID, try again (format: 23BI12325): {BCOLORS.ENDC}")
            continue
        if next((True for student in STUDENTS if student["id"] == student_id), False):
            student_id = input(f"{BCOLORS.FAIL}ID already exists, try again: {BCOLORS.ENDC}")
            continue
        break

    student_dob = input("Enter student date of birth (YYYY-MM-DD): ")
    while True:
        if not re.match(r"\d{4}-\d{2}-\d{2}", student_dob):
            student_dob = input(f"{BCOLORS.FAIL}Invalid date of birth, try again: {BCOLORS.ENDC}")
            continue
        break

    marks: list[dict[str, str | float]] = []
    STUDENTS.append({"name": student_name, "id": student_id, "dob": student_dob, "marks": marks})

def add_course() -> None:
    course_name = input("Enter course name: ")
    while next((True for course in COURSES if course["name"] == course_name), False):
        course_name = input(f"{BCOLORS.FAIL}Course already exists, try again: {BCOLORS.ENDC}")

    course_id = input("Enter course ID (e.g., 23C123): ")  # You may want to apply a similar format here
    while next((True for course in COURSES if course["id"] == course_id), False):
        course_id = input(f"{BCOLORS.FAIL}ID already exists, try again: {BCOLORS.ENDC}")

    COURSES.append({"name": course_name, "id": course_id})

def add_mark() -> None:
    if not STUDENTS or not COURSES:
        print(f"{BCOLORS.FAIL}No students or courses available to add marks.{BCOLORS.ENDC}")
        return

    student_id = get_user_selection([student["id"] for student in STUDENTS], 0)
    course_id = get_user_selection([course["id"] for course in COURSES], 0)

    mark = input("Enter mark (0-20): ")
    while True:
        try:
            mark = float(mark)
            if mark < 0 or mark > 20:
                raise ValueError
            break
        except ValueError:
            mark = input(f"{BCOLORS.FAIL}Invalid mark, try again: {BCOLORS.ENDC}")

    STUDENTS[student_id]["marks"].append({"course_id": COURSES[course_id]["id"], "mark": mark})

def format_str(content: str, width: int) -> str:
    return f"| {content}{' '*(width-len(content))} "

def print_table() -> None:
    if not STUDENTS or not COURSES:
        print(f"{BCOLORS.WARNING}No data to display.{BCOLORS.ENDC}")
        return

    headers = ["Data", "ID", "DOB"] + [f"Course: {course['name']}" for course in COURSES]
    column_width = max(len(header) for header in headers)

    print(format_str("Data", column_width), end="")
    for student in STUDENTS:
        print(format_str(student["name"], column_width), end="")
    print()

    print("=" * (column_width + 3), end="")
    for _ in STUDENTS:
        print("=" * (column_width + 3), end="")
    print()

    print(format_str("ID", column_width), end="")
    for student in STUDENTS:
        print(format_str(student["id"], column_width), end="")
    print()

    print(format_str("DOB", column_width), end="")
    for student in STUDENTS:
        print(format_str(student["dob"], column_width), end="")
    print()

    for course in COURSES:
        print(format_str(f"Course: {course['name']}", column_width), end="")
        for student in STUDENTS:
            mark = next((str(m["mark"]) for m in student["marks"] if m["course_id"] == course["id"]), "")
            print(format_str(mark, column_width), end="")
        print()

def main():
    last_message = ""
    while True:
        clear_screen()
        if last_message:
            print(last_message + "\n")
            last_message = ""

        print(f"{BCOLORS.HEADER}Student Mark Management System{BCOLORS.ENDC}")
        print(dedent("""\
            [1] Add student
            [2] Add course
            [3] Add mark
            [4] Show student marks
            [5] Exit
            [6] Add sample data
        """))
        
        choice = get_user_input_number("Choose one of the above options", 1)

        match choice:
            case 1:
                number_of_students_to_add = get_user_input_number("How many students do you want to add", 1)
                for _ in range(number_of_students_to_add):
                    add_student()
            case 2:
                number_of_courses_to_add = get_user_input_number("How many courses do you want to add", 1)
                for _ in range(number_of_courses_to_add):
                    add_course()
            case 3:
                number_of_marks_to_add = get_user_input_number("How many marks do you want to add", 1)
                for _ in range(number_of_marks_to_add):
                    add_mark()
            case 4:
                print_table()
                input("\nPress enter to continue...")
            case 5:
                break
            case 6:
                # Sample data addition
                for _ in range(5):
                    id = f"{random.randint(20, 29)}BI{random.randint(100, 999)}"
                    while id in [student["id"] for student in STUDENTS]:
                        id = f"{random.randint(20, 29)}BI{random.randint(100, 999)}"
                    name = random.choice(["John", "Jane", "Jack", "Jill", "Jenny", "Jen", "Jenifer", "Jeniffer"])
                    dob = f"{random.randint(1990, 2000)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
                    STUDENTS.append({"id": id, "name": name, "dob": dob, "marks": []})

                for _ in range(5):
                    id = f"{random.randint(20, 29)}C{random.randint(100, 999)}"
                    while id in [course["id"] for course in COURSES]:
                        id = f"{random.randint(20, 29)}C{random.randint(100, 999)}"

                    courses_list = ["Maths", "Physics", "Chemistry", "Biology", "English", "History", "Geography"]
                    course = random.choice(courses_list)
                    while course in [course["name"] for course in COURSES]:
                        course = random.choice(courses_list)

                    COURSES.append({"id": id, "name": course})

                for student in STUDENTS:
                    for course in COURSES:
                        student_marks: list[dict[str, str | float]] = student["marks"]
                        student_marks.append({"course_id": course["id"], "mark": random.randint(0, 20)})
                last_message = f"{BCOLORS.OKGREEN}Sample data added{BCOLORS.ENDC}"
            case _:
                print(f"{BCOLORS.FAIL}Invalid choice.{BCOLORS.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{BCOLORS.FAIL}Exiting...{BCOLORS.ENDC}")
        sys.exit(0)