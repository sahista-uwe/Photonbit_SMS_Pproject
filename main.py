#this is main.py
import tkinter as tk
from tkinter import ttk, messagebox
from auth import authenticate, get_user_role
import pandas as pd
from admin import add_user
from student import update_profile
from utils import plot_subject_averages, embed_plot, initialize_data_files,plot_grade_trends
from models import Admin
from models import Student

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student System Login")
        self.create_widgets()
        self.root.mainloop()
        

    def create_widgets(self):
        ttk.Label(self.root, text="Username:").grid(row=0, column=0)
        self.username = ttk.Entry(self.root)
        self.username.grid(row=0, column=1)

        ttk.Label(self.root, text="Password:").grid(row=1, column=0)
        self.password = ttk.Entry(self.root, show="*")
        self.password.grid(row=1, column=1)

        ttk.Button(self.root, text="Login", command=self.check_login).grid(row=2, column=1)

    def check_login(self):
        username = self.username.get()
        try:
            if authenticate(username, self.password.get()):
                role = get_user_role(username)
                if role not in ['admin', 'student']:
                    raise ValueError("Invalid role detected")
                
                self.root.destroy()
                user = Admin(username, role) if role == 'admin' else Student(username, role)
                DashboardWindow(user)
            else:
                tk.messagebox.showerror("Error", "Invalid credentials")
        except Exception as e:
            tk.messagebox.showerror("System Error", f"Login failed: {str(e)}")


    

class DashboardWindow:
    def __init__(self, user):  
        self.window = tk.Tk()
        self.user = user
        self.username = user.username
        self.window.title(f"{user.role.capitalize()} Dashboard")
        
        if user.role == "admin":
            self.create_admin_dashboard()
        else:
            self.create_student_dashboard()
        
        self.window.mainloop()


    def create_student_dashboard(self):
        # Student profile frame
        profile_frame = ttk.LabelFrame(self.window, text="My Profile")
        profile_frame.pack(pady=10, padx=10, fill='x')
    
        # Get student data
        try:
            users = pd.read_csv('data/users.txt')
            student = users[users['username'] == self.user.username].iloc[0]
        
            ttk.Label(profile_frame, text=f"Name: {student['name']}").pack(anchor='w')
            ttk.Label(profile_frame, text=f"Email: {student['email']}").pack(anchor='w')
            ttk.Label(profile_frame, text=f"Phone: {student['phone']}").pack(anchor='w')
        
        # Update profile button
            ttk.Button(profile_frame, text="Update Profile", 
                      command=self.show_update_profile).pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load profile: {str(e)}")
            return
        # Grades display frame (OUTSIDE the try-except block)
        grades_frame = ttk.LabelFrame(self.window, text="Your Grades")
        grades_frame.pack(pady=10, padx=10, fill='both', expand=True)

    # Show subject grades bar chart
        fig = plot_subject_averages(username=self.user.username)
        if fig:
            embed_plot(grades_frame, fig)

    # Performance button
        ttk.Button(self.window, text="Check Performance", 
                   command=self.show_performance).pack(pady=5)

    # Grade trends plot
        try:
            fig = plot_grade_trends(self.user.username)
            if fig:
                embed_plot(self.window, fig)
        except Exception as e:
            messagebox.showinfo("Info", f"Grade trends unavailable: {str(e)}")

        eca_frame = ttk.LabelFrame(self.window, text="My ECAs")
        eca_frame.pack(pady=10, fill='x')

        try:
            eca = pd.read_csv('data/eca.txt')
            student_eca = eca[eca['username'] == self.user.username].iloc[0]
            ttk.Label(eca_frame, text=f"Activity 1: {student_eca['activity1']}").pack(anchor='w')
            ttk.Label(eca_frame, text=f"Activity 2: {student_eca['activity2']}").pack(anchor='w')
            ttk.Button(eca_frame, text="Update ECAs", 
                  command=self.show_update_eca).pack()
        except:
            messagebox.showinfo("Info", "No ECA records found")




    def show_update_profile(self):
        update_window = tk.Toplevel(self.window)
        update_window.title("Update Profile")
    
        # Get current info
        users = pd.read_csv('data/users.txt')
        student = users[users['username'] == self.user.username].iloc[0]
    
        ttk.Label(update_window, text="Email:").grid(row=0, column=0)
        email_entry = ttk.Entry(update_window)
        email_entry.insert(0, student['email'])
        email_entry.grid(row=0, column=1)
    
        ttk.Label(update_window, text="Phone:").grid(row=1, column=0)
        phone_entry = ttk.Entry(update_window)
        phone_entry.insert(0, student['phone'])
        phone_entry.grid(row=1, column=1)
    
        def submit():
            from student import update_profile
            if update_profile(self.user.username, email_entry.get(), phone_entry.get()):
                update_window.destroy()
                self.window.destroy()  
                DashboardWindow("self.user") 
    
        ttk.Button(update_window, text="Update", command=submit).grid(row=2, columnspan=2)

    def show_performance(self):
        from student import check_performance
        performance = check_performance(self.user.username)
    
        if performance:
            messagebox.showinfo("Performance", 
                            f"Average: {performance['average']}\n"
                            f"Rank: {performance['rank']}/{performance['total_students']}")

# --------------------------------------------------------------------------------------------------------------
    def create_admin_dashboard(self):
        button_frame = ttk.Frame(self.window) 
        button_frame.pack(pady=15, fill='x')

        # Add all admin buttons to the frame
        ttk.Button(button_frame, text="Add User", command=self.show_add_user).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Update Grades", command=self.show_update_grades).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Modify ECA", command=self.show_modify_eca).pack(side='left', padx=5)
        ttk.Button(button_frame, text="ECA Insights", command=self.show_eca_insights).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Delete User", command=self.show_delete_user).pack(side='left', padx=5)


        

        fig = plot_subject_averages()
        embed_plot(self.window, fig)

        

    def show_add_user(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("Add New User")
    
        # Form fields
        ttk.Label(add_window, text="Username:").grid(row=0, column=0)
        username_entry = ttk.Entry(add_window)
        username_entry.grid(row=0, column=1)
    
        ttk.Label(add_window, text="Name:").grid(row=1, column=0)
        name_entry = ttk.Entry(add_window)
        name_entry.grid(row=1, column=1)
    
        ttk.Label(add_window, text="Password:").grid(row=2, column=0)
        password_entry = ttk.Entry(add_window, show="*")
        password_entry.grid(row=2, column=1)
    
        ttk.Label(add_window, text="Role:").grid(row=3, column=0)
        role_combobox = ttk.Combobox(add_window, values=["admin", "student"])
        role_combobox.grid(row=3, column=1)
    
        ttk.Label(add_window, text="Email:").grid(row=4, column=0)
        email_entry = ttk.Entry(add_window)
        email_entry.grid(row=4, column=1)
    
        ttk.Label(add_window, text="Phone:").grid(row=5, column=0)
        phone_entry = ttk.Entry(add_window)
        phone_entry.grid(row=5, column=1)

        def submit():
            from admin import add_user
            username = username_entry.get()
            name = name_entry.get()
            password = password_entry.get()
            role = role_combobox.get()
            email = email_entry.get()
            phone = phone_entry.get()

        # Validate required fields
            if not all([username, name, password, role]):
                messagebox.showerror("Error", "All fields except phone/email are required!")
                return

        # Call add_user with error handling
            success, message = add_user(
                username, name, password, role, email, phone
            )
            
            if success:
                messagebox.showinfo("Success", message)
                add_window.destroy()
            else:
                messagebox.showerror("Error", message)
        ttk.Button(add_window, text="Add User", command=submit ).grid(row=6, columnspan=2)
    
    def show_update_grades(self):
        update_window = tk.Toplevel(self.window)
        update_window.title("Update Student Grades")

    # Student selection dropdown
        ttk.Label(update_window, text="Student:").grid(row=0, column=0)
        users = pd.read_csv('data/users.txt')
        students = users[users['role'] == 'student']['username'].tolist()  # Only students
        student_combobox = ttk.Combobox(update_window, values=students)
        student_combobox.grid(row=0, column=1)

    # Grade entry fields
        subjects = ['math', 'science', 'english', 'history', 'art']
        entries = {}
        for i, subject in enumerate(subjects):
            ttk.Label(update_window, text=f"{subject.capitalize()}:").grid(row=i+1, column=0)
            entries[subject] = ttk.Entry(update_window)
            entries[subject].grid(row=i+1, column=1)

        def submit():
            from admin import modify_grades
            student = student_combobox.get()
            new_grades = {subject: int(entries[subject].get()) for subject in subjects}
            success, msg = modify_grades(student, new_grades)  # Reuse existing function
            if success:
                messagebox.showinfo("Success", msg)
                update_window.destroy()
            else:
                messagebox.showerror("Error", msg)

        ttk.Button(update_window, text="Update", command=submit).grid(row=6, columnspan=2)
    
    def show_modify_eca(self):
        """Display window for admin to modify student ECA activities"""
        modify_window = tk.Toplevel(self.window)
        modify_window.title("Modify Student Extracurricular Activities")
        modify_window.geometry("400x300")
        modify_window.resizable(False, False)
    
        # Style configuration
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10), padding=5)
    
        # Main container frame
        main_frame = ttk.Frame(modify_window, padding="10 10 10 10")
        main_frame.pack(fill=tk.BOTH, expand=True)
    
        # Student selection
        ttk.Label(main_frame, text="Select Student:").grid(row=0, column=0, sticky='w', pady=5)
    
        users = pd.read_csv('data/users.txt')
        students = users[users['role'] == 'student']['username'].tolist()
        student_combobox = ttk.Combobox(
            main_frame, 
            values=students, 
            state='readonly',
            font=('Arial', 10)
        )
        student_combobox.grid(row=0, column=1, sticky='ew', pady=5, padx=5)
    
        # Activity entries
        activities = ['Activity 1', 'Activity 2', 'Activity 3']
        entries = {}
    
        for i, activity in enumerate(activities):
            ttk.Label(main_frame, text=f"{activity}:").grid(
                row=i+1, column=0, sticky='w', pady=5)
        
            entries[activity] = ttk.Combobox(
                main_frame,
                values=["Basketball", "Chess", "Drama", "Music", "Debate", "Robotics", "None"],
                font=('Arial', 10)
            )
            entries[activity].grid(row=i+1, column=1, sticky='ew', pady=5, padx=5)
            entries[activity].set("None")  # Default value
    
    # Load current activities when student is selected
        def load_current_activities(event):
            student = student_combobox.get()
            try:
                eca = pd.read_csv('data/eca.txt')
                student_eca = eca[eca['username'] == student].iloc[0]
                for i, activity in enumerate(activities):
                    entries[activity].set(student_eca[f'activity{i+1}'])
            except Exception as e:
                messagebox.showerror("Error", f"Couldn't load activities: {str(e)}")
    
        student_combobox.bind("<<ComboboxSelected>>", load_current_activities)
    
        # Submit button
        submit_frame = ttk.Frame(main_frame)
        submit_frame.grid(row=4, column=0, columnspan=2, pady=15)
    
        def submit():
            student = student_combobox.get()
            if not student:
                messagebox.showerror("Error", "Please select a student first!")
                return
            
            new_activities = [entries[activity].get() for activity in activities]
        
            # Validate at least one activity is selected
            if all(a.lower() == "none" for a in new_activities):
                messagebox.showwarning("Warning", "Please select at least one activity!")
                return
            
            # Call admin function to modify ECA
            from admin import modify_eca
            success, msg = modify_eca(student, new_activities)
        
            if success:
                # Create success popup
                success_popup = tk.Toplevel(modify_window)
                success_popup.title("Success!")
                success_popup.geometry("300x200")
            
                # Success message
                ttk.Label(
                    success_popup, 
                    text="ECA Activities Updated Successfully!",
                    font=('Arial', 10, 'bold'),
                    foreground='green'
                ).pack(pady=10)
            
                # Display updated activities
                activities_frame = ttk.LabelFrame(success_popup, text="Updated Activities")
                activities_frame.pack(pady=10, padx=10, fill='x')
            
                for i, activity in enumerate(activities):
                    ttk.Label(
                        activities_frame,
                        text=f"{activity}: {new_activities[i]}"
                    ).pack(anchor='w', padx=5, pady=2)
            
                # OK button that closes both windows
                ttk.Button(
                    success_popup,
                    text="OK",
                    command=lambda: [success_popup.destroy(), modify_window.destroy()]
                ).pack(pady=10)
            
                # Play success sound if available
                try:
                    import winsound
                    winsound.MessageBeep(winsound.MB_OK)
                except:
                    pass
            else:
                messagebox.showerror("Error", msg)
    
        ttk.Button(
            submit_frame,
            text="Update Activities",
            command=submit,
            style='TButton'
        ).pack(side=tk.LEFT, padx=5)
    
        ttk.Button(
            submit_frame,
            text="Cancel",
            command=modify_window.destroy,
            style='TButton'
        ).pack(side=tk.LEFT, padx=5)
    
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        for i in range(4):
            main_frame.rowconfigure(i, weight=1)



    def show_delete_user(self):
        delete_window = tk.Toplevel(self.window)
        ttk.Label(delete_window, text="Enter username to delete:").pack()
        username_entry = ttk.Entry(delete_window)
        username_entry.pack()
    
        def confirm_delete():
            from admin import delete_user
            success, message = delete_user(username_entry.get())
            messagebox.showinfo("Info", message)
            delete_window.destroy()
    
        ttk.Button(delete_window, text="Delete", command=confirm_delete).pack()


    def show_eca_insights(self):
        from utils import plot_eca_participation
        fig = plot_eca_participation()
        embed_plot(self.window, fig)
        
    


if __name__ == "__main__":
    from utils import initialize_data_files
    import pandas as pd
    import os

    # 1. Initialize files WITHOUT deleting existing data
    initialize_data_files()  # Only creates files if missing

    # 2. Add default admin ONLY if no users exist
    users_file = "data/users.txt"
    if os.path.exists(users_file):
        try:
            users = pd.read_csv(users_file)
            if users.empty:  # File exists but is empty
                from admin import add_user
                add_user("admin", "Admin", "admin123", "admin", "admin@school.com", "1234567890")
        except:
            # Corrupted file - recreate it
            from admin import add_user
            add_user("admin", "Admin", "admin123", "admin", "admin@school.com", "1234567890")
    else:
        from admin import add_user
        add_user("admin", "Admin", "admin123", "admin", "admin@school.com", "1234567890")

    LoginWindow()