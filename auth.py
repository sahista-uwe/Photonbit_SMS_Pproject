import pandas as pd

def authenticate(username, password):
    """Validate credentials using pandas"""
    try:
        passwords = pd.read_csv('data/passwords.txt')
        user = passwords[(passwords['username'] == username) & 
                        (passwords['password'] == password)]
        return not user.empty
    except FileNotFoundError:
        return False

def get_user_role(username):
    """Get role using pandas"""
    users = pd.read_csv('data/users.txt')
    user = users[users['id'] == username]
    return user['role'].values[0] if not user.empty else None