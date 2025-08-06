import csv
import os

#This module handles seat availability and bookings
#Bookings are stored for each flight separately named by flight_id

#Function to generate file path for a specific flight's bookings
def bookings_path(flight_id):
    return os.path.join(os.path.dirname(__file__), '..', 'data', f'bookings_{flight_id}.csv')

#Function to load bookings for a given flight
def load_bookings(flight_id):
    path = bookings_path(flight_id)

    # If the bookings file doesn't exist, return an empty dictionary
    if not os.path.exists(path):
        return {}

    # Open the bookings file and read all bookings into a dictionary
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        return {row['seat']: row for row in reader}

# Function to save a new booking for a seat on a flight
def save_booking(flight_id, seat, passenger):
    path = bookings_path(flight_id)
    exists = os.path.exists(path)

    # Open the file in append mode to add a new booking
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)

        # If this is the first booking for the flight, write header row
        if not exists:
            writer.writerow(['seat','name','gender','passport','visa','booked_by'])

        # Write the passenger's booking info to the file
        writer.writerow([
            seat,
            passenger.get('name'),
            passenger.get('gender'),
            passenger.get('passport'),
            passenger.get('visa'),
            passenger.get('booked_by')  #The user who made the booking
        ])

# Function to get all bookings made by a specific user (by username)
def user_bookings(username):
    bookings = []

    # Look through all files in the 'data' directory
    for fname in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'data')):

        # Filter to only include files named like bookings_<flight_id>.csv
        if fname.startswith("bookings_") and fname.endswith(".csv"):
            path = os.path.join(os.path.dirname(__file__), '..', 'data', fname)

            # Read each file and look for rows booked by the given username
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:

                    # Compare booked_by field (case-insensitive, stripped)
                    if row.get('booked_by', '').strip().lower() == username.strip().lower():
                        # Extract flight_id from filename
                        flight_id = fname.replace("bookings_", "").replace(".csv", "")
                        row['flight_id'] = flight_id # Add flight_id to the booking info
                        bookings.append(row)

    return bookings # Return a list of all bookings by this user

