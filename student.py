#this is student.py
import pandas as pd
import tkinter as tk
from CTkMessagebox import CTkMessagebox
from utils import validate_email, validate_phone


def update_profile(username, new_email, new_phone):
    try:
        if not validate_email(new_email):
           
            CTkMessagebox(title="Error", message="Invalid email format", icon="cancel")
            return False
        
        if not validate_phone(new_phone):
            
            CTkMessagebox(title="Error", message="Invalid phone number", icon="cancel")
            return False
        
        df = pd.read_csv('data/users.txt')
        df.loc[df['username'] == username, 'email'] = new_email
        df.loc[df['username'] == username, 'phone'] = new_phone
        df.to_csv('data/users.txt', index=False)
       
        CTkMessagebox(title="Success", message="Profile updated successfully")
        return True
    except Exception as e:
        
        CTkMessagebox(title="Error", message=f"Failed to update profile: {str(e)}", icon="cancel")
        return False

def check_performance(username):
    try:
        grades_df = pd.read_csv('data/grades.txt')
        student_grades = grades_df[grades_df['username'] == username]
        
        if student_grades.empty:
            
            CTkMessagebox(title="Info", message="No grade records found", icon="cancel")
            return None
        
        subjects = [col for col in student_grades.columns if col != 'username']
        average = student_grades[subjects].mean(axis=1).values[0]
        
        averages = grades_df[subjects].mean(axis=1)
        rank = (averages > average).sum() + 1
        
        return {
            'average': round(average, 2),
            'rank': rank,
            'total_students': len(grades_df)
        }
    except Exception as e:
       
        CTkMessagebox(title="Error", message=f"Failed to check performance: {str(e)}", icon="cancel")
        return None

