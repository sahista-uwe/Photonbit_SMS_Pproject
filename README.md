# PhotoBit Student Management System

**Programming Language:** Python 3.8+  
**GUI Framework:** CustomTkinter  
**Data Handling:** Pandas  
**Data Visualization:** Matplotlib  

## Project Overview

PhotoBit is a user-friendly, Python-based student management system designed to manage academic records, personal details, and extracurricular activities. It provides secure login, role-based access, and performance visualizations to enhance user experience and decision-making.

## Features

- Secure User Authentication (Admin & Student roles)  
- Admin Control Panel for managing student data  
- Performance Visualizations with Matplotlib  
- Longitudinal Analysis of academic trends  
- Student Portal for academic tracking and profile management  

## Tech Stack

| Component          | Tool             |
|--------------------|------------------|
| Language           | Python 3.8+       |
| GUI Framework      | CustomTkinter     |
| Data Handling      | Pandas            |
| Visualization      | Matplotlib        |
| Message Boxes      | CTkMessagebox     |
| Data Persistence   | TXT Files   |

## File Structure

```
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

```

## Authentication System

- Username/password login system  
- Role-based access (Admin / Student)  
- Error handling for invalid credentials  

Note: Passwords are stored in plain text (`passwords.txt`) for demonstration purposes. For production, implement password hashing (e.g., with `bcrypt`) and use a secure database.

## Administrator Dashboard

- Create, edit, and delete user accounts  
- Manage academic records and extracurricular activities  
- Generate reports:
  - Subject-wise performance
  - Grade trends
  - Activity-to-performance correlation  

## Student Dashboard

- View personal and academic information  
- Access subject-wise performance and historical grades  
- Track class ranking and trends  
- Update personal contact details  

## Data Visualization (Coming Soon)

- admin_dashboard.png  
- student_performance.png  
- eca_analysis.png  

## Installation & Setup

### Prerequisites

- Python 3.8 or higher

### Install Required Packages

```bash
pip install customtkinter pandas matplotlib CTkMessagebox
```

### Run the System

```bash
python main.py
```

To initialize data files (if not already created):

```bash
python utils.py
```

## Default Login Credentials

| Role    | Username | Password  |
|---------|----------|-----------|
| Admin   | admin    | admin123  |

## License

This project is licensed under the MIT License.

## Developer Info

**Authors:**  
- Sahista Gurung  
- Chelsey Shrestha  
- Swapnil Shrestha  

Contact: sahistagurung@gmail.com

