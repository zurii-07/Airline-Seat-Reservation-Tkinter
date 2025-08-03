import csv
import os
from datetime import datetime, timedelta

def load_airports():
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'airports.csv')
    airports = []
    with open(path, encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            airports.append(r)
    return airports

def generate_flights(days_ahead=7):
    airports = load_airports()
    flights = []
    idx = 1
    now = datetime.now()
    for i in range(days_ahead):
        dt = now + timedelta(days=i)
        for origin in airports:
            for dest in airports:
                if origin['Country'] == dest['Country']:
                    continue
                flight = {
                    'flight_id': f"FL{idx:04d}",
                    'date': dt.strftime("%Y-%m-%d"), #upcomming 7 days from the current day
                    'time': f"{10 + (idx % 10):02d}:00",  # sample times
                    'origin_country': origin['Country'],
                    'origin_airport': origin['Airport'],
                    'dest_country': dest['Country'],
                    'dest_airport': dest['Airport']
                }
                flights.append(flight)
                idx += 1
    return flights



