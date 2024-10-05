import json
import os

class Student:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.absences = []

    def add_absence(self, date_absent, reason, course):
        self.absences.append({'date': date_absent, 'reason': reason, 'course': course})

class OSASlip:
    def __init__(self, student):
        self.student = student

    def determine_slip(self, reason):
        excusable_reasons = ['medical issue', 'family emergency', 'university event']
        if reason.lower() in excusable_reasons:
            return False
        else:
            return True

class OSASystem:
    def __init__(self, json_file='osa_slips.json'):
        self.students = []
        self.json_file = json_file
        if os.path.exists(self.json_file):
            self.load_data()

    def add_student(self, name, email, date_absent, reason, course):
        for student in self.students:
            if student.email == email:
                print(f"Student with email {email} already exists. Adding new absence record.")
                student.add_absence(date_absent, reason, course)
                self.save_data()
                return
        
        student = Student(name, email)
        student.add_absence(date_absent, reason, course)
        self.students.append(student)
        self.save_data()

    def save_data(self):
        with open(self.json_file, 'w') as file:
            json.dump([student.__dict__ for student in self.students], file, indent=4)

    def load_data(self):
        with open(self.json_file, 'r') as file:
            student_data = json.load(file)
            for student in student_data:
                loaded_student = Student(student['name'], student['email'])
                loaded_student.absences = student['absences']
                self.students.append(loaded_student)

    def process_student(self, student):
        slip = OSASlip(student)
        for absence in student.absences:
            if slip.determine_slip(absence['reason']):
                print(f"{student.name}, you will be issued an OSA slip for your late/absence on {absence['date']} in {absence['course']}.")
            else:
                print(f"{student.name}, please go directly to the OSA office with supporting documents for the date {absence['date']} in {absence['course']}.")

    def run(self):
        course_codes = {
            "9372A": "CS 311", "9375B": "CS 311L", "9373A": "CS 312", "9373B": "CS 312L", "9374": "CS 313",
            "9375": "CS 314", "9376": "CS 315", "9377": "CSM 316", "9378": "CFE 105A"
        }
        
        course_names = {course: code for code, course in course_codes.items()}

        while True:
            print("Automated OSA Slip Distribution")
            name = input("Enter your name: ")
            email = input("Enter your student email: ")
            date_absent = input("Enter the date of late/absence (YYYY-MM-DD): ")
            reason = input("Enter the reason for your late/absence: ")

            print("\nSelect the course code or course name for the absence (e.g., 9372A or CS 311):")
            for code, course in course_codes.items():
                print(f"{code}: {course}")
            
            course_input = input("Enter the course code or course name: ").strip().upper()
            
            if course_input in course_codes:
                course = course_codes[course_input]
            elif course_input in course_names:
                course = course_input
                course_input = course_names[course]
            else:
                print("Invalid course code or name. Please try again.")
                continue

            self.add_student(name, email, date_absent, reason, course)

            for student in self.students:
                if student.email == email:
                    self.process_student(student)
                    break

            another = input("Do you want to process another student? (yes/no): ").strip().lower()
            if another != 'yes':
                break

if __name__ == "__main__":
    osa_system = OSASystem()
    osa_system.run()