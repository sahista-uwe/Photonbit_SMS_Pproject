import pandas as pd
from tkinter import messagebox
from utils import record_grade_update

def add_user(username, name, password, role, email, phone):
    """Add new user with pandas"""
    try:
        # Update users
        users = pd.read_csv('data/users.txt')
        new_user = pd.DataFrame([[username, name, role, email, phone]],
                                columns=users.columns)
        pd.concat([users, new_user]).to_csv('data/users.txt', index=False)
        
        # Update passwords
        passwords = pd.read_csv('data/passwords.txt')
        new_pass = pd.DataFrame([[username, password]],
                                columns=passwords.columns)
        pd.concat([passwords, new_pass]).to_csv('data/passwords.txt', index=False)
        
        # Initialize grades
        grades = pd.read_csv('data/grades.txt')
        new_grade = pd.DataFrame([[username, 0, 0, 0, 0, 0]],
                                columns=grades.columns)
        pd.concat([grades, new_grade]).to_csv('data/grades.txt', index=False)
        
        messagebox.showinfo("Success", "User added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add user: {str(e)}")

        
def update_grades(username, new_grades):
    """Update student grades and record history"""
    try:
        grades = pd.read_csv('data/grades.txt')
        grades.loc[grades['id'] == username, ['math','science','english','history','art']] = new_grades
        grades.to_csv('data/grades.txt', index=False)
        
        # Record in history
        record_grade_update(username, new_grades)
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False