import tkinter as tk
from tkinter import ttk, messagebox
from auth import authenticate, get_user_role
import pandas as pd
from admin import add_user
from student import update_profile
from utils import plot_subject_averages, embed_plot, initialize_data_files,plot_grade_trends

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
        if authenticate(username, self.password.get()):
            role = get_user_role(username)
            self.root.destroy()
            DashboardWindow(role, username)  # Pass username here
        else:
            tk.messagebox.showerror("Error", "Invalid credentials")

    

class DashboardWindow:
    def __init__(self, role, username):
        self.window = tk.Tk()
        self.window.title(f"{role.capitalize()} Dashboard")
        self.role = role
        self.username = username  # You'll need to pass this from the login
    
        if role == "admin":
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
            student = users[users['id'] == self.username].iloc[0]
        
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
        fig = plot_subject_averages(username=self.username)
        if fig:
            embed_plot(grades_frame, fig)

    # Performance button
        ttk.Button(self.window, text="Check Performance", 
                   command=self.show_performance).pack(pady=5)

    # Grade trends plot
        try:
            fig = plot_grade_trends(self.username)
            if fig:
                embed_plot(self.window, fig)
        except Exception as e:
            messagebox.showinfo("Info", f"Grade trends unavailable: {str(e)}")



    def show_update_profile(self):
        update_window = tk.Toplevel(self.window)
        update_window.title("Update Profile")
    
        # Get current info
        users = pd.read_csv('data/users.txt')
        student = users[users['id'] == self.username].iloc[0]
    
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
            if update_profile(self.username, email_entry.get(), phone_entry.get()):
                update_window.destroy()
                self.window.destroy()  # Refresh dashboard
                DashboardWindow("student")  # Reopen with updated info
    
        ttk.Button(update_window, text="Update", command=submit).grid(row=2, columnspan=2)

    def show_performance(self):
        from student import check_performance
        performance = check_performance(self.username)
    
        if performance:
            messagebox.showinfo("Performance", 
                            f"Average: {performance['average']}\n"
                            f"Rank: {performance['rank']}/{performance['total_students']}")


    def create_admin_dashboard(self):

        ttk.Button(self.window, text="Add User", command=self.show_add_user).pack()
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
            if add_user(
                username_entry.get(),
                name_entry.get(),
                password_entry.get(),
                role_combobox.get(),
                email_entry.get(),
                phone_entry.get()
            ):
                add_window.destroy()
    
        ttk.Button(add_window, text="Add User", command=submit).grid(row=6, columnspan=2)


if __name__ == "__main__":
    initialize_data_files()
    LoginWindow()