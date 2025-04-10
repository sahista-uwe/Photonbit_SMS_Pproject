import pandas as pd
import tkinter as tk
from tkinter import messagebox
from utils import plot_grade_trends

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

def show_grade_trends(username, parent_window):
    """Display trends in a new window"""
    trend_window = tk.Toplevel(parent_window)
    trend_window.title(f"Grade Trends - {username}")
    plot_grade_trends(username, trend_window)