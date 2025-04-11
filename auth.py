import pandas as pd
from tkinter import messagebox

def authenticate(username, password):
    """Verify credentials with error handling"""
    try:
        passwords = pd.read_csv('data/passwords.txt')
        user = passwords[(passwords['username'] == username) & 
                        (passwords['password'] == password)]
        return not user.empty
    except Exception as e:
        messagebox.showerror("System Error", f"Authentication failed: {str(e)}")
        return False

def get_user_role(username):
    try:
        users = pd.read_csv('data/users.txt')
        user = users[users['id'] == username]
        return user['role'].values[0] if not user.empty else None
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None