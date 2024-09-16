import requests
import csv
import pandas as pd
from config import APIFY_API_KEY


# Function to fetch places data from Apify's Google Places Crawler
def fetch_places_from_apify(api_key, lat, lng, query, radius=10000):
    url = f"https://api.apify.com/v2/actor-tasks/{api_key}/run-sync-get-dataset-items"
    payload = {
        'searchString': query,
        'lat': lat,
        'lng': lng,
        'radius': radius,  # Search radius in meters
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")
    return []


# Function to save the places data to a CSV file
def save_to_csv(places, filename="data/apify_places_leads.csv"):
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
                    'Email': place.get('email', 'N/A'),  # Apify may return emails if available
                    'Website': place.get('website', 'N/A')
                })
        print(f"Leads saved to {filename}")
    except IOError as io_err:
        print(f"Error writing to file {filename}: {io_err}")


# Function to save the places data to an Excel file
def save_to_excel(places, filename="data/apify_places_leads.xlsx"):
    data = []
    for place in places:
        data.append({
            'Business Name': place.get('title', 'N/A'),
            'Address': place.get('address', 'N/A'),
            'Rating': place.get('rating', 'N/A'),
            'Phone Number': place.get('phone', 'N/A'),
            'Email': place.get('email', 'N/A'),  # Apify may return emails if available
            'Website': place.get('website', 'N/A')
        })

    df = pd.DataFrame(data)

    try:
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Leads saved to {filename}")
    except IOError as io_err:
        print(f"Error writing to Excel file {filename}: {io_err}")


# Main program execution
if __name__ == "__main__":
    try:
        api_key = APIFY_API_KEY
        lat = input("Enter the latitude (e.g., '40.712776' for New York City): ")
        lng = input("Enter the longitude (e.g., '-74.005974' for New York City): ")
        query = input("Enter your search query (e.g., 'plumber'): ")
        radius = input("Enter the search radius in meters (e.g., 10000 for 10km): ")

        if not lat or not lng or not query or not radius:
            raise ValueError("Latitude, longitude, search query, and radius are all required fields.")

        # Fetch places using Apify
        places = fetch_places_from_apify(api_key, lat, lng, query, int(radius))

        if not places:
            print("No results were returned from the API.")
        else:
            file_formats = input("Which formats would you like to save? (Enter 'csv', 'excel', or 'both'): ").lower()

            if file_formats == 'csv':
                csv_filename = input("Enter the CSV filename (e.g., 'apify_places_leads.csv'): ")
                save_to_csv(places, f"data/{csv_filename}")
            elif file_formats == 'excel':
                excel_filename = input("Enter the Excel filename (e.g., 'apify_places_leads.xlsx'): ")
                save_to_excel(places, f"data/{excel_filename}")
            elif file_formats == 'both':
                csv_filename = input("Enter the CSV filename (e.g., 'apify_places_leads.csv'): ")
                excel_filename = input("Enter the Excel filename (e.g., 'apify_places_leads.xlsx'): ")
                save_to_csv(places, f"data/{csv_filename}")
                save_to_excel(places, f"data/{excel_filename}")
            else:
                print("Invalid option. Please enter 'csv', 'excel', or 'both'.")

    except ValueError as val_err:
        print(f"Input error: {val_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
