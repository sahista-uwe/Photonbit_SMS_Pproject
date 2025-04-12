#this is admin.py
import pandas as pd
import os

from tkinter import messagebox
from utils import (
    record_grade_update, 
    validate_grade,
    validate_email,
    validate_phone
)
from auth import hash_password


def add_user(username, name, password, role, email, phone):
    
    try:
        if not validate_email(email):
            return False, "Invalid email format"
        if phone and not validate_phone(phone):
            return False, "Invalid phone number"
        
    except pd.errors.EmptyDataError:
        # Handle empty files
        return False, "Data files corrupted. Please contact admin"
    except FileNotFoundError:
        return False, "Data files missing. Please reinstall system"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"
    try:

        # 1. Ensure 'data' folder exists
        os.makedirs("data", exist_ok=True)

        # 2. Load or create files
        users_path = "data/users.txt"
        passwords_path = "data/passwords.txt"
        grades_path = "data/grades.txt"

        # Initialize files if missing
        for file, columns in [
            (users_path, ["username", "name", "role", "email", "phone"]),
            (passwords_path, ["username", "password"]),
            (grades_path, ["username", "math", "science", "english", "history", "art"])
        ]:
            if not os.path.exists(file):
                pd.DataFrame(columns=columns).to_csv(file, index=False)

        # 3. Check for duplicate username
        users = pd.read_csv(users_path)
        if username in users["username"].values:
            return False, "Username already exists!"

        # 4. Hash password
        hashed_pw = hash_password(password)

        # 5. Save user data
        new_user = pd.DataFrame([[username, name, role, email, phone]], columns=['username', 'name', 'role', 'email', 'phone'])
        users = pd.concat([users, new_user], ignore_index=True)
        users.to_csv(users_path, index=False)

        # 6. Save password
        passwords = pd.read_csv(passwords_path)
        new_pass = pd.DataFrame([[username, hashed_pw]], columns=passwords.columns)
        passwords = pd.concat([passwords, new_pass], ignore_index=True)
        passwords.to_csv(passwords_path, index=False)

        # 7. Initialize grades
        grades = pd.read_csv(grades_path)
        new_grade = pd.DataFrame([[username, 0, 0, 0, 0, 0]], columns=grades.columns)
        grades = pd.concat([grades, new_grade], ignore_index=True)
        grades.to_csv(grades_path, index=False)

        # 8. Record in history
        record_grade_update(username, {"math":0, "science":0, "english":0, "history":0, "art":0})

        eca_df = pd.read_csv('data/eca.txt')
        if username not in eca_df['username'].values:
            new_eca = pd.DataFrame({
                'username': [username],
                'activity1': ['None'],
                'activity2': ['None'],
                'activity3': ['None']
            })
            eca_df = pd.concat([eca_df, new_eca], ignore_index=True)
            eca_df.to_csv('data/eca.txt', index=False)
        return True, "User added successfully!"

    except Exception as e:
        return False, f"Error saving data: {str(e)}"


        
def update_grades(username, new_grades):
    """Update student grades - returns (success, message) """
    try:
        grades = pd.read_csv('data/grades.txt')
        grades.loc[grades['username'] == username, list(new_grades.keys())] = list(new_grades.values())
        grades.to_csv('data/grades.txt', index=False)
        
        record_grade_update(username, new_grades)
        return True, "Grades updated successfully"
    except Exception as e:
        return False, f"Grade update failed: {str(e)}"

def modify_grades(student_id, new_grades):
    """Update grades after validation"""
    try:
        if not all(validate_grade(g) for g in new_grades.values()):
            return False, "All grades must be 0-100"
            
        grades = pd.read_csv('data/grades.txt')
        grades.loc[grades['username'] == student_id, list(new_grades.keys())] = list(new_grades.values())
        grades.to_csv('data/grades.txt', index=False)
        
        record_grade_update(student_id, new_grades)
        return True, "Grades modified successfully"
    except Exception as e:
        return False, f"Grade modification failed: {str(e)}"
    
def modify_eca(student_id, activities):
    """Update ECA activities for a student"""
    try:
        eca = pd.read_csv('data/eca.txt')
        
        # Check if student exists
        if student_id not in eca['username'].values:
            return False, "Student not found in ECA records"
            
        # Update activities
        eca.loc[eca['username'] == student_id, ['activity1', 'activity2', 'activity3']] = activities
        eca.to_csv('data/eca.txt', index=False)
        
        # Return success with the updated activities
        updated_activities = ", ".join([a for a in activities if a.lower() != 'none'])
        return True, f"ECA updated successfully!\nActivities: {updated_activities}"
    except Exception as e:
        return False, f"Error updating ECA: {str(e)}"


def delete_user(target_username):
    try:
        # Delete from all files including eca.txt
        for file in ['users.txt', 'passwords.txt', 'grades.txt', 'eca.txt']:
            df = pd.read_csv(f'data/{file}')
            df = df[df['username'] != target_username]
            df.to_csv(f'data/{file}', index=False)
        
        # Delete grade history file
        history_file = f'data/grade_history/{target_username}.csv'
        if os.path.exists(history_file):
            os.remove(history_file)
        
        return True, f"User {target_username} deleted"
    except Exception as e:
        return False, f"Delete failed: {str(e)}"