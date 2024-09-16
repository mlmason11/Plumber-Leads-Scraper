
# Google Places Leads Fetcher using Apify

This Python application allows users to fetch business leads (like local businesses) using the **Apify Google Places Crawler**. Users can search for businesses by specifying latitude, longitude, and search terms. The application retrieves business details and allows saving the results in CSV or Excel format.

## Features

- Fetch business data from Apify's Google Places Crawler API.
- Save the results in CSV or Excel format.
- User input for dynamic location search (latitude, longitude, and query).
- Supports flexible search radius for precise data gathering.

## Requirements

Before you begin, ensure you have met the following requirements:

- You need an Apify account and an API key for accessing the Google Places Crawler.
- Python 3.6 or later is required.
- The following Python packages are required:
  - `requests`
  - `pandas`
  - `openpyxl`

You can install the required packages using the following command:

```bash
pip install requests pandas openpyxl
```

## Setup

1. Clone the repository or download the files to your local machine.

2. Install the required Python dependencies by running:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `config.py` file in the root directory and add your **Apify API key** as follows:

   ```python
   APIFY_API_KEY = 'your-apify-api-key-here'
   ```

## Usage

1. Run the script using:

   ```bash
   python app.py
   ```

2. When prompted, input the following:

   - **Latitude**: The latitude for the location to search (e.g., `40.712776` for New York City).
   - **Longitude**: The longitude for the location to search (e.g., `-74.005974` for New York City).
   - **Search query**: What you're looking for (e.g., `plumber`).
   - **Search radius**: The radius (in meters) to search within (e.g., `10000` for 10km).
   - **File format**: Choose whether to save the results as `csv`, `excel`, or both.

3. The script will retrieve the business data and prompt you for a filename before saving the data.

## Example

Here's a sample flow:

1. **Latitude**: `40.712776`
2. **Longitude**: `-74.005974`
3. **Search query**: `restaurant`
4. **Search radius**: `5000` (5km)
5. **File format**: `both` (CSV and Excel)
6. **CSV filename**: `restaurants_nyc.csv`
7. **Excel filename**: `restaurants_nyc.xlsx`

The output files will be saved to the `data` directory.

## Error Handling

- **Connection errors**: If the script cannot connect to the API, a detailed error message will be printed.
- **File I/O errors**: If saving the results fails due to file permissions or incorrect paths, appropriate error messages are shown.
- **Input validation**: The script checks for missing or invalid inputs and prompts the user accordingly.

## Limitations

- Make sure your Apify account has sufficient API credits to run the Google Places Crawler.
- The accuracy and availability of data depend on Google Places and Apify API responses.

## License

This project is licensed under the MIT License.

## Contact

If you have any questions or feedback, feel free to reach out.
