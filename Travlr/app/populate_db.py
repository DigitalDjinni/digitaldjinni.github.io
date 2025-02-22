import sys
import os
from app import db, create_app
from app.models import Trip
import json
from datetime import datetime

# Adds Travlr to my python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize the Flask application
app = create_app()
app.app_context().push()

# JSON file path
json_file_path = os.path.join(os.path.dirname(__file__), 'trips.json')

# Check if the JSON file exists
if not os.path.exists(json_file_path):
    print(f"JSON file was not foun at {json_file_path}")
    exit(1)

# Load JSON data
with open(json_file_path, 'r') as file:
    trips_data = json.load(file)

# Insert trips into the database
for trip_data in trips_data:
    try:
        new_trip = Trip(
            code=trip_data['code'],
            name=trip_data['name'],
            length=trip_data['length'],
            start=datetime.strptime(trip_data['start'], '%Y-%m-%dT%H:%M:%SZ').date(),
            resort=trip_data['resort'],
            per_person=float(trip_data['perPerson']),
            image=trip_data['image'],
            description=trip_data['description']
        )
        db.session.add(new_trip)
    except Exception as e:
        print(f"Error adding trip {trip_data['code']}: {e}")
        db.session.rollback()

# Commits changes to database
try:
    db.session.commit()
    print("JSON was successfully added to the database!")
except Exception as e:
    db.session.rollback()
    print(f"Failed to add JSON file to the database: {e}")
