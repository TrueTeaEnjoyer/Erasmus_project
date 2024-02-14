
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
with open('oGoodnight.json') as f:
    events = json.load(f)

# Map of German to English day names
german_to_english_days = {
    'Montag': 'Monday',
    'Dienstag': 'Tuesday',
    'Mittwoch': 'Wednesday',
    'Donnerstag': 'Thursday',
    'Freitag': 'Friday',
    'Samstag': 'Saturday',
    'Sonntag': 'Sunday'
}

# Create calendar events from loaded data
for event in events:
    # Parse the title and link
    title = event['Title']
    link = event['Link'][0]  # Assuming there's only one link

    # Parse the date and time
    date_str = event['Date']
    date_parts = date_str.split(' ')

    # Print date_parts to inspect its contents
    print("date_parts:", date_parts)

    if len(date_parts) >= 3:
        # Extract time range and date
        time_range = date_parts[1]
        date = date_parts[-1]  # Extract the date

        # Parse time range
        start_time_str, end_time_str = time_range.split('-')
        start_time = datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.strptime(end_time_str, "%H:%M").time()

        # Parse the date with year
        start_datetime = datetime.strptime(date, "%d.%m.%y")  # Assuming the date is in the format DD.MM.YY

        # Combine date and time to create datetime objects
        start_datetime = datetime.combine(start_datetime.date(), start_time)
        end_datetime = datetime.combine(start_datetime.date(), end_time)

        # Create the event with start and end times
        event_data = {
            'name': title,
            'start': start_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'stop': end_datetime.strftime('%Y-%m-%d %H:%M:%S'),  # Use stop instead of end for XML-RPC
            'description': link,  # Using the link as the description
            'location': link,  # Using the link as the location as well
        }
        event_id = models.execute_kw(db, uid, password, 'calendar.event', 'create', [event_data])