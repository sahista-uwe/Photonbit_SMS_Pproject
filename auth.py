#this is auth.py
import pandas as pd
import hashlib

from CTkMessagebox import CTkMessagebox



def hash_password(password: str) -> str:
    """Create secure password hash"""
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate(username, password):
    """Verify credentials with hashed passwords"""
    try:
        passwords = pd.read_csv('data/passwords.txt')
        user = passwords[passwords['username'] == username]
        
        if user.empty:
            return False
            
        stored_hash = user.iloc[0]['password']
        input_hash = hash_password(password)
        return stored_hash == input_hash
        
    except Exception as e:
        CTkMessagebox(title="Error", message="Invalid credentials!", icon="cancel")
        return False

    
def get_user_role(username):
    try:
        users = pd.read_csv('data/users.txt')
        user = users[users['username'] == username]
        return user['role'].values[0] if not user.empty else None
    except Exception as e:
        CTkMessagebox(title="Error", message="Invalid credentials!", icon="cancel")
        return None