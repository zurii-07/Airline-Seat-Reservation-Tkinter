import csv
import os

#Initializing the path to a csv for saving user details.
DATA_PATH = os.path.join(os.path.dirname(__file__),'..', 'data', 'users.csv')

#Checks whether a user exists
def ensure_user_csv_exists():
    if not os.path.isfile(DATA_PATH):
        with open(DATA_PATH, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['username', 'password', 'fullname', 'email'])

#Saving new user details to the csv file
def register_user(username, password, fullname, email):
    ensure_user_csv_exists()
    if user_exists(username):
        return False, "Username already exists! Pick a different username"
    with open(DATA_PATH, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, password, fullname, email])
    return True, "Registration Successful"

#Determines if the csv file is present and scans users
def user_exists(username):
    ensure_user_csv_exists()
    with open(DATA_PATH, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                return True
    return False

#Authenticate user login
def authenticate_user(username, password):
    ensure_user_csv_exists()
    with open(DATA_PATH, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username and row['password'] == password:
             return True
    return False