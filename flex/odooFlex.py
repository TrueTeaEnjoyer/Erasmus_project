import json
import xmlrpc.client
import ssl
from datetime import datetime

url = "http://148.251.132.24:8069"
db = "student"
username = 'student'
password = "student"

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url), verbose=False, use_datetime=True, context=ssl._create_unverified_context())
common.version()
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url), verbose=False, use_datetime=True, context=ssl._create_unverified_context())

# Load event data from JSON file
with open('oFlex.json') as f:
    events = json.load(f)

# Create calendar events from loaded data
for event in events:
    date_parts = event['Date'].split(' - ')
    start_time = datetime.strptime(date_parts[0], "%d %b %H:%M")
    end_time = date_parts[1]  # Just use the end time as string
    event_date = start_time.replace(year=datetime.now().year)  # Assuming all events are in the current year

    # Create the event with start and end times
    event_data = {
        'name': event['Title'],
        'start': event_date.strftime('%Y-%m-%d %H:%M:%S'),
        'stop': event_date.strftime('%Y-%m-%d ') + end_time,  # Combine date with end time string
        'description': event['Link'],  # Using the link as the description
        'location': event['Link'],  # Using the link as the location as well
    }
    event_id = models.execute_kw(db, uid, password, 'calendar.event', 'create', [event_data])
    print("New event created with ID:", event_id)