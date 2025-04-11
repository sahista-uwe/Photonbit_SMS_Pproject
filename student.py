import pandas as pd
import tkinter as tk
from tkinter import messagebox
from utils import validate_email, validate_phone, plot_grade_trends


def update_profile(username, new_email, new_phone):
    try:
        if not validate_email(new_email):
            messagebox.showerror("Error", "Invalid email format")
            return False
        
        if not validate_phone(new_phone):
            messagebox.showerror("Error", "Invalid phone number")
            return False
        
        df = pd.read_csv('data/users.txt')
        df.loc[df['id'] == username, 'email'] = new_email
        df.loc[df['id'] == username, 'phone'] = new_phone
        df.to_csv('data/users.txt', index=False)
        messagebox.showinfo("Success", "Profile updated successfully")
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update profile: {str(e)}")
        return False

def check_performance(username):
    try:
        grades_df = pd.read_csv('data/grades.txt')
        student_grades = grades_df[grades_df['id'] == username]
        
        if student_grades.empty:
            messagebox.showinfo("Info", "No grade records found")
            return None
        
        subjects = [col for col in student_grades.columns if col != 'id']
        average = student_grades[subjects].mean(axis=1).values[0]
        
        averages = grades_df[subjects].mean(axis=1)
        rank = (averages > average).sum() + 1
        
        return {
            'average': round(average, 2),
            'rank': rank,
            'total_students': len(grades_df)
        }
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check performance: {str(e)}")
        return None

