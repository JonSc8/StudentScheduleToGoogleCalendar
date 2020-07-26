from __future__ import print_function
import os
import datetime
import pickle
import os.path
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarAPI:

    def __init__(self):
        super().__init__()

    def authorize_calendar(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        print("Authorizing google calendar access")
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('calendar', 'v3', credentials=creds)

        return service
    
    def add_event(self, service, course, calendar_id):
        print("Adding google calendar event")
        event = {
            'summary': course.get_name(),
            'location': course.get_location(),
            'description': course.get_further_details(),
            'start': {
                'dateTime': course.get_start_date_time(),
                'timeZone': 'America/New_York',
            },
            'end': {
                'dateTime': course.get_end_date_time(),
                'timeZone': 'America/New_York',
            },
            'recurrence': [
                'RRULE:FREQ=WEEKLY;BYDAY={};UNTIL={}'.format(course.get_week_days(), course.get_course_end_date())
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 15},
                ],
            },
        }

        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    
    # return upcoming num_events
    def get_upcoming_events(self, service, num_events):
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming {} events'.format(num_events))
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=num_events, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    
    def create_secondary_calendar(self, service, calendar_name):
        calendar = {
            'summary': calendar_name,
            'timeZone': 'America/New_York'
        }

        created_calendar = service.calendars().insert(body=calendar).execute()
        if created_calendar['summary'] == calendar_name:
            print("Successfuly created secondary calendar")
        else:
            print("Could not create secondary calendar")
        
        return created_calendar["id"]
    
    def check_calendar_exists(self, service, calendar_name):
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if calendar_list_entry['summary'] == calendar_name:
                    return calendar_list_entry["id"]
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        
        return None