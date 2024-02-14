import json
import xmlrpc.client
import ssl
from datetime import datetime, timedelta

url = "http://148.251.132.24:8069"
db = "student"
username = 'student'
password = "student"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), verbose=False, use_datetime=True, context=ssl._create_unverified_context())
common.version()
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), verbose=False, use_datetime=True, context=ssl._create_unverified_context())

# Load event data from JSON file
with open('oFlucc.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

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
for event in data:
    # Extract date and time information
    date_str = event['Date']
    date_parts = date_str.split(', ')[1].split(' ')
    date = ' '.join(date_parts[:3])
    time = date_parts[3]

    # Extract start and end times
    start_time, end_time = time.split('—')

    # Remove unnecessary characters from end_time
    end_time = end_time.split('\\')[0]

    # Parse the date with year
    start_datetime = datetime.strptime(date, "%d. %b %Y")

    # Combine date and time to create datetime objects
    start_datetime = datetime.combine(start_datetime.date(), datetime.strptime(start_time, "%H:%M").time())
    end_datetime = datetime.combine(start_datetime.date(), datetime.strptime(end_time, "%H:%M").time())

    # Create the event with start and end times
    event_data = {
        'name': event['Title'],
        'start': start_datetime.strftime('%Y-%m-%d %H:%M:%S'),
        'stop': end_datetime.strftime('%Y-%m-%d %H:%M:%S'),  # Use stop instead of end for XML-RPC
        'description': event['Link'],  # Using the link as the description
        'location': event['Link'],  # Using the link as the location as well
    }
    event_id = models.execute_kw(db, uid, password, 'calendar.event', 'create', [event_data])
    print("New event created with ID:", event_id)