import json
import os

from osa.models import Student, OSASlip, User


class OSASystem:
    def __init__(self, users_file='data/users.json',
                 json_file='data/osa_slips.json'):
        self.students = []
        self.users = []
        self.json_file = json_file
        self.users_file = users_file
        if os.path.exists(self.json_file):
            self.load_data()
        if os.path.exists(self.users_file):
            self.load_users()

    def add_student(self, name, email, date_absent, reason, course):
        for student in self.students:
            if student.email == email:
                student.add_absence(date_absent, reason, course)
                self.save_data()
                return
        student = Student(name, email)
        student.add_absence(date_absent, reason, course)
        self.students.append(student)
        self.save_data()

    def save_data(self):
        with open(self.json_file, 'w') as file:
            json.dump([student.__dict__ for student
                       in self.students], file, indent=4)

    def load_data(self):
        with open(self.json_file, 'r') as file:
            student_data = json.load(file)
            for student in student_data:
                loaded_student = Student(student['name'], student['email'])
                loaded_student.absences = student['absences']
                self.students.append(loaded_student)

    def load_users(self):
        with open(self.users_file, 'r') as file:
            user_data = json.load(file)
            for user in user_data:
                self.users.append(User(user['email'],
                                       user['password'], user['usertype']))

    def validate_user(self, email, password):
        for user in self.users:
            if user.email == email and user.password == password:
                return user
        return None

    def process_student(self, student):
        slip = OSASlip(student)
        results = []
        for absence in student.absences:
            if slip.determine_slip(absence['reason']):
                results.append(
                    f"{student.name}, you will be issued an OSA slip for your "
                    f"late/absence on {absence['date']} "
                    f"in {absence['course']}."
                )
            else:
                results.append(
                    f"{student.name}, please go directly "
                    f"to the OSA office with supporting documents "
                    f"for the date {absence['date']} "
                    f"in {absence['course']}.")
        return results


osa_system = OSASystem()
