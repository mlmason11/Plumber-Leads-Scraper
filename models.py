import sqlite3
from datetime import datetime

# Define the Business class to model a business entity
class Business:
    def __init__(self, business_name, address, phone, email, website, rating, lat, lng, business_type):
        self.business_name = business_name
        self.address = address
        self.phone = phone
        self.email = email
        self.website = website
        self.rating = rating
        self.lat = lat
        self.lng = lng
        self.business_type = business_type  # New field to classify businesses
        self.last_updated = datetime.now()

    @staticmethod
    def setup_database():
        conn = sqlite3.connect("local_cache.db")
        c = conn.cursor()
        # Create businesses table if it doesn't exist
        c.execute('''CREATE TABLE IF NOT EXISTS businesses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    business_name TEXT,
                    address TEXT,
                    phone TEXT,
                    email TEXT,
                    website TEXT,
                    rating REAL,
                    lat REAL,
                    lng REAL,
                    business_type TEXT,  # New field to store the type of business
                    last_updated TIMESTAMP
                    )''')
        conn.commit()
        conn.close()

    # Method to check if a business already exists in the cache
    @staticmethod
    def business_exists(business_name, address):
        conn = sqlite3.connect("local_cache.db")
        c = conn.cursor()
        c.execute("SELECT 1 FROM businesses WHERE business_name=? AND address=?", (business_name, address))
        exists = c.fetchone() is not None
        conn.close()
        return exists

    # Method to add a new business to the cache
    def add_to_cache(self):
        conn = sqlite3.connect("local_cache.db")
        c = conn.cursor()
        c.execute('''INSERT INTO businesses 
                    (business_name, address, phone, email, website, rating, lat, lng, business_type, last_updated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                  (self.business_name, self.address, self.phone, self.email, self.website,
                   self.rating, self.lat, self.lng, self.business_type, self.last_updated))
        conn.commit()
        conn.close()

    # Method to retrieve all businesses of a specific type from the cache
    @staticmethod
    def get_businesses_by_type(business_type):
        conn = sqlite3.connect("local_cache.db")
        c = conn.cursor()
        c.execute("SELECT * FROM businesses WHERE business_type=?", (business_type,))
        businesses = c.fetchall()
        conn.close()
        return businesses
