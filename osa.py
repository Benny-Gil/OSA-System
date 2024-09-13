import json
import os

# Class representing a student
class Student:
    """
    Represents a student with a name, email, and a list of absences.
    
    Attributes:
        name : The name of the student.
        email : The email of the student.
        absences : A list of absences, where each absence is represented as a dictionary with 'date', 'reason', and 'course'.
    """
    def __init__(self, name, email):
        # Initializes a new Student instance with a name and email.
        self.name = name
        self.email = email
        self.absences = []  # List to store date, reason, and course

    def add_absence(self, date_absent, reason, course):
        """
        Adds an absence record for the student.
        
        Args:
            date_absent : The date of the absence in 'YYYY-MM-DD' format.
            reason : The reason for the absence.
            course : The course code or name associated with the absence.
        """
        self.absences.append({'date': date_absent, 'reason': reason, 'course': course})

# Class handling OSA slip logic
class OSASlip:
    """
    Handles the logic for determining whether a student should be issued an OSA slip.
    
    Attributes:
        student : The student for whom the slip is being determined.
    """
    def __init__(self, student):
        # Initializes a new OSASlip instance for a specific student.
        self.student = student

    def determine_slip(self, reason):
        """
        Determines if a slip should be issued based on the reason for absence.
        
        Args:
            reason: The reason for the absence.
        
        Returns:
            bool: True if a slip should be issued, False if the student should go directly to the OSA office.
        """
        # Define reasons that do not require an OSA slip
        excusable_reasons = ['medical issue', 'family emergency', 'university event']
        # If the reason is in the list of excusable reasons, no slip is needed
        if reason.lower() in excusable_reasons:
            return False
        else:
            return True

# Class handling the main OSA system logic
class OSASystem:
    """
    The main system for managing OSA slips for students.
    
    Attributes:
        students : A list of Student objects currently in the system.
        json_file : The path to the JSON file where student data is stored.
    """
    def __init__(self, json_file='osa_slips.json'):
        # Initializes the OSA system, loading existing student data if available.
        self.students = []  # Initialize an empty list to hold student data
        self.json_file = json_file  # JSON file for saving and loading data

        # Load existing data if file exists
        if os.path.exists(self.json_file):
            self.load_data()

    def add_student(self, name, email, date_absent, reason, course):
        """
        Adds a student to the system or updates an existing student's record.
        
        If a student with the given email already exists, adds the new absence to their record.
        Otherwise, creates a new student entry.
        
        Args:
            name : The name of the student.
            email : The email of the student.
            date_absent : The date of the absence in 'YYYY-MM-DD' format.
            reason : The reason for the absence.
            course : The course code or name for the absence.
        """
        # Check if student already exists
        for student in self.students:
            if student.email == email:
                print(f"Student with email {email} already exists. Adding new absence record.")
                student.add_absence(date_absent, reason, course)
                self.save_data()
                return
        
        # If student does not exist, create a new student
        student = Student(name, email)
        student.add_absence(date_absent, reason, course)
        self.students.append(student)
        self.save_data()

    def save_data(self):
        # Saves the current student data to the JSON file.
        with open(self.json_file, 'w') as file:
            # Convert student objects to dictionaries for JSON serialization
            json.dump([student.__dict__ for student in self.students], file, indent=4)

    def load_data(self):
        #Loads student data from the JSON file into the system.
        with open(self.json_file, 'r') as file:
            student_data = json.load(file)
            # Reconstruct Student objects from the loaded data
            for student in student_data:
                loaded_student = Student(student['name'], student['email'])
                loaded_student.absences = student['absences']
                self.students.append(loaded_student)

    def process_student(self, student):
        """
        Processes the student's absences and determines whether a slip is needed.
        
        Args:
            student: The student whose absences are being processed.
        """
        slip = OSASlip(student)
        # Check each absence to determine if a slip is needed
        for absence in student.absences:
            if slip.determine_slip(absence['reason']):
                print(f"{student.name}, you will be issued an OSA slip for your late/absence on {absence['date']} in {absence['course']}.")
            else:
                print(f"{student.name}, please go directly to the OSA office with supporting documents for the date {absence['date']} in {absence['course']}.")

    def run(self):
        # Runs the main loop of the OSA system, allowing for continuous processing of students.

        course_codes = {
            "9372A": "CS 311", "9375B": "CS 311L", "9373A": "CS 312", "9373B": "CS 312L", "9374": "CS 313",
            "9375": "CS 314", "9376": "CS 315", "9377": "CSM 316", "9378": "CFE 105A"
        }
        
        # Invert the dictionary for quick lookup by course name
        course_names = {course: code for code, course in course_codes.items()}

        while True:
            print("Automated OSA Slip Distribution")
            name = input("Enter your name: ")
            email = input("Enter your student email: ")
            date_absent = input("Enter the date of late/absence (YYYY-MM-DD): ")
            reason = input("Enter the reason for your late/absence: ")

            # Select course
            print("\nSelect the course code or course name for the absence (e.g., 9372A or CS 311):")
            for code, course in course_codes.items():
                print(f"{code}: {course}")
            
            # Input course code or name
            course_input = input("Enter the course code or course name: ").strip().upper()

            # Determine if the input is a valid course code or name
            if course_input in course_codes:
                course = course_codes[course_input]
            elif course_input in course_names:
                course = course_input
                course_input = course_names[course]
            else:
                print("Invalid course code or name. Please try again.")
                continue

            # Add or update the student's record
            self.add_student(name, email, date_absent, reason, course)
            
            # Process the student to check if they need a slip for the most recent absence
            for student in self.students:
                if student.email == email:
                    self.process_student(student)
                    break

            # Ask if the user wants to process another student
            another = input("Do you want to process another student? (yes/no): ").strip().lower()
            if another != 'yes':
                break

# Main execution
if __name__ == "__main__":
    osa_system = OSASystem()
    osa_system.run()