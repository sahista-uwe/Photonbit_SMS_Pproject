import tkinter as tk
from tkinter import ttk
from auth import authenticate, get_user_role
from admin import add_user
from student import update_profile
from utils import plot_subject_averages, embed_plot

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
        if authenticate(self.username.get(), self.password.get()):
            role = get_user_role(self.username.get())
            self.root.destroy()
            DashboardWindow(role)
        else:
            tk.messagebox.showerror("Error", "Invalid credentials")

class DashboardWindow:
    def __init__(self, role):
        self.window = tk.Tk()
        self.window.title(f"{role.capitalize()} Dashboard")
        
        if role == "admin":
            self.create_admin_dashboard()
        else:
            self.create_student_dashboard()
        
        self.window.mainloop()

    def create_admin_dashboard(self):
        ttk.Button(self.window, text="Add User", command=self.show_add_user).pack()
        fig = plot_subject_averages()
        embed_plot(self.window, fig)

    def show_add_user(self):
        # Add user form implementation
        pass

    def create_student_dashboard(self):
        ttk.Label(self.window, text="Student Dashboard").pack()
        # Add student features

if __name__ == "__main__":
    LoginWindow()