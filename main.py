from __future__ import print_function

import asyncio
import datetime
import json
import openai
import os.path
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def gen_prompt(user_input):
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
        messages=[{"role": "user", "content": gen_prompt(user_input)}],
    )

    # print(response["choices"][0]["message"])
    # json_response = json.loads(response["choices"][0]["message"]["content"])
    # return json_response
    return json.loads(response.choices[0].message.content)


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
    user_input = input("What would you like to schedule this week? ")

    # Parse text input from user through GPT-3 model.
    json_file = get_gpt_response(user_input)
    # print(json_file)
    print(json.dumps(json_file, indent=4))

    # try:
    #     service = build('calendar', 'v3', credentials=creds)
    #
    #     # Call the Calendar API
    #     now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    #     print('Getting the upcoming 10 events')
    #     events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                           maxResults=10, singleEvents=True,
    #                                           orderBy='startTime').execute()
    #     events = events_result.get('items', [])
    #
    #     if not events:
    #         print('No upcoming events found.')
    #         return
    #
    #     # Prints the start and name of the next 10 events
    #     for event in events:
    #         start = event['start'].get('dateTime', event['start'].get('date'))
    #         print(start, event['summary'])
    #
    # except HttpError as error:
    #     print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()
