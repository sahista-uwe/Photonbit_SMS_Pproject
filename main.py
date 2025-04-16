#This is main.py
from PIL import Image
import pandas as pd
import os
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from auth import authenticate, get_user_role
from admin import add_user
from student import update_profile
from utils import plot_subject_averages, embed_plot, initialize_data_files
from models import Admin, Student

# Setting the appearance to dark
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("dark-blue")  

class LoginWindow:
    def __init__(self):
        self.root = ctk.CTk() #customtkinter
        self.root.title("Student System Login")
        self.center_window(400, 300) #width, height
        self.create_widgets()
        self.root.mainloop()
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Title label
        ctk.CTkLabel(
            self.main_frame, 
            text="Student System Login",
            font=("Helvetica", 16, "bold")
        ).pack(pady=20)
        
        # Username entry
        self.username_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.username_frame.pack(pady=10)
        
        ctk.CTkLabel(
            self.username_frame,
            text="Username:",
            font=("Helvetica", 12)
        ).pack(side="left", padx=(0, 10))
        
        self.username_entry = ctk.CTkEntry(
            self.username_frame,
            width=200,
            font=("Helvetica", 12)
        )
        self.username_entry.pack(side="left")
        
        # Password entry
        self.password_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.password_frame.pack(pady=10)
        
        ctk.CTkLabel(
            self.password_frame,
            text="Password:",
            font=("Helvetica", 12)
        ).pack(side="left", padx=(0, 10))
        
        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            width=200,
            show="*",
            font=("Helvetica", 12)
        )
        self.password_entry.pack(side="left")
        
        # Login button
        self.login_button = ctk.CTkButton(
            self.main_frame,
            text="Login",
            command=self.check_login,
            font=("Helvetica", 12)
        )
        self.login_button.pack(pady=20)

    def check_login(self):
        username = self.username_entry.get()
        
        if authenticate(username, self.password_entry.get()):
            role = get_user_role(username)
            if role not in ['admin', 'student']:
                
                CTkMessagebox(title="error", message="Invalid role detected", icon= 'cancel')
                return
                
            self.root.destroy()
            user = Admin(username, role) if role == 'admin' else Student(username, role)
            DashboardWindow(user)
        else:
           
            CTkMessagebox(title="error", message="Invalid credentials", icon= 'cancel')

class DashboardWindow:
    def __init__(self, user):  
        self.window = ctk.CTk()
        self.user = user
        self.username = user.username
        self.window.title(f"{user.role.capitalize()} Dashboard")
        self.center_window(1000, 800)
        
        if user.role == "admin":
            self.create_admin_dashboard()
        else:
            self.create_student_dashboard()
        
        self.window.mainloop()
    
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def create_student_dashboard(self):
        # Main container frame
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Student profile frame
        profile_frame = ctk.CTkFrame(self.main_frame)
        profile_frame.pack(pady=10, padx=10, fill="x")
        
        ctk.CTkLabel(
            profile_frame,
            text="My Profile",
            font=("Helvetica", 14, "bold")
        ).pack(pady=1)
        
        # Get student data
        try:
            users = pd.read_csv('data/users.txt')
            student = users[users['username'] == self.user.username].iloc[0]
            
            info_frame = ctk.CTkFrame(profile_frame, fg_color="transparent")
            info_frame.pack(pady=1)
            
            ctk.CTkLabel(
                info_frame,
                text=f"Name: {student['name']}",
                font=("Helvetica", 12)
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=f"Email: {student['email']}",
                font=("Helvetica", 12)
            ).pack(anchor="w")
            
            ctk.CTkLabel(
                info_frame,
                text=f"Phone: {student['phone']}",
                font=("Helvetica", 12)
            ).pack(anchor="w")
            
            # Update profile button
            ctk.CTkButton(
                profile_frame,
                text="Update Profile",
                command=self.show_update_profile,
                font=("Helvetica", 12)
            ).pack(pady=1)
            
        except Exception as e:
           
            CTkMessagebox(title="Error", message=f" Failed to load profile: {str(e)}", icon="cancel")
            return
        
        # Grades display frame
        grades_frame = ctk.CTkFrame(self.main_frame)
        grades_frame.pack(pady=10, padx=10, fill="both", expand= True )
        
        ctk.CTkLabel(
            grades_frame,
            text="Your Grades",
            font=("Helvetica", 14, "bold")
        ).pack(pady=5)
        
        # Show subject grades bar chart
        fig = plot_subject_averages(username=self.user.username)
        if fig:
            embed_plot(grades_frame, fig)
        
        # Performance button
        ctk.CTkButton(
            self.main_frame,
            text="Check Performance",
            command=self.show_performance,
            font=("Helvetica", 12)
        ).pack(pady=5)
        
        # ECA section
        eca_frame = ctk.CTkFrame(self.main_frame)
        eca_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(
            eca_frame,
            text="My ECAs",
            font=("Helvetica", 14, "bold")
        ).pack(pady=5)
        
        try:
            if os.path.exists('data/eca.txt'):
                eca = pd.read_csv('data/eca.txt')
                student_eca = eca[eca['username'] == self.user.username].iloc[0]
                if not student_eca.empty:
                    eca_info_frame = ctk.CTkFrame(eca_frame, fg_color="transparent")
                    eca_info_frame.pack(pady=5)
                    
                    ctk.CTkLabel(
                        eca_info_frame,
                        text=f"Activity 1: {student_eca['activity1']}",
                        font=("Helvetica", 12)
                    ).pack(anchor="w")
                    
                    ctk.CTkLabel(
                        eca_info_frame,
                        text=f"Activity 2: {student_eca['activity2']}",
                        font=("Helvetica", 12)
                    ).pack(anchor="w")
                    
                    ctk.CTkLabel(
                        eca_info_frame,
                        text=f"Activity 3: {student_eca['activity3']}",
                        font=("Helvetica", 12)
                    ).pack(anchor="w")
                    
                    ctk.CTkButton(
                        eca_frame,
                        text="Update ECAs",
                        command=self.show_update_eca,
                        font=("Helvetica", 12)
                    ).pack(pady=5)
                else:
                    ctk.CTkLabel(
                        eca_frame,
                        text="No ECA records found",
                        font=("Helvetica", 12)
                    ).pack()
            else:
                ctk.CTkLabel(
                    eca_frame,
                    text="ECA database not available",
                    font=("Helvetica", 12)
                ).pack()
        except Exception as e:
            ctk.CTkLabel(
                eca_frame,
                text="Enrolled ECA",
                font=("Helvetica", 12)
            ).pack()

    def show_update_profile(self):
        update_window = ctk.CTkToplevel(self.window)
        update_window.title("Update Profile")
        update_window.geometry("400x300")
        
        # Get current info
        users = pd.read_csv('data/users.txt')
        student = users[users['username'] == self.user.username].iloc[0]
        
        # Email entry
        ctk.CTkLabel(
            update_window,
            text="Email:",
            font=("Helvetica", 12)
        ).pack(pady=5)
        
        email_entry = ctk.CTkEntry(
            update_window,
            width=250,
            font=("Helvetica", 12)
        )
        email_entry.insert(0, student['email'])
        email_entry.pack(pady=5)
        
        # Phone entry
        ctk.CTkLabel(
            update_window,
            text="Phone:",
            font=("Helvetica", 12)
        ).pack(pady=5)
        
        phone_entry = ctk.CTkEntry(
            update_window,
            width=250,
            font=("Helvetica", 12)
        )
        phone_entry.insert(0, student['phone'])
        phone_entry.pack(pady=5)
        
        def submit():
            if update_profile(self.user.username, email_entry.get(), phone_entry.get()):
                update_window.destroy()
                self.window.destroy()  
                DashboardWindow(self.user) 
        
        # Submit button
        ctk.CTkButton(
            update_window,
            text="Update",
            command=submit,
            font=("Helvetica", 12)
        ).pack(pady=10)

    def show_performance(self):
        from student import check_performance
        performance = check_performance(self.user.username)
        
        if performance:
            
            CTkMessagebox(
            title="Performance",
            message=f"Average: {performance['average']}\n"
                   f"Rank: {performance['rank']}/{performance['total_students']}",
                   icon="info",
            bg_color="#2b2b2b",  # Dark background
            fg_color="#2b2b2b",  # Dark frame
            text_color="white",  # White text
            button_color="#3b3b3b",  # Dark buttons
            button_hover_color="#4b4b4b",  # Button hover
            corner_radius=10  # Rounded corners
        )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def create_admin_dashboard(self):
        # Main container frame
        self.main_frame = ctk.CTkFrame(self.window,fg_color="#2b2b2b")
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        

        
        profile_frame = ctk.CTkFrame(self.main_frame)
        profile_frame.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(
            profile_frame,
            text="Admin Profile",
            font=("Helvetica", 14, "bold")
        ).pack(pady=5)


       
        #widgests
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=15, fill="x")
        # Add all admin buttons to the frame
        button_options = {
            "Add User": self.show_add_user,
            "Update Grades": self.show_update_grades,
            "Modify ECA": self.show_modify_eca,
            "ECA Insights": self.show_eca_insights,
            "Delete User": self.show_delete_user
        }
        
        for text, command in button_options.items():
            ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                font=("Helvetica", 12)
            ).pack(side="left", padx=5, expand=True)
        
        # Show subject averages plot
        fig = plot_subject_averages()
        if fig:
            embed_plot(self.main_frame, fig)

    def show_eca_insights(self):
        from utils import plot_eca_participation

     # Create a new window for ECA insights
        insights_window = ctk.CTkToplevel(self.window)
        insights_window.title("ECA Participation Insights")
        insights_window.geometry("800x600")

        fig = plot_eca_participation()
        if fig:
            embed_plot(insights_window, fig)
        else:
            CTkMessagebox(title="Error", message="Could not generate ECA insights", icon="cancel")







    def show_add_user(self):
        add_window = ctk.CTkToplevel(self.window)
        add_window.title("Add New User")
        add_window.geometry("400x600")

    
        
        # Form fields
        fields = [
            ("Username:", ctk.CTkEntry(add_window, width=250)),
            ("Name:", ctk.CTkEntry(add_window, width=250)),
            ("Password:", ctk.CTkEntry(add_window, show="*", width=250)),
            ("Role:", ctk.CTkComboBox(add_window, values=["admin", "student"], width=250)),
            ("Email:", ctk.CTkEntry(add_window, width=250)),
            ("Phone:", ctk.CTkEntry(add_window, width=250))
        ]
        
        entries = []
        for i, (label_text, entry_widget) in enumerate(fields):
            ctk.CTkLabel(
                add_window,
                text=label_text,
                font=("Helvetica", 12)
            ).pack(pady=(10 if i == 0 else 5))
            
            entry_widget.pack(pady=5)
            entries.append(entry_widget)
        
        def submit():
            from admin import add_user
            username = entries[0].get()
            name = entries[1].get()
            password = entries[2].get()
            role = entries[3].get()
            email = entries[4].get()
            phone = entries[5].get()

            # Validate required fields
            if not all([username, name, password, role]):
                CTkMessagebox(title="Error", message="All fields except phone/email are required!")
                return

            # Call add_user with error handling
            success, message = add_user(
                username, name, password, role, email, phone
            )
            
            if success:
                CTkMessagebox(title="Success",message=message,icon="check")
                
                add_window.destroy()
            else:
                
                CTkMessagebox(title="Error",message=message,icon="cancel")

        
        ctk.CTkButton(
            add_window,
            text="Add User",
            command=submit,
            font=("Helvetica", 12)
        ).pack(pady=15)
    
    def show_update_grades(self):
        update_window = ctk.CTkToplevel(self.window)
        update_window.title("Update Student Grades")
        update_window.geometry("400x600")
        
        # Student selection dropdown
        ctk.CTkLabel(
            update_window,
            text="Student:",
            font=("Helvetica", 12)
        ).pack(pady=5)
        
        users = pd.read_csv('data/users.txt')
        students = users[users['role'] == 'student']['username'].tolist()
        student_combobox = ctk.CTkComboBox(
            update_window,
            values=students,
            font=("Helvetica", 12),
            width=250
        )
        student_combobox.pack(pady=5)
        
        # Grade entry fields
        subjects = ['math', 'science', 'english', 'history', 'art']
        entries = {}
        
        for subject in subjects:
            ctk.CTkLabel(
                update_window,
                text=f"{subject.capitalize()}:",
                font=("Helvetica", 12)
            ).pack(pady=2)
            
            entries[subject] = ctk.CTkEntry(
                update_window,
                width=250,
                font=("Helvetica", 12)
            )
            entries[subject].pack(pady=2)

        def submit():
            from admin import modify_grades
            student = student_combobox.get()
            new_grades = {subject: int(entries[subject].get()) for subject in subjects}
            success, msg = modify_grades(student, new_grades)
            if success:
                CTkMessagebox(title="Success",message="success",icon="check")
                update_window.destroy()
            else:
                CTkMessagebox(title="Error",message="error",icon="cancel")

        ctk.CTkButton(
            update_window,
            text="Update",
            command=submit,
            font=("Helvetica", 12)
        ).pack(pady=15)
    
    def show_modify_eca(self):
        modify_window = ctk.CTkToplevel(self.window)
        modify_window.title("Modify Student Extracurricular Activities")
        modify_window.geometry("400x400")
        
        # Main container frame
        main_frame = ctk.CTkFrame(modify_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Student selection
        ctk.CTkLabel(
            main_frame,
            text="Select Student:",
            font=("Helvetica", 12)
        ).pack(pady=5)
        
        users = pd.read_csv('data/users.txt')
        students = users[users['role'] == 'student']['username'].tolist()
        student_combobox = ctk.CTkComboBox(
            main_frame,
            values=students,
            font=("Helvetica", 12),
            width=250
        )
        student_combobox.pack(pady=5)
        
        # Activity entries
        activities = ['Activity 1', 'Activity 2', 'Activity 3']
        entries = {}
        activity_options = ["Basketball", "Chess", "Drama", "Music", "Debate", "Robotics", "None"]
        
        for activity in activities:
            ctk.CTkLabel(
                main_frame,
                text=f"{activity}:",
                font=("Helvetica", 12)
            ).pack(pady=2)
            
            entries[activity] = ctk.CTkComboBox(
                main_frame,
                values=activity_options,
                font=("Helvetica", 12),
                width=250
            )
            entries[activity].set("None")
            entries[activity].pack(pady=2)
        
        # Load current activities when student is selected
        def load_current_activities(event):
            student = student_combobox.get()
            try:
                eca = pd.read_csv('data/eca.txt')
                student_eca = eca[eca['username'] == student].iloc[0]
                for i, activity in enumerate(activities):
                    entries[activity].set(student_eca[f'activity{i+1}'])
            except Exception as e:
                
                CTkMessagebox(title="Error",message=f"Couldn't load activities: {str(e)}",icon="cancel")

        
        student_combobox.bind("<<ComboboxSelected>>", load_current_activities)
        
        # Submit button
        def submit():
            student = student_combobox.get()
            if not student:
                CTkMessagebox(title="Error",message="Please select a student first!",icon="cancel")


                return
            
            new_activities = [entries[activity].get() for activity in activities]
            
            # Validate at least one activity is selected
            if all(a.lower() == "none" for a in new_activities):
                CTkMessagebox( title="Warning",message="Please select at least one activity!", icon="warning", ) # Uses a warning icon

                return
            
            # Call admin function to modify ECA
            from admin import modify_eca
            success, msg = modify_eca(student, new_activities)
            
            if success:
            
                CTkMessagebox(title="Success",message="ECA Activities Updated Successfully!",icon="check")

                modify_window.destroy()
            else:
                
                CTkMessagebox(title="Error",message="Error",icon="cancel")

        
        ctk.CTkButton(
            main_frame,
            text="Update Activities",
            command=submit,
            font=("Helvetica", 12)
        ).pack(pady=15)

    def show_delete_user(self):
        delete_window = ctk.CTkToplevel(self.window)
        delete_window.title("Delete User")
        delete_window.geometry("300x200")
        
        ctk.CTkLabel(
            delete_window,
            text="Enter username to delete:",
            font=("Helvetica", 12)
        ).pack(pady=15)
        
        username_entry = ctk.CTkEntry(
            delete_window,
            width=200,
            font=("Helvetica", 12)
        )
        username_entry.pack(pady=5)
        
        def confirm_delete():
            from admin import delete_user
            success, message = delete_user(username_entry.get())
            CTkMessagebox(title="Info",message=message,icon="info")

            delete_window.destroy()
        
        ctk.CTkButton(
            delete_window,
            text="Delete",
            command=confirm_delete,
            font=("Helvetica", 12)
        ).pack(pady=15)



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