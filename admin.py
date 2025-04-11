import pandas as pd
from tkinter import messagebox
from utils import record_grade_update, validate_grade




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
    
def modify_grades(student_id, new_grades):
    """Update grades after validation"""
    try:
        if not all(validate_grade(g) for g in new_grades.values()):
            raise ValueError("All grades must be 0-100")
        
        grades = pd.read_csv('data/grades.txt')
        grades.loc[grades['id'] == student_id, list(new_grades.keys())] = list(new_grades.values())
        grades.to_csv('data/grades.txt', index=False)
        
        record_grade_update(student_id, new_grades)
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False
    
def modify_eca(student_id, activities):
    """Update ECA activities"""
    try:
        eca = pd.read_csv('data/eca.txt')
        eca.loc[eca['id'] == student_id, ['activity1', 'activity2', 'activity3']] = activities
        eca.to_csv('data/eca.txt', index=False)
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False

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
        
        # Initialize grade history with zeros
        initial_grades = {'math': 0, 'science': 0, 'english': 0, 'history': 0, 'art': 0}
        record_grade_update(username, initial_grades)  # <-- Add this line
        
        messagebox.showinfo("Success", "User added successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add user: {str(e)}")