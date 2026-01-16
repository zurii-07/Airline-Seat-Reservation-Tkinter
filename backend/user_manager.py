import csv
import os
# This module manages user data: registration, login, and checking
# User information is stored in a CSV file: users.csv

#Path to the csv for saving user details.
DATA_PATH = os.path.join(os.path.dirname(__file__),'..', 'data', 'users.csv')

#Creates the CSV file with headers if it doesn't exist
def ensure_user_csv_exists():
    if not os.path.isfile(DATA_PATH):
        with open(DATA_PATH, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            #write header row for user fields
            writer.writerow(['username', 'password', 'fullname', 'email'])

#Registers a new user into the CSV file if username is unique
def register_user(username, password, fullname, email):
    ensure_user_csv_exists()

    # If user already exists, return failure
    if user_exists(username):
        return False, "Username already exists! Pick a different username"
    # Append new user details to the CSV file
    with open(DATA_PATH, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([username, password, fullname, email])
    return True, "Registration Successful"

#Checks if a username is already registered
def user_exists(username):
    ensure_user_csv_exists() #ensure file exists

    #open the CSV and scan each row
    with open(DATA_PATH, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username:
                return True #username found
    return False #username not found

#Verifies a username-password pair for login
def authenticate_user(username, password):
    ensure_user_csv_exists() #Ensure file exists

    # Open the CSV and check if credentials match any record
    with open(DATA_PATH, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['username'] == username and row['password'] == password:
             return True # Login successful
    return False # Login failed