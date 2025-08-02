import csv
import os
#handles seat availability and bookings

def bookings_path(flight_id):
    return os.path.join(os.path.dirname(__file__), '..', 'data', f'bookings_{flight_id}.csv')

def load_bookings(flight_id):
    path = bookings_path(flight_id)
    if not os.path.exists(path):
        return {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        return {row['seat']: row for row in reader}

def save_booking(flight_id, seat, passenger):
    path = bookings_path(flight_id)
    exists = os.path.exists(path)
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(['seat','name','gender','passport','visa','booked_by'])
        writer.writerow([seat, passenger['name'], passenger['gender'],
                         passenger['passport'], passenger['visa'], passenger['booked_by']])
