#This is models.py
import pandas as pd
import os

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role
        
    def get_profile(self):
        users = pd.read_csv('data/users.txt')
        return users[users['username'] == self.username].iloc[0].to_dict()

class Admin(User):
   def delete_user(self, target_username):
        try:
            # Delete from users.txt
            users=pd.read_csv('data/users.txt')
            users = users[users['username'] != target_username]
            users.to_csv('data/users.txt', index=False)

            # Delete from passwords.txt
            passwords = pd.read_csv('data/passwords.txt')
            passwords = passwords[passwords['username'] != target_username]
            passwords.to_csv('data/passwords.txt', index=False)
            
            # Delete from grades.txt
            grades = pd.read_csv('data/grades.txt')
            grades = grades[grades['username'] != target_username]
            grades.to_csv('data/grades.txt', index=False)
            
            # Delete from eca.txt
            eca = pd.read_csv('data/eca.txt')
            print(f"ECA records BEFORE deletion for {target_username}:")
            print(eca[eca['username'] == target_username])  # Should show the user's row

            eca = eca[eca['username'] != target_username]  # Keep rows where username != target
            eca.to_csv('data/eca.txt', index=False)

        # DEBUG: Print ECA records after deletion
            eca_after = pd.read_csv('data/eca.txt')
            print(f"ECA records AFTER deletion for {target_username}:")
            print(eca_after[eca_after['username'] == target_username])  # Should be empty
            
            # Delete grade history file
            history_file = f'data/grade_history/{target_username}.csv'
            if os.path.exists(history_file):
                os.remove(history_file)
            
            return True, f"User {target_username} and all related data deleted."

            
        except Exception as e:
            return False, f"Failed to delete user: {str(e)}"

class Student(User):
    def get_grades(self):
        grades = pd.read_csv('data/grades.txt')
        return grades[grades['username'] == self.username].iloc[0].to_dict()