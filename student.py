import pandas as pd
from tkinter import messagebox

def update_profile(username, new_email, new_phone):
    """Update student details using pandas"""
    try:
        users = pd.read_csv('data/users.txt')
        users.loc[users['id'] == username, ['email', 'phone']] = [new_email, new_phone]
        users.to_csv('data/users.txt', index=False)
        return True
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return False


def check_performance(username):
    grades = pd.read_csv('data/grades.txt')
    student_grades = grades[grades['id'] == username].iloc[0, 1:]
    if student_grades.mean() < 60:
        return "Needs academic support"
    return "Performance satisfactory"