

"""
Family calendar app

Help from:
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
https://stackoverflow.com/a/64509140/14219576
https://github.com/kuzmoyev/google-calendar-simple-api
"""
from datetime import date, datetime, time

from oauth2client.service_account import ServiceAccountCredentials  # For sheet
from google.oauth2 import service_account  # For Calendar

import gspread
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event


class Service:
    def __init__(self, year: str, calendar_name: str, key_path: str = "client_secret.json", ):

        scope = ['https://www.googleapis.com/auth/sqlservice.admin',
                 'https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive',
                 'https://www.googleapis.com/auth/calendar']

        self._year = year
        # Google sheet auth and connect
        creds = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
        self._gspread_client = gspread.authorize(creds)

        # Google calendar auth and connect
        # TODO use previous auth?
        creds2 = service_account.Credentials.from_service_account_file(key_path,
                                                                       scopes=scope)
        self.calendar = GoogleCalendar(calendar_name,
                                       credentials=creds2)

        sheet_obj = self._gspread_client.open(self._year).get_worksheet(0)
        self._sheet_dict = sheet_obj.get_all_records()

    @property
    def data(self):
        return self._sheet_dict


def main():
    # use creds to create a client to interact with the Google Drive API

    # Config
    sheet_name = "2021"
    calendar_name = 'famille.catoire.brard@gmail.com'
    users = ["Aurélie", "Aurélie"]
    looked_user = users[0]
    looked_month = 1

    my = Service(sheet_name, calendar_name)

    # Lets play
    print("Colors?")
    print(my.calendar.list_event_colors())

    print("Delete old events")
    for event in my.calendar:
        # TODO get email from json
        if event.other.get("creator").get("email") == "google@family-calendar-298110.iam.gserviceaccount.com":
            print("Delete : {}".format(event))
            my.calendar.delete_event(event)

    print("Looked event")
    for element in my.data:
        if element.get("Date") != "":
            element_date = date.fromisoformat(element.get("Date").replace("/", "-"))
            if element_date.month == looked_month:
                print("{} - {}".format(element.get("Date"), element.get(looked_user)))
                new_event = Event(
                    summary=element.get(looked_user),
                    description="Remarques\n- Parents:\n{}\n- Enfants:\n{}".format(element.get("Parents"),
                                                                                   element.get("Enfants")),
                    start=datetime.combine(element_date, time(12)),
                    end=datetime.combine(element_date, time(13)),
                    color=None,
                    minutes_before_popup_reminder=0
                )
                my.calendar.add_event(new_event)

    print("Event list")
    for event in my.calendar:
        # TODO count events
        print("{}".format(event))


main()
