# OSA Slip System

This is a Flask web application for managing and distributing OSA slips for student absences. The system allows students
to submit their absence details and determines whether an OSA slip should be issued based on the reason provided.

## Features

- Add student absence details
- Determine if an OSA slip should be issued
- Store and load student data from a JSON file

## Requirements

- Python 3.12
- Flask 3.1.0

## Installation

1. **Clone the repository**:
   ```sh
   git clone https://github.com/benny-gil/osa-slip-system.git
   cd osa-slip-system
    ```

## Running the Application

1. **Run the application**:

   ```sh
   python app.py
   ```

2. **Open the application in your browser**:
   ```sh
   # Default URL
   http://127.0.0.1:5000/
   ```

### Usage

Fill out the form on the homepage with the student's name, email, date of absence, reason for absence, and course code
or name. Submit the form to see if an OSA slip will be issued or if the student needs to visit the OSA office with
supporting
documents.

### Contributors
- Aguilar, Aaron Kyle 
- Lactaotao, Benny Gil A. 
- Fortaleza, Keanu Sonn 
- Caser, Prince 
- Madriaga, Rommel 
- Octavo, Sean Drei 