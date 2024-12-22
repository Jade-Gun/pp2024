from __future__ import annotations
import os
import re
import sys
import random
from datetime import datetime


def hr1():
    return print("-" * 30)


def hr2():
    return print("=" * 30)


class BCOLORS:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class Func:
    def get_user_selection(self, options: list[str], default: int = 0) -> int:
        """Get user selection from a list of options and return the index of the selected option."""
        for i, option in enumerate(options):
            print(f"{BCOLORS.OKGREEN}{i+1}. {option}{BCOLORS.ENDC}")
        choice = input(f"choose one of the above options (default: {default+1}): ")
        while True:
            try:
                if choice == "":
                    return default
                choice = int(choice)
                if choice not in range(1, len(options) + 1):
                    raise ValueError
                return choice - 1
            except ValueError:
                choice = input(f"{BCOLORS.FAIL}invalid choice, try again: {BCOLORS.ENDC}")

    def get_user_input_number(self, prompt: str, default: int = 0) -> int:
        """Get user input positive integer number."""
        choice = input(f"{prompt} (default: {default}): ")
        while True:
            try:
                if choice == "":
                    return default
                choice = int(choice)
                return choice
            except ValueError:
                choice = input(f"{BCOLORS.FAIL}invalid choice, try again: {BCOLORS.ENDC}")

    def format_str(self, content: str, width: int) -> str:
        """Format string to fit in a table cell."""
        return f"| {content}{' '*(width-len(content))} "


class BasicInfo:
    def __init__(self, name: str, id: str):
        self.__name = name
        self.__id = id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def id(self) -> str:
        return self.__id

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name

    @id.setter
    def id(self, id: str) -> None:
        self.__id = id


class Student(BasicInfo):
    def __init__(self, name: str, id: str, dob: str):
        super().__init__(name=name, id=id)
        self.__dob = dob
        self.__courses_marks: list[Mark] = []

    @property
    def dob(self) -> str:
        return self.__dob

    @property
    def courses_marks(self) -> list[Mark]:
        return self.__courses_marks

    def add_mark(self, course_id: str, attendance: float, midterm: float, final: float) -> None:
        for index, course_marks in enumerate(self.__courses_marks):
            if course_marks.course_id == course_id:
                self.__courses_marks[index] = Mark(course_id, attendance, midterm, final)
                break
        else:
            self.__courses_marks.append(Mark(course_id, attendance, midterm, final))


class Classroom:
    def __init__(self):
        self.__students: list[Student] = []

    def add_student(self):
        student_name = input("\nenter student name: ")
        student_id = input("enter student id (2xBIxxxxx): ").upper()

        # === Verify student ID ===
        while True:
            if re.match(r"^\d{2}BI\d{5}$", student_id):
                for student in self.__students:
                    if student.id == student_id:
                        student_id = input(
                            f"{BCOLORS.FAIL}another student has the same id, try again: {BCOLORS.ENDC}"
                        ).upper()
                        break
                else:
                    break
            else:
                student_id = input(f"{BCOLORS.FAIL}invalid id, try again: {BCOLORS.ENDC}")

        student_dob = input("enter student date of birth (dd-mm-yyyy): ")

        # === Validate date of birth ===
        while True:
            try:
                if re.match(r"\d{2}-\d{2}-\d{4}", student_dob):
                    break

                day, month, year = student_dob.split("-")
                day, month, year = int(day), int(month), int(year)

                is_leap_year = (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
                valid_day = (
                    month in (1, 3, 5, 7, 8, 10, 12)
                    and 1 <= day <= 31
                    or month in (4, 6, 9, 11)
                    and 1 <= day <= 30
                    or month == 2
                    and 1 <= day <= 29
                    and is_leap_year
                    or month == 2
                    and 1 <= day <= 28
                    and not is_leap_year
                )
                valid_month = 1 <= month <= 12
                valid_year = 1900 <= year <= datetime.now().year

                if not valid_day or not valid_month or not valid_year:
                    raise ValueError
                break
            except ValueError:
                student_dob = input(f"{BCOLORS.FAIL}invalid date of birth, try again: {BCOLORS.ENDC}")

        self.__students.append(Student(student_name, student_id, student_dob))

    def add_mark(self, courses: list[BasicInfo]) -> None:
        print(f"{BCOLORS.BOLD}Select student:{BCOLORS.ENDC}")
        student_index_selected = Func.get_user_selection(
            [f"{student.name} (ID {student.id})" for student in self.__students], 0
        )
        student_id_selected = self.__students[student_index_selected].id

        print(f"{BCOLORS.BOLD}Select course:{BCOLORS.ENDC}")
        course_index_selected = Func.get_user_selection([f"{course.name} (ID {course.id})" for course in courses], 0)
        course_id_selected = courses[course_index_selected].id

        # === Print student's marks of the selected course if exist ===
        for _, student in enumerate(self.__students):
            if student.id != student_id_selected:
                continue
            if len(student.courses_marks) == 0:
                break
            for course_marks in student.courses_marks:
                if course_marks.course_id != course_id_selected:
                    continue
                print(f"{BCOLORS.BOLD}{student.name}'s mark of {courses[course_index_selected].name}: {BCOLORS.ENDC}")
                print(
                    # f"{BCOLORS.BOLD}attendance: {course_marks.attendance}, midterm: {course_marks.midterm}, final: {course_marks.final}{BCOLORS.ENDC}"
                    "{}attendance: {}, midterm: {}, final: {}{}".format(
                        BCOLORS.BOLD, course_marks.attendance, course_marks.midterm, course_marks.final, BCOLORS.ENDC
                    )
                )

        marks_input = input(
            "enter attendance, mid-term, final mark (separated by comma, _ for empty mark, mark must be in range [0, 20]): "
        )
        marks = marks_input.split(",")
        print(marks)
        while True:
            try:
                if len(marks) != 3:
                    raise ValueError
                for mark in marks:
                    if mark != "_":
                        mark = float(mark)
                        if mark < 0 or mark > 20:
                            raise ValueError
                    else:
                        mark = -1
                attendance, midterm, final = marks
                break
            except ValueError:
                marks_input = input(f"{BCOLORS.FAIL}invalid marks, try again: {BCOLORS.ENDC}")
                marks = marks_input.split(",")

        self.__students[student_index_selected].add_mark(course_id_selected, attendance, midterm, final)

    def print_table(self, courses: list[BasicInfo]) -> None:
        func = Func()

        data_column_content = ["Data", "ID", "DOB"]
        data_column_content.extend([f"Course: {course.name}" for course in courses])
        data_column_width = max([len(content) for content in data_column_content])
        del data_column_content

        student_col_width: list[int] = []
        for student in self.__students:
            student_column_content = [student.name, student.id, student.dob]
            for course_marks in student.courses_marks:
                attendance, midterm, final, gpa = (
                    course_marks.attendance,
                    course_marks.midterm,
                    course_marks.final,
                    course_marks.gpa,
                )
                string_to_print = f"{attendance} {midterm} {final} {gpa}"
                student_column_content.append(string_to_print)
            student_col_width.append(max([len(content) for content in student_column_content]))

        # First row
        print(func.format_str(content="Data", width=data_column_width), end="")
        for i, student in enumerate(self.__students):
            print(func.format_str(content=student.name, width=student_col_width[i]), end="")
        print()

        # Seperator row
        print("=" * (data_column_width + 3), end="")
        for width in student_col_width:
            print("=" * (width + 3), end="")
        print()

        print(func.format_str(content="ID", width=data_column_width), end="")
        for i, student in enumerate(self.__students):
            print(func.format_str(content=student.id, width=student_col_width[i]), end="")
        print()

        print(func.format_str(content="DOB", width=data_column_width), end="")
        for i, student in enumerate(self.__students):
            print(func.format_str(content=student.dob, width=student_col_width[i]), end="")
        print()

        for course in courses:
            print(func.format_str(content=f"Course: {course.name}", width=data_column_width), end="")
            for i, student in enumerate(self.__students):
                for course_marks in student.courses_marks:
                    if course_marks.course_id == course.id:
                        attendance, midterm, final, gpa = (
                            course_marks.attendance,
                            course_marks.midterm,
                            course_marks.final,
                            course_marks.gpa,
                        )
                        string_to_print = f"{attendance} {midterm} {final} {gpa}"
                        print(func.format_str(content=string_to_print, width=student_col_width[i]), end="")
                        break
                else:
                    print(func.format_str(content="", width=student_col_width[i]), end="")
            print()

    def overwrite_students(self, students: list[Student]) -> None:
        self.__students = students


class Mark:
    def __init__(self, id: str, attendance: float = -1, midterm: float = -1, final: float = -1):
        self.attendance: float = attendance
        self.midterm: float = midterm
        self.final: float = final
        self.__gpa: float = -1
        self.course_id: str = id

    @property
    def gpa(self) -> float:
        if self.__gpa == -1:
            self.__calculate_gpa()
        return self.__gpa

    @property
    def course_id(self) -> str:
        return self.course_id

    @gpa.setter
    def gpa(self, gpa: float) -> None:
        self.__gpa = gpa

    def __calculate_gpa(self) -> float:
        self.attendance = 0 if self.attendance == -1 else self.attendance
        self.midterm = 0 if self.midterm == -1 else self.midterm
        self.final = 0 if self.final == -1 else self.final
        self.gpa = round((self.attendance * 0.1 + self.midterm * 0.3 + self.final * 0.6), 2)
        return self.__gpa


class Courses:
    def __init__(self):
        self.__courses: list[BasicInfo] = []

    def add_course(self) -> None:
        course_name_entered = input("\nenter course name: ")
        course_id_entered = input("enter course id: ")

        for course in self.__courses:
            if course.name == course_name_entered or course.id == course_id_entered:
                print(f"{BCOLORS.FAIL}course already exists{BCOLORS.ENDC}")
                return

        self.__courses.append(BasicInfo(course_name_entered, course_id_entered))

    @property
    def list_course(self) -> list[BasicInfo]:
        return self.__courses

    def overwrite_courses(self, courses: list[BasicInfo]) -> None:
        self.__courses = courses


def main():
    classroom = Classroom()
    courses = Courses()

    last_message = ""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(last_message + "\n") if last_message else None
        last_message = ""

        print(f"{BCOLORS.HEADER}Student Mark Management System{BCOLORS.ENDC}")
        hr2()
        print(f"{BCOLORS.OKBLUE}[1]{BCOLORS.ENDC} Add student")
        print(f"{BCOLORS.OKBLUE}[2]{BCOLORS.ENDC} Add course")
        print(f"{BCOLORS.OKBLUE}[3]{BCOLORS.ENDC} Add mark")
        print(f"{BCOLORS.OKBLUE}[4]{BCOLORS.ENDC} Show student marks")
        print(f"{BCOLORS.OKBLUE}[5]{BCOLORS.ENDC} Exit")
        hr2()
        print(f"{BCOLORS.OKBLUE}[6]{BCOLORS.ENDC} Add sample data")

        choice = input("Choose one of the above options: ")
        while True:
            try:
                choice = int(choice)
                if choice not in range(1, 7):
                    raise ValueError
                break
            except ValueError:
                choice = input(f"{BCOLORS.FAIL}invalid choice, try again: {BCOLORS.ENDC}")

        match choice:
            case 1:
                number_of_students_to_add = Func.get_user_input_number("# of student to add", 1)
                for _ in range(number_of_students_to_add):
                    classroom.add_student()
            case 2:
                number_of_courses_to_add = Func.get_user_input_number("# of course to add", 1)
                for _ in range(number_of_courses_to_add):
                    courses.add_course()
            case 3:
                number_of_marks_to_add = Func.get_user_input_number("# of mark to add", 1)
                for _ in range(number_of_marks_to_add):
                    hr1()
                    classroom.add_mark(courses.list_course)
            case 4:
                print()
                classroom.print_table(courses.list_course)
            case 5:
                break
            case 6:
                STUDENTS_DATA: list[Student] = []
                COURSES_DATA: list[BasicInfo] = []

                # Random student data
                for _ in range(5):
                    random_id = f"BI20-{random.randint(100, 999)}"
                    while random_id in [student.id for student in STUDENTS_DATA]:
                        random_id = f"BI20-{random.randint(100, 999)}"
                    random_name = random.choice(
                        ["Alice", "John", "Bob", "Mary", "Jane", "Peter", "Paul", "Mark", "Sarah", "Sara"]
                    )
                    random_dob = f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(1990, 2000)}"
                    STUDENTS_DATA.append(Student(id=random_id, name=random_name, dob=random_dob))

                # Random courses data
                for _ in range(5):
                    random_id = f"subject-{random.randint(100, 999)}"
                    while random_id in [course.id for course in COURSES_DATA]:
                        random_id = f"subject-{random.randint(100, 999)}"

                    course_random_list = [
                        "Maths",
                        "Physics",
                        "Chemistry",
                        "Biology",
                        "English",
                        "History",
                        "Geography",
                        "Computer Science",
                        "Art",
                        "Music",
                    ]
                    random_course = random.choice(course_random_list)
                    while random_course in [course.name for course in COURSES_DATA]:
                        random_course = random.choice(course_random_list)
                        if len(COURSES_DATA) >= len(course_random_list):
                            break

                    COURSES_DATA.append(BasicInfo(id=random_id, name=random_course))

                # Random marks data for each student in each course
                for student in STUDENTS_DATA:
                    for course in COURSES_DATA:
                        attendance, midterm, final = random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)
                        student.add_mark(course.id, attendance, midterm, final)
                last_message = f"{BCOLORS.OKGREEN}sample data added{BCOLORS.ENDC}"

                classroom.overwrite_students(STUDENTS_DATA)
                courses.overwrite_courses(COURSES_DATA)
            case _:
                print(f"{BCOLORS.FAIL}invalid choice{BCOLORS.ENDC}")
        input("\npress enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"{BCOLORS.FAIL}\nexiting...{BCOLORS.ENDC}")
        sys.exit(0)
