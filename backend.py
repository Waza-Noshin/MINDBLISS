from bcrypt import hashpw, gensalt, checkpw
from pymongo import MongoClient

class Backend:
    def __init__(self):
        """ Initialize MongoDB connection """
        try:
            self.client = MongoClient('mongodb://localhost:27017/')
            self.client.server_info()  # Check MongoDB connection
            self.db = self.client['mindbliss']
            self.users = self.db['users']
            self.scribblings = self.db['scribblings']
            print("[INFO] MongoDB connected successfully!")
        except Exception as e:
            print("[ERROR] MongoDB Connection Failed:", e)

    def register_user(self, username, email, password):
        """ Register a new user securely """
        if self.users.find_one({'$or': [{'username': username}, {'email': email}]}):
            print("[INFO] User already exists:", username, email)
            return False

        hashed_password = hashpw(password.encode(), gensalt())  # Store as bytes
        self.users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password  # Store as bytes (MongoDB handles it correctly)
        })
        print("[INFO] User registered successfully!")
        return True

    def login_user(self, username, password):
        """ Authenticate a user """
        user = self.users.find_one({"username": username})
        if user:
            stored_password = user['password']
            if isinstance(stored_password, str):
                stored_password = stored_password.encode()  # Convert to bytes for bcrypt

            if checkpw(password.encode(), stored_password):  # Compare correctly
                return user  # Return the full user document
        return None

    def save_scribble(self, user_id, note):
        """ Save a scribble """
        from bson.objectid import ObjectId
        if isinstance(user_id, str):
            user_id = ObjectId(user_id)  # Convert string to ObjectId
        self.scribblings.insert_one({
            "user_id": user_id,
            "note": note
        })

    def get_scribblings(self, user_id):
        """ Fetch all scribblings for a user """
        try:
            print(f"Fetching scribblings for user_id: {user_id}")
            scribblings = list(self.scribblings.find({"user_id": user_id}))
            print(f"Scribblings found: {scribblings}")
            return scribblings
        except Exception as e:
            print(f"Error fetching scribblings: {e}")
            return []

# Initialize backend
backend = Backend()