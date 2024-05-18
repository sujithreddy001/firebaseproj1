Here's a comprehensive `README.md` file for your Firebase project:

```markdown
# Firebase Firestore Population Scripts

This project contains Python scripts to populate a Firebase Firestore database with random user data and geohash-based time slots for locations around Hyderabad ORR (Outer Ring Road).

## Project Setup

### Prerequisites

- Python 3.x
- Firebase account
- Firebase Admin SDK service account key

### Firebase Configuration

1. **Create a Firebase Project**:
   - Go to the [Firebase Console](https://console.firebase.google.com/).
   - Create a new project named `proj2`.

2. **Download Service Account Key**:
   - Navigate to Project Settings > Service Accounts.
   - Generate a new private key and download the JSON file.

### Install Required Python Packages

Install the required packages using pip:

```bash
pip install firebase-admin geopy
```

## User Population Script

This script populates the Firestore database with 80 random users.

### `populate_users.py`

```python
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
```

### Execution

To run the user population script, execute the following command in your terminal:

```bash
python populate_users.py
```

## Time Slots and Geohash Script

This script populates the Firestore database with 20 random geohashes and corresponding time slots for each of the next 5 dates.

### `timeslots.py`

```python
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
```

### Execution

To run the time slots and geohash script, execute the following command in your terminal:

```bash
python timeslots.py
```

## Repository Setup

### Clone the Repository

If you haven't already, clone the repository to your local machine using VS Code:

1. Open VS Code.
2. Open the Command Palette (`Ctrl+Shift+P`).
3. Type `Git: Clone` and select it.
4. Enter your repository URL: `https://github.com/sujithreddy001/firebaseproj1.git`
5. Select the local directory to clone the repository.

### Initial Commit and Push to GitHub

Follow these steps to commit your changes and push them to GitHub:

1. Open the integrated terminal in VS Code (`View > Terminal`).

2. Initialize a Git repository if not already done:
   ```bash
   git init
   ```

3. Add all files to the Git index:
   ```bash
   git add .
   ```

4. Commit the files:
   ```bash
   git commit -m "Initial commit"
   ```

5. Rename the default branch to `main` if it's not already:
   ```bash
   git branch -M main
   ```

6. Add the remote repository:
   ```bash
   git remote add origin https://github.com/sujithreddy001/firebaseproj1.git
   ```

7. Push to the remote repository and set the upstream branch:
   ```bash
   git push -u origin main
   ```
Contact Information
For any questions or inquiries, please contact:

Name: Sujith Reddy
Email: sujithreddy4959@gmail.com
GitHub: sujithreddy001


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Notes

- Make sure to replace `/path/to/your/firebase-key.json` with the actual path to your Firebase service account key JSON file.
- Adjust any other paths and details as necessary for your specific setup.
