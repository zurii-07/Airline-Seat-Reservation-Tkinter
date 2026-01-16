import csv
import os
from datetime import datetime, timedelta

#Function to load airport data from a CSV file
def load_airports():
    #Building the path to 'airports.csv' in the '../data/' folder
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'airports.csv')
    airports = []

    # Open the CSV file with UTF-8 encoding
    with open(path, encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f) # Read rows as dictionaries
        for r in reader:
            airports.append(r) #adding each airport dict to the list

    return airports # Return list of all airports

# Function to generate flight schedules for a number of upcoming days
def generate_flights(days_ahead=7):
    airports = load_airports() # Load the list of airports
    flights = [] # Initialize list to store generated flights
    idx = 1 # Flight ID counter (used to make unique IDs)
    now = datetime.now() # Current date and time

    # Loop over each day for the next 'days_ahead' days
    for i in range(days_ahead):
        dt = now + timedelta(days=i) # Calculate the date for day i

        # For every possible pair of airports (origin → destination)
        for origin in airports:
            for dest in airports:
                # Skip flights where origin and destination are in the same country
                if origin['Country'] == dest['Country']:
                    continue

                #creating a flight dictionary
                flight = {
                    'flight_id': f"FL{idx:04d}",
                    'date': dt.strftime("%Y-%m-%d"), #upcomming 7 days from the current day
                    'time': f"{10 + (idx % 10):02d}:00",  # sample times
                    'origin_country': origin['Country'],
                    'origin_airport': origin['Airport'],
                    'dest_country': dest['Country'],
                    'dest_airport': dest['Airport']
                }
                flights.append(flight) #adding the flight to the list
                idx += 1 #increment flight ID counter

    return flights #return the list of generated flights



