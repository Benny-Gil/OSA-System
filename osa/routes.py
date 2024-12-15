from flask import Flask
from flask import request
from flask import jsonify
from flask import render_template
from flask import redirect
from flask import url_for
from flask import session
from osa.services import osa_system

app = Flask(__name__)
app.secret_key = 'secret_key'


@app.route('/')
def index():
    return render_template('index.html')


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
        return render_template('admin.html', students=osa_system.students)
    return redirect(url_for('index'))


@app.route('/admin/approve_absence', methods=['POST'])
def approve_absence():
    if 'usertype' in session and session['usertype'] == 'admin':
        data = request.json
        email = data.get('email')
        date_absent = data.get('date_absent')
        admin_reason = data.get('admin_reason', '')

        student = next((s for s in osa_system.students
                        if s.email == email), None)
        if student:
            for absence in student.absences:
                if absence['date'] == date_absent:
                    absence['status'] = 'Approved'
                    absence['admin_reason'] = admin_reason
                    osa_system.save_data()
                    return jsonify({'success': True})
    return jsonify({'error': 'Unauthorized'}), 401


@app.route('/admin/deny_absence', methods=['POST'])
def deny_absence():
    if 'usertype' in session and session['usertype'] == 'admin':
        data = request.json
        email = data.get('email')
        date_absent = data.get('date_absent')
        admin_reason = data.get('admin_reason', '')

        student = next((s for s in osa_system.students
                        if s.email == email), None)
        if student:
            for absence in student.absences:
                if absence['date'] == date_absent:
                    absence['status'] = 'Denied'
                    absence['admin_reason'] = admin_reason
                    osa_system.save_data()
                    return jsonify({'success': True})
    return jsonify({'error': 'Unauthorized'}), 401


@app.route('/student')
def student():
    if 'usertype' in session and session['usertype'] == 'student':
        return render_template('student.html')
    return redirect(url_for('index'))


@app.route('/add_student', methods=['POST'])
def add_student():
    if 'usertype' in session and session['usertype'] == 'student':
        data = request.json
        required_fields = ['date_absent', 'reason', 'course']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        email = session['email']
        student = next((s for s in osa_system.students
                        if s.email == email), None)
        if student:
            name = student.name
            date_absent = data['date_absent']
            reason = data['reason']
            course = data['course']
            osa_system.add_student(name, email, date_absent, reason, course)
            results = osa_system.process_student(student)
            return jsonify(results)
    return jsonify({"error": "Unauthorized"}), 401


@app.route('/osaform')
def osaform():
    return render_template('osaform.html')


@app.route('/history')
def history():
    if 'usertype' in session and session['usertype'] == 'student':
        return render_template('history.html')
    return redirect(url_for('index'))


@app.route('/api/absences')
def api_absences():
    if 'usertype' in session and session['usertype'] == 'student':
        email = session['email']
        student = next((s for s in osa_system.students
                        if s.email == email), None)
        if student:
            return jsonify(student.absences)
    return jsonify([]), 404
