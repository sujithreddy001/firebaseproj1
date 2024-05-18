import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import random
import string

cred = credentials.Certificate("/Users/sujithreddy/Desktop/Tempdata/pythonscript-25e2e-firebase-adminsdk-n73wq-92776b9082.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# For generating random users
def random_user():
    full_name = ''.join(random.choices(string.ascii_letters, k=10)) + ' ' + ''.join(random.choices(string.ascii_letters, k=10))
    email_id = ''.join(random.choices(string.ascii_letters, k=5)) + '@gmail.com'
    phone_number = '+91'+''.join(random.choices(string.digits, k=10))
    age = random.randint(16, 70)
    city = random.choice(['Hyderabad', 'Nizambad', 'Karimnagar', 'Medak', 'Siddipet','Sangareddy','Secunderabad','Rangareddy'])
    
    user = {
        "fullName": full_name,
        "emailID": email_id,
        "phoneNumber": phone_number,
        "age": age,
        "city": city
    }
    
    return user

def populate_users(num_users):
    users_ref = db.collection('users')
    for _ in range(num_users):
        user_data = random_user()
        users_ref.add(user_data)

if __name__ == "__main__":
    num_users = 80
    populate_users(num_users)

print("successful")