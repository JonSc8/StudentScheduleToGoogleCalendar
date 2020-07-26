import sys
from browser_helper import BrowserHelper
from schedule import Schedule
from google_calendar_api import GoogleCalendarAPI
from configuration_object import ConfigObject


def main():
    config = ConfigObject()
    username = sys.argv[1] if len(sys.argv) == 3 else config.username
    password = sys.argv[2] if len(sys.argv) == 3 else config.password
    
    browser = BrowserHelper(config.url)
    browser.login(username, password)
    student_schedule = browser.get_student_schedule()
    schedule = Schedule(student_schedule)
    courses = schedule.courses

    api = GoogleCalendarAPI()
    service = api.authorize_calendar()
    calendar_name = "Columbia University"
    calendar_id = api.check_calendar_exists(service, calendar_name)
    if calendar_id is None:
        calendar_id = api.create_secondary_calendar(service, calendar_name)
    
    for course in courses:
        api.add_event(service, course, calendar_id)


if __name__ == "__main__":
    main()