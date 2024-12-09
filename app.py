from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

class User:
    def __init__(self, email, password, usertype):
        self.email = email
        self.password = password
        self.usertype = usertype

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
        return reason.lower() not in excusable_reasons

class OSASystem:
    def __init__(self, users_file='users.json', json_file='osa_slips.json'):
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
            json.dump([student.__dict__ for student in self.students], file, indent=4)

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
                self.users.append(User(user['email'], user['password'], user['usertype']))

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
                results.append(f"{student.name}, you will be issued an OSA slip for your late/absence on {absence['date']} in {absence['course']}.")
            else:
                results.append(f"{student.name}, please go directly to the OSA office with supporting documents for the date {absence['date']} in {absence['course']}.")
        return results

osa_system = OSASystem()

# Routes
@app.route('/')
def index():
    return render_template('student.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = osa_system.validate_user(email, password)
    if user:
        session['email'] = user.email
        session['usertype'] = user.usertype
        if user.usertype == 'admin':
            return jsonify({'redirect': '/admin'})
        elif user.usertype == 'student':
            return jsonify({'redirect': '/student'})
    return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/admin')
def admin():
    if 'usertype' in session and session['usertype'] == 'admin':
        return render_template('admin.html')
    return redirect(url_for('index'))

@app.route('/student')
def student():
    if 'usertype' in session and session['usertype'] == 'student':
        return render_template('student.html')
    return redirect(url_for('index'))

@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    required_fields = ['name', 'email', 'date_absent', 'reason', 'course']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    name = data['name']
    email = data['email']
    date_absent = data['date_absent']
    reason = data['reason']
    course = data['course']
    osa_system.add_student(name, email, date_absent, reason, course)
    for student in osa_system.students:
        if student.email == email:
            results = osa_system.process_student(student)
            return jsonify(results)
    return jsonify({"error": "Student not found"}), 404

@app.route('/osaform')
def osaform():
    return render_template('osaform.html')

if __name__ == '__main__':
    app.run(debug=True)