from models import Business  # Import the Business class from models.py
import requests
import csv
import logging
from datetime import datetime
from config import APIFY_API_KEY

# Setup logging
logging.basicConfig(filename="app.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Function to fetch places data from Apify's Google Places Crawler
def fetch_places_from_apify(api_key, lat, lng, query, radius=10000):
    logging.info("Fetching new results from API for query: %s", query)
    url = f"https://api.apify.com/v2/actor-tasks/{api_key}/run-sync-get-dataset-items"
    payload = {
        'searchString': query,
        'lat': lat,
        'lng': lng,
        'radius': radius  # Search radius in meters
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        places = response.json()
        return places
    except requests.exceptions.RequestException as req_err:
        logging.error(f"API request failed: {req_err}")
        return []

# Function to detect and add new businesses
def detect_new_businesses(places, business_type):
    new_businesses = []
    for place in places:
        business_name = place.get('title', 'N/A')
        address = place.get('address', 'N/A')

        if not Business.business_exists(business_name, address):
            business = Business(
                business_name=business_name,
                address=address,
                phone=place.get('phone', 'N/A'),
                email=place.get('email', 'N/A'),
                website=place.get('website', 'N/A'),
                rating=place.get('rating', 0),
                lat=place.get('lat', 0),
                lng=place.get('lng', 0),
                business_type=business_type  # Pass the business type
            )
            business.add_to_cache()
            new_businesses.append(business)

    return new_businesses

# Function to save the places data to a CSV file
def save_to_csv(places, filename):
    fieldnames = ['Business Name', 'Address', 'Rating', 'Phone Number', 'Email', 'Website']

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for place in places:
                writer.writerow({
                    'Business Name': place.get('title', 'N/A'),
                    'Address': place.get('address', 'N/A'),
                    'Rating': place.get('rating', 'N/A'),
                    'Phone Number': place.get('phone', 'N/A'),
                    'Email': place.get('email', 'N/A'),
                    'Website': place.get('website', 'N/A')
                })
        logging.info(f"Leads saved to {filename}")
    except IOError as io_err:
        logging.error(f"Error writing to file {filename}: {io_err}")

# Dynamic file naming based on query and timestamp
def generate_filename(query, extension='csv'):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_query = query.replace(" ", "_")
    return f"data/{sanitized_query}_{timestamp}.{extension}"

# Main program execution
if __name__ == "__main__":
    Business.setup_database()  # Ensure database and businesses table are set up

    try:
        api_key = APIFY_API_KEY

        # Default location and query for Manhattan plumbers
        default_lat = 40.7831
        default_lng = -73.9712
        default_query = "plumber"
        default_radius = 10000  # 10 km

        # Prompt the user for optional inputs
        lat = input(f"Enter the latitude (default {default_lat}): ") or str(default_lat)
        lng = input(f"Enter the longitude (default {default_lng}): ") or str(default_lng)
        query = input(f"Enter your search query (default '{default_query}'): ") or default_query
        radius = input(f"Enter the search radius in meters (default {default_radius}): ") or str(default_radius)
        business_type = input(f"Enter the business type (e.g., plumber, property manager, insurance agent): ").strip()

        # Fetch places using Apify
        places = fetch_places_from_apify(api_key, float(lat), float(lng), query, int(radius))

        if not places:
            logging.info("No results were returned from the API.")
            print("No results found.")
        else:
            # Detect and add new businesses
            new_businesses = detect_new_businesses(places, business_type)

            if new_businesses:
                print(f"Found {len(new_businesses)} new {business_type} businesses.")
                logging.info(f"{len(new_businesses)} new businesses found and added to cache.")
            else:
                print(f"No new {business_type} businesses found. All businesses already exist in the cache.")

            # Save the results (both cached and new)
            filename = generate_filename(query)
            save_to_csv(places, filename)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
