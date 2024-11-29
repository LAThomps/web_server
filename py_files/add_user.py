"""
CLI tool for adding users to database
"""
import os 
import sys
from dotenv import load_dotenv
from data import db
from pwinput import pwinput
import hashlib
import pandas as pd

# change this to whatever you call the database the `users` table is stored
DATABASE_NAME = "mini_social"

def main():
    load_dotenv()
    conn = db(
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PW"),
        database=DATABASE_NAME
    )
    # have user enter in all values, confirm insert op
    print("input user values")
    while True:
        current_users = set(conn.qry("SELECT UserName FROM users;")['UserName'])
        while True:
            print("\nadding a new user\n")
            while True:
                user_name = input("Enter User Name:\t")
                if user_name in current_users:
                    print(f"UserName `{user_name}` is unavailable, try again\n")
                elif user_name == 'exit':
                    sys.exit()
                else:
                    break
            while True:
                password_1 = pwinput("Enter Password:\t\t")
                password_2 = pwinput("Re-Enter Password:\t")
                if password_1 != password_2:
                    print("passwords do not match, try again\n")
                else:
                    break 
            first_name = input("Enter first name:\t")
            last_name = input("Enter last_name:\t")
            email = input("Enter email:\t\t")
            print(f"""
New user to be added:
UserName:\t{user_name}
Password:\t******* (always hidden)
FirstName:\t{first_name}
LastName:\t{last_name}
Email:\t\t{email} 
            """)
            go = input("Continue (Y/N):\t")
            if go.upper() == "Y":
                break 
            else:
                print("not adding user, restarting user entry\n")
        
        # actually add the user to the db
        salt = os.getenv("MINI_SOCIAL_SALT")
        pass_hash = hashlib.sha256(bytes(salt + password_2, 'utf-8')).hexdigest()
        conn.qry(f"""
INSERT INTO mini_social.users (UserName, FirstName, LastName, Password, Email, SignUpDate)
VALUE ('{user_name}', '{first_name}', '{last_name}', '{pass_hash}', '{email}', now());
        """)
        print(f"user {user_name} added_ to the database")
        add_another = input("Enter 'add' to add another user or any key to exit:\t")
        if add_another != 'add':
            break 
    return 

if __name__ == "__main__":
    main()