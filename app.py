

"""
Family calendar app

Help from:
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
https://stackoverflow.com/a/64509140/14219576
https://github.com/kuzmoyev/google-calendar-simple-api
"""
from datetime import date, datetime, time

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from gcsa.google_calendar import GoogleCalendar
from google.oauth2 import service_account
from gcsa.event import Event


def main():
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://www.googleapis.com/auth/sqlservice.admin',
             'https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive',
             'https://www.googleapis.com/auth/calendar']
    key_file = "client_secret.json"

    # Config
    sheet_name = "2021"
    users = ["Aurélie", "Aurélie"]
    looked_user = users[0]
    looked_month = 1
    looked_day = 1

    # Google sheet auth and connect
    creds = ServiceAccountCredentials.from_json_keyfile_name(key_file, scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    sheet_dict = sheet.get_all_records()

    # Google calendar auth and connect
    # TODO use previous auth?
    creds2 = service_account.Credentials.from_service_account_file(key_file,
                                                                   scopes=scope)
    calendar = GoogleCalendar('famille.catoire.brard@gmail.com',
                              credentials=creds2)

    # Lets play
    print("Colors?")
    print(calendar.list_event_colors())

    print("Looked event")
    for element in sheet_dict:
        if element.get("Date") != "":
            element_date = date.fromisoformat(element.get("Date").replace("/", "-"))
            if element_date.month == looked_month:
                if element_date.day == looked_day:
                    print("{} - {}".format(element.get("Date"), element.get(looked_user)))
                    create_event(calendar,
                                 datetime.combine(element_date, time(12)))

    print("Event list")
    for event in calendar:
        print("{} - {}".format(event, event.other.get("creator").get("email")))


def create_event(calendar, ev_date: datetime):
    new_event = Event(
        summary='test',
        description=None,
        start=ev_date,
        end=None,
        color=None,
        minutes_before_popup_reminder=0
    )
    calendar.add_event(new_event)


main()
