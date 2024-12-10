import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))

import unittest
from osa.models import Student, User
from osa.services import OSASystem


class TestOSASystem(unittest.TestCase):

    def setUp(self):
        self.osa_system = OSASystem(users_file='test_users.json',
                                    json_file='test_osa_slips.json')
        self.osa_system.students = []
        self.osa_system.users = []

    def tearDown(self):
        if os.path.exists('test_users.json'):
            os.remove('test_users.json')
        if os.path.exists('test_osa_slips.json'):
            os.remove('test_osa_slips.json')

    def test_add_student(self):
        self.osa_system.add_student('John Doe', 'john@example.com',
                                    '2023-10-01', 'Sick', 'Math')
        self.assertEqual(len(self.osa_system.students), 1)
        self.assertEqual(self.osa_system.students[0].name, 'John Doe')
        self.assertEqual(self.osa_system.students[0].email, 'john@example.com')
        self.assertEqual(len(self.osa_system.students[0].absences), 1)

    def test_save_and_load_data(self):
        self.osa_system.add_student('John Doe', 'john@example.com',
                                    '2023-10-01', 'Sick', 'Math')
        self.osa_system.save_data()
        self.osa_system.students = []
        self.osa_system.load_data()
        self.assertEqual(len(self.osa_system.students), 1)
        self.assertEqual(self.osa_system.students[0].name, 'John Doe')

    def test_validate_user(self):
        user = User('admin@example.com', 'password', 'admin')
        self.osa_system.users.append(user)
        validated_user = self.osa_system.validate_user('admin@example.com',
                                                       'password')
        self.assertIsNotNone(validated_user)
        self.assertEqual(validated_user.email, 'admin@example.com')

    def test_process_student(self):
        student = Student('John Doe', 'john@example.com')
        student.add_absence('2023-10-01', 'Sick', 'Math')
        self.osa_system.students.append(student)
        results = self.osa_system.process_student(student)
        self.assertEqual(len(results), 1)
        self.assertIn('John Doe', results[0])


if __name__ == '__main__':
    unittest.main()
