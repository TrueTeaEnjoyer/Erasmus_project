
import json
import xmlrpc.client
import ssl
from datetime import datetime, timedelta

url = "http://148.251.132.24:8069"
db = "student"
username = 'student'
password = "student"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), verbose=False, use_datetime=True,
                                   context=ssl._create_unverified_context())
common.version()
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), verbose=False, use_datetime=True,
                                   context=ssl._create_unverified_context())

# Load event data from JSON file
with open('oGoabase.json') as f:
    events = json.load(f)

# Map of German to English month names
german_to_english_months = {
    'Januar': 'January',
    'Feber': 'February',
    'März': 'March',
    'April': 'April',
    'Mai': 'May',
    'Juni': 'June',
    'Juli': 'July',
    'August': 'August',
    'September': 'September',
    'Oktober': 'October',
    'November': 'November',
    'Dezember': 'December'
}

# Create calendar events from loaded data
for event in events:
    # Parse the start and end dates
    start_date_str = event['Date'][0]

    # Split the start date string
    start_date_parts = start_date_str.split(', ')

    # Print start_date_parts to inspect its contents
    print("start_date_parts:", start_date_parts)

    # Proceed only if start_date_parts contains at least two elements
    if len(start_date_parts) >= 2:
        date_str = start_date_parts[1]  # Extract the date part
        time_str = start_date_parts[2]  # Extract the time part

        # Reconstruct the start date string
        start_datetime = datetime.strptime(date_str + ' ' + time_str, "%d %b %y %H:%M")

        # Calculate the end time (assuming 3 hours duration)
        end_datetime = start_datetime + timedelta(hours=3)

        # Create the event with start and end times
        event_data = {
            'name': event['Title'],
            'start': start_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'stop': end_datetime.strftime('%Y-%m-%d %H:%M:%S'),  # Use stop instead of end for XML-RPC
            'description': event['Link'],  # Using the link as the description
            'location': event['Link'],  # Using the link as the location as well
        }
        event_id = models.execute_kw(db, uid, password, 'calendar.event', 'create', [event_data])