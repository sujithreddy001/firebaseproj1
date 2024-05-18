Firebase Firestore Population Scripts
This project contains Python scripts to populate a Firebase Firestore database with random user data and geohash-based time slots for locations around Hyderabad ORR (Outer Ring Road).

Setup Instructions
Prerequisites
Python 3.x
Firebase account
Service account key for Firebase project
Firebase Configuration
Create a Firebase Project:

Go to the Firebase Console.
Create a new project named proj2.
Download Service Account Key:

Navigate to Project Settings > Service Accounts.
Generate a new private key and download the JSON file.
Install Required Python Packages
Install the required packages using pip:

bash
Copy code
pip install firebase-admin geopy
User Population Script
This script populates the Firestore database with 80 random users.

populate_users.py
python
Copy code
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import string

# Initialize Firebase App
cred = credentials.Certificate("/path/to/your/firebase-key.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore Client
db = firestore.client()

# Function to Generate Random User
def random_user():
    full_name = ''.join(random.choices(string.ascii_letters, k=10)) + ' ' + ''.join(random.choices(string.ascii_letters, k=10))
    email_id = ''.join(random.choices(string.ascii_letters, k=5)) + '@gmail.com'
    phone_number = '+91' + ''.join(random.choices(string.digits, k=10))
    age = random.randint(16, 70)
    city = random.choice(['Hyderabad', 'Nizamabad', 'Karimnagar', 'Medak', 'Siddipet', 'Sangareddy', 'Secunderabad', 'Rangareddy'])
    
    user = {
        "fullName": full_name,
        "emailID": email_id,
        "phoneNumber": phone_number,
        "age": age,
        "city": city
    }
    
    return user

# Function to Populate Users
def populate_users(num_users):
    users_ref = db.collection('users')
    for _ in range(num_users):
        user_data = random_user()
        users_ref.add(user_data)

if __name__ == "__main__":
    num_users = 80
    populate_users(num_users)
    print("80 users populated in Firestore.")
Time Slots and Geohash Script
This script populates the Firestore database with 20 random geohashes and corresponding time slots for each of the next 5 dates.

timeslots.py
python
Copy code
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import string
from geopy.distance import geodesic
from geopy.point import Point

# Initialize Firebase App
cred = credentials.Certificate("/path/to/your/firebase-key.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore Client
db = firestore.client()

# Function to Generate Geohash
def generate_geohash():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# Function to Generate Dates
def generate_dates():
    return [str(20240517 + i) for i in range(1, 6)]

# Function to Generate Time Slots
def generate_time_slots():
    time_slots = []
    for hour in range(9, 22):
        for minute in range(0, 60, 60):
            time = f"{hour:02d}:{minute:02d}"
            time_slots.append({"time": time, "available": 15})
            if len(time_slots) >= 15:
                break
    return time_slots

# Function to Generate Random Location within Hyderabad ORR
def generate_random_location_within_hyd():
    center_point = Point(17.3850, 78.4867)
    radius = 5
    while True:
        random_distance = random.uniform(0, radius)
        random_bearing = random.uniform(0, 360)
        destination = geodesic(kilometers=random_distance).destination(center_point, random_bearing)
        if is_within_bounds(destination):
            return (destination.latitude, destination.longitude)

# Function to Check if Point is within Bounds
def is_within_bounds(point):
    min_lat, max_lat = 17.2000, 17.6000
    min_lon, max_lon = 78.2000, 78.8000
    return min_lat <= point.latitude <= max_lat and min_lon <= point.longitude <= max_lon

# Function to Populate Geohashes Collection
def populate_hyd_geohashes_collection():
    dates = generate_dates()
    for _ in range(20):
        is_active = random.choice([True, False])
        if not is_active:
            continue
        geohash_value = generate_geohash()
        doc_ref = db.collection("hyd_areas").document(geohash_value)
        doc_ref.set({
            "geoHash": geohash_value,
            "is_active": is_active
        })
        for date in dates:
            time_slots = generate_time_slots()
            doc_ref.collection("availableGeneralSlots").document(date).set({
                "date": date,
                "dropdownTimeslots": time_slots
            })

if __name__ == "__main__":
    populate_hyd_geohashes_collection()
    print("20 geohashes and time slots populated in Firestore.")
Execution
Ensure you have your Firebase service account key JSON file at the specified path in the script.
Run the scripts:
bash
Copy code
python populate_users.py
python timeslots.py
Check your Firestore database to see the populated data.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Make sure to replace "/path/to/your/firebase-key.json" with the actual path to your Firebase service account key JSON file. This README provides clear instructions on setting up and running the scripts for populating the Firestore database.






