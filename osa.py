import json
import os

# Class representing a student
class Student:
    """
    Represents a student with a name, email, and a list of absences.
    
    Attributes:
        name (str): The name of the student.
        email (str): The email of the student.
        absences (list): A list of absences, where each absence is represented as a dictionary with 'date' and 'reason' keys.
    """
    def __init__(self, name, email):
        """
        Initializes a new Student instance with a name and email.
        
        Args:
            name (str): The name of the student.
            email (str): The email of the student.
        """
        self.name = name
        self.email = email
        self.absences = []  # List to store date and reason dictionaries

    def add_absence(self, date_absent, reason):
        """
        Adds an absence record for the student.
        
        Args:
            date_absent (str): The date of the absence in 'YYYY-MM-DD' format.
            reason (str): The reason for the absence.
        """
        self.absences.append({'date': date_absent, 'reason': reason})

# Class handling OSA slip logic
class OSASlip:
    """
    Handles the logic for determining whether a student should be issued an OSA slip.
    
    Attributes:
        student (Student): The student for whom the slip is being determined.
    """
    def __init__(self, student):
        """
        Initializes a new OSASlip instance for a specific student.
        
        Args:
            student (Student): The student for whom the slip logic will be applied.
        """
        self.student = student

    def determine_slip(self, reason):
        """
        Determines if a slip should be issued based on the reason for absence.
        
        Args:
            reason (str): The reason for the absence.
        
        Returns:
            bool: True if a slip should be issued, False if the student should go directly to the OSA office.
        """
        # Define reasons that do not require an OSA slip
        excusable_reasons = ['medical issue', 'family emergency', 'university event']
        # If the reason is in the list of excusable reasons, no slip is needed
        if reason.lower() in excusable_reasons:
            return False  # No slip needed, direct to OSA office
        else:
            return True  # Slip needed

# Class handling the main OSA system logic
class OSASystem:
    """
    The main system for managing OSA slips for students.
    
    Attributes:
        students (list): A list of Student objects currently in the system.
        json_file (str): The path to the JSON file where student data is stored.
    """
    def __init__(self, json_file='osa_slips.json'):
        """
        Initializes the OSA system, loading existing student data if available.
        
        Args:
            json_file (str): The filename where student data is stored. Defaults to 'osa_slips.json'.
        """
        self.students = []  # Initialize an empty list to hold student data
        self.json_file = json_file  # JSON file for saving and loading data

        # Load existing data if file exists
        if os.path.exists(self.json_file):
            self.load_data()

    def add_student(self, name, email, date_absent, reason):
        """
        Adds a student to the system or updates an existing student's record.
        
        If a student with the given email already exists, adds the new absence to their record.
        Otherwise, creates a new student entry.
        
        Args:
            name (str): The name of the student.
            email (str): The email of the student.
            date_absent (str): The date of the absence in 'YYYY-MM-DD' format.
            reason (str): The reason for the absence.
        """
        # Check if student already exists
        for student in self.students:
            if student.email == email:
                print(f"Student with email {email} already exists. Adding new absence record.")
                student.add_absence(date_absent, reason)
                self.save_data()
                return
        
        # If student does not exist, create a new student
        student = Student(name, email)
        student.add_absence(date_absent, reason)
        self.students.append(student)
        self.save_data()

    def save_data(self):
        """
        Saves the current student data to the JSON file.
        """
        with open(self.json_file, 'w') as file:
            # Convert student objects to dictionaries for JSON serialization
            json.dump([student.__dict__ for student in self.students], file, indent=4)

    def load_data(self):
        """
        Loads student data from the JSON file into the system.
        """
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
            student (Student): The student whose absences are being processed.
        """
        slip = OSASlip(student)
        # Check each absence to determine if a slip is needed
        for absence in student.absences:
            if slip.determine_slip(absence['reason']):
                print(f"{student.name}, you will be issued an OSA slip for your late/absence on {absence['date']}.")
            else:
                print(f"{student.name}, please go directly to the OSA office with supporting documents for the date {absence['date']}.")

    def run(self):
        """
        Runs the main loop of the OSA system, allowing for continuous processing of students.
        """
        while True:
            print("Automated OSA Slip Distribution")
            name = input("Enter your name: ")
            email = input("Enter your student email: ")
            date_absent = input("Enter the date of late/absence (YYYY-MM-DD): ")
            reason = input("Enter the reason for your late/absence: ")

            # Add or update the student's record
            self.add_student(name, email, date_absent, reason)
            
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
