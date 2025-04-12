#this is utils.py
import pandas as pd
import matplotlib.pyplot as plt
import os
from tkinter import messagebox
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def initialize_data_files():
    """Create data files with headers if they don't exist."""
    data_files = {
        'data/users.txt': ['username', 'name', 'role', 'email', 'phone'],
        'data/passwords.txt': ['username', 'password'],
        'data/grades.txt': ['username', 'math', 'science', 'english', 'history', 'art'],
        'data/eca.txt': ['username', 'activity1', 'activity2', 'activity3']
    }
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/grade_history', exist_ok=True)

    for file_path, columns in data_files.items():
        if not os.path.exists(file_path):
            pd.DataFrame(columns=columns).to_csv(file_path, index=False)
    
     # Sync ECA records with users.txt (run this after adding a user)
    users = pd.read_csv('data/users.txt')
    eca = pd.read_csv('data/eca.txt')
    
    # Find missing users in ECA and add blank entries
    missing_users = users[~users['username'].isin(eca['username'])]
    if not missing_users.empty:
        new_entries = pd.DataFrame({
            'username' : missing_users['username'],
            'activity1':'None',
            'activity2':'None',
            'activity3':'None',
        })
        eca = pd.concat([eca, new_entries], ignore_index=True)
        eca.to_csv('data/eca.txt', index=False)
     

def record_grade_update(username, grades):
    """Record grade changes in history file"""
    history_file = f'data/grade_history/{username}.csv'
    today = datetime.now().strftime('%Y-%m-%d')
    
    new_record = {'date': today}
    new_record.update(grades)
    
    # Create file if it doesn't exist
    if not os.path.exists(history_file):
        pd.DataFrame(columns=new_record.keys()).to_csv(history_file, index=False)
    
    # Append new record
    history_df = pd.read_csv(history_file)
    history_df = pd.concat([history_df, pd.DataFrame([new_record])])
    history_df.to_csv(history_file, index=False)

def plot_grade_trends(username, window=None):
    """Plots grade trends for ONE student (given by username)"""
    history_file = f'data/grade_history/{username}.csv'  # Only this student's file
    
    try:
        # Check if file exists
        if not os.path.exists(history_file):
            raise FileNotFoundError(f"No grade history found for {username}")
        
        # Read ONLY this student's data
        df = pd.read_csv(history_file)
        
        # Check if data is available
        if len(df) < 1:
            raise ValueError(f"No records found for {username}")
        
        # Convert date and sort
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values('date', inplace=True)
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(6, 2.5))
        plt.title(f"Grade Trends for {username}")
        
        # Subjects to plot
        subjects = ['math', 'science', 'english', 'history', 'art']
        
        # Plot each subject as a line (or bars if preferred)
        for subject in subjects:
            ax.plot(df['date'], df[subject], marker='o', label=subject)
        
        # Customize plot
        ax.set_xlabel("Date")
        ax.set_ylabel("Score")
        ax.legend()
        ax.grid(True)
        
        plt.tight_layout()
        
        # Display in Tkinter if needed
        if window:
            canvas = FigureCanvasTkAgg(fig, master=window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)
            return canvas
        return fig
        
    except Exception as e:
        print(f"Error plotting trends for {username}: {str(e)}")
        if window:
            messagebox.showinfo("Info", f"No grade data available for {username}")
        return None

def plot_subject_averages(username=None):
    """Show subject grades for one student or class averages"""
    try:
        grades = pd.read_csv('data/grades.txt')
        
        if username:  # Student view
            student_data = grades[grades['username'] == username]
            if student_data.empty:
                raise ValueError(f"No grades found for {username}")
            
            # Extract just the grades (exclude 'username' column)
            grades_data = student_data.iloc[0][['math','science','english','history','art']]
            
            fig, ax = plt.subplots(figsize=(6,2.5))
            grades_data.plot.bar(ax=ax, color=['#4CAF50','#2196F3','#FFC107','#9C27B0','#F44336'])
            ax.set_title(f"Your Current Grades")
            ax.set_ylim(0, 100)
            
        else:  # Admin view (class averages)
            avg = grades.mean(numeric_only=True)
            fig, ax = plt.subplots(figsize=(6,2.5))
            avg.plot.bar(ax=ax, color='skyblue')
            ax.set_title("Class Averages")
            ax.set_ylim(0, 100)
        
        ax.set_ylabel("Score")
        ax.grid(True, axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        return fig
        
    except Exception as e:
        messagebox.showerror("Error", f"Could not load grades: {str(e)}")
        return None

def embed_plot(window, fig):
    """Embed a Matplotlib figure into a Tkinter window."""
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)

def plot_eca_participation():
    """Show ECA participation statistics"""
    eca_df = pd.read_csv('data/eca.txt')
    fig, ax = plt.subplots()
    eca_counts = eca_df['activity1'].value_counts()
    eca_counts.plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_title("ECA Activity Distribution")
    return fig

def check_performance(username):
    """Identify underperforming students"""
    grades = pd.read_csv(f'data/grade_history/{username}.csv')
    latest = grades.iloc[-1]
    
    alerts = []
    if latest['average'] < 60:
        alerts.append("Overall performance below 60%")
    
    for subj in ['math', 'science', 'english']:
        if latest[subj] < 50:
            alerts.append(f"{subj.capitalize()} below 50%")
    
    return alerts

def update_eca(username, activities):
    """Update extracurricular activities"""
    eca = pd.read_csv('data/eca.txt')
    eca.loc[eca['username'] == username, ['activity1','activity2','activity3']] = activities
    eca.to_csv('data/eca.txt', index=False)

def validate_grade(grade: int) -> bool:
    return 0 <= grade <= 100

import re

def validate_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    return re.match(r'^\+?[1-9]\d{1,14}$', phone) is not None  # Supports international numbers

