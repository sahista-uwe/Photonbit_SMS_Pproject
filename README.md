PhotoBit Student Management System

Programming Language: Python 3.8+

GUI Framework: CustomTkinter

Data Handling: Pandas

Data Visualization: Matplotlib


Project Overview

The PhotoBit Student Management System is a user-friendly, Python-based application that manages student academic records, personal information, 

and extracurricular activities. It offers secure login, role-based access, and visual performance analytics.


Features

Secure User Authentication (Admin & Student roles)

Admin Control Panel for managing student data

Performance Visualizations using Matplotlib

Longitudinal Analysis of academic performance

Student Portal for profile management and academic tracking


Tech Stack

Component           Tool

Language	          Python 3.8+

GUI Framework	      CustomTkinter

Data Handling	      Pandas

Visualization	      Matplotlib

Message Boxes	      CTkMessagebox

Data Persistence	  CSV / TXT Files


File Structure

PhotoBit_Student_System/

├── main.py             # App entry point

├── auth.py             # Authentication logic

├── admin.py            # Admin dashboard logic

├── student.py          # Student portal features

├── models.py           # Object classes (User, Admin, Student)

├── utils.py            # Helper functions and data init

├── README.md           # Project documentation

├── screenshots/        # Interface screenshots (to be added)

│

├── data/

│   ├── users.txt       # User profiles

│   ├── passwords.txt   # Credentials (plaintext for demo only)

│   ├── grades.txt      # Student grades

│   ├── eca.txt         # Extracurricular activity records

│

└── grade_history/      # Historical grade performance data


Authentication System
Username/password login system
Role-based access: Admin vs Student
Error handling for invalid credentials

Note:
Passwords are stored in plain text (passwords.txt) for educational purposes. In a production environment, you should implement password hashing (e.g., using bcrypt) and secure database storage.

Administrator Dashboard
Create, edit, delete user accounts
View and manage student academic records
Record and update extracurricular activity participation
Generate analytical reports:
   Subject-wise performance
   Grade trends
   Activity-to-performance correlation

Student Dashboard
View personal and academic information
Access subject-wise performance and historical grades
Monitor class ranking and trends
Update personal contact details
Data Visualization Examples
(Screenshots will be added later)

admin_dashboard.png

student_performance.png

eca_analysis.png

Installation and Setup
Prerequisites
Python 3.8 or higher

Install required packages:
pip install customtkinter pandas matplotlib CTkMessagebox
Run the System

python main.py
To initialize the data files (if not already created):


python utils.py
Default Login Credentials
Role	Username	Password
Admin	admin	admin123

License
This project is licensed under the MIT License.

Developer Info
Author: Sahista Gurung, Chelsey, Shrestha, Swapnil Shrestha
Email: sahistagurung@gmail.com
