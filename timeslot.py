import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import string
from geopy.distance import geodesic
from geopy.point import Point

cred = credentials.Certificate("/Users/sujithreddy/Desktop/Tempdata/pythonscript-25e2e-firebase-adminsdk-n73wq-92776b9082.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def generate_geohash():
    """
    Generating geohash with 6 characters.
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

def generate_dates():
    """
    Generating dates in YYYYMMDD format.
    """
    return [str(20240517 + i) for i in range(1, 6)]  

def generate_time_slots():

    time_slots = []
    for hour in range(9, 22):  # A slots from 9 AM to 9 PM
        for minute in range(0, 60, 60):  # slots in 60-minute intervals
            time = f"{hour:02d}:{minute:02d}"
            time_slots.append({"time": time, "available": 15})
            if len(time_slots) >= 15:
                break
    return time_slots

def generate_random_location_within_hyd():
    """
    Generates a random location within a rough bounding box around Hyderabad's ORR.
    """
    center_point = Point(17.3850, 78.4867)  # Latitude and Longitude of Hyderabad center
    radius = 5 

    while True:
        random_distance = random.uniform(0, radius)
        random_bearing = random.uniform(0, 360)
        destination = geodesic(kilometers=random_distance).destination(center_point, random_bearing)
        if is_within_bounds(destination):
            return (destination.latitude, destination.longitude)

def is_within_bounds(point):
    """
    Checking the point point in  Hyderabad ORR.
    """
    min_lat, max_lat = 17.2000, 17.6000  # orr latitude
    min_lon, max_lon = 78.2000, 78.8000  # orr longitude

    return min_lat <= point.latitude <= max_lat and min_lon <= point.longitude <= max_lon

def populate_hyd_geohashes_collection():
    """
    populates 6-character geohashes for areas within Hyderabad ORR.
    """
    dates = generate_dates()

    for _ in range(20): 
        is_active = random.choice([True, False])
        if not is_active:
            continue 
        generate_random_location_within_hyd()
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
    
    # Populate the hyderabad_orr_areas collection
    populate_hyd_geohashes_collection()
    
    print("successful.")
