from __future__ import print_function

from datetime import datetime
import json
import openai
import os.path
import pytz

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

LOCAL_TIME_ZONE = pytz.timezone("America/Los_Angeles")


def gen_prompt(user_input):
    # TODO: Get today's date, and place in day_name and formatted_data
    day_name = "Sunday"
    formatted_date = "2023-06-18"
    return "Generate a JSON file that is an array of events named 'events'. Each event has the following fields: " \
           "eventName, duration (in minutes), possibleIntervals[ { date, timePeriod: {startTime, endTime} ]. " \
           "timePeriod indicates the full range of time that event could happen. Today is " + day_name + " " + \
           formatted_date + ". Query: " + user_input


def get_gpt_response(user_input):
    """Parses the user_input into a JSON file using the GPT-3 model."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,
        messages=[{"role": "user", "content": gen_prompt(user_input)}],
    )
    return json.loads(response.choices[0].message.content)


def convert_date_time_to_utc(date, time):
    """Given: a date: YYYY-MM-DD, and time: HH:MM in local timezone
       Returns: date and time in ISO format in UTC."""
    naive = datetime.strptime(date + " " + time, "%Y-%m-%d %H:%M")
    local_dt = LOCAL_TIME_ZONE.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    return utc_dt.isoformat().replace('+00:00', 'Z')


def find_free_slot(service, duration, pos_interval_start, pos_interval_end):
    """Given: pos_interval_start, pos_interval_end, both date + time in ISO format in UTC
              duration, how long the event will last
       Returns: a free slot [free_slot_start, free_slot_end] in ISO format in UTC,
                or [-1,-1] if free slot cannot be found. """
    free_slot = [-1, -1]

    duration_min = datetime.timedelta(minutes=duration)

    free_busy_body = {
        "timeMin": pos_interval_start,
        "timeMax": pos_interval_end,
        "items": [
            {
                "id": "primary"
            }
        ]
    }

    free_busy_res = service.freebusy().query(body=free_busy_body).execute()
    busy_list = free_busy_res['calendars']['primary']['busy']

    free_start = datetime.fromisoformat(pos_interval_start.replace('Z', ''))
    if len(busy_list) == 0:
        free_end = free_start + duration_min
        free_slot = [free_start.isoformat().replace('+00:00', 'Z'), free_end.isoformat().replace('+00:00', 'Z')]
        return free_slot

    i = 0
    while free_start < pos_interval_end:
        if i >= len(busy_list):
            return free_slot
        elif free_start >= busy_list[i].start:
            free_start = busy_list[i].end
            i += 1
        elif free_start + duration_min <= busy_list[i].start:
            free_end = free_start + duration_min
            free_slot = [free_start.isoformat().replace('+00:00', 'Z'), free_end.isoformat().replace('+00:00', 'Z')]
            return free_slot
    return free_slot


def add_event_to_calendar(service, event_name, free_slot):
    """Adds an event with event_name, that starts at free_slot[0]
    and ends at free_slot[1] to the Google calendar."""
    event = {
        'summary': event_name,
        'start': {
            'dateTime': free_slot[0],
        },
        'end': {
            'dateTime': free_slot[1],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Get text input from user.
    user_input = input("What would you like to schedule this week?\n ")

    # Parse text input from user through GPT-3 model.
    json_file = get_gpt_response(user_input)
    # print(json.dumps(json_file, indent=4))

    try:
        service = build('calendar', 'v3', credentials=creds)

        no_free_slot_names = []
        found_urls = []

        for event in json_file['events']:
            free_slot_found = False

            for posInterval in event['possibleIntervals']:
                pos_interval_start = convert_date_time_to_utc(posInterval['date'], posInterval['timePeriod']['startTime'])
                pos_interval_end = convert_date_time_to_utc(posInterval['date'], posInterval['timePeriod']['endTime'])
                free_slot = find_free_slot(service, event['duration'], pos_interval_start, pos_interval_end)
                if free_slot[0] != -1:
                    free_slot_found = True
                    found_urls.append(add_event_to_calendar(service, event['eventName'], free_slot))

            if not free_slot_found:
                no_free_slot_names.append(event['eventName'])

        for url in found_urls:
            print("Event created: %s" % url)
        for not_found_event in no_free_slot_names:
            print("Sorry, I couldn't add " + not_found_event + " to your calendar because of conflicts")

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
