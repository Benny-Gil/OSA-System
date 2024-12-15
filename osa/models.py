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

    def add_absence(self, date_absent, reason,
                    course, status='Pending', admin_reason=''):
        self.absences.append(
            {'date': date_absent, 'reason': reason, 'course': course,
             'status': status, 'admin_reason': admin_reason})


class OSASlip:
    def __init__(self, student):
        self.student = student

    def determine_slip(self, reason):
        excusable_reasons = ['medical issue',
                             'family emergency', 'university event']
        return reason.lower() not in excusable_reasons
