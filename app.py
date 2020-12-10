

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


class WorkDay:
    def __init__(self, name, start, end, comment, is_off=False):
        self.name = name
        self.start = start
        self.end = end
        self.comment = comment
        self.is_off = is_off
        self.color = None


class WorkDays:
    work_days = [WorkDay("J", time(8, 30), time(16, 30), "Jour"),
                 WorkDay("M", time(6, 45), time(14, 15), "Matin"),
                 WorkDay("S", time(13, 45), time(21, 15), "Soir"),
                 WorkDay("N", time(21, 0), time(7, 0), "Nuit"),
                 WorkDay("Jca", time(8, 30), time(16, 30), "Jour modifiable"),
                 WorkDay("Jrp", time(8, 30), time(16, 30), "Jour modifiable"),
                 WorkDay("TA", None, None, "Repo recup ?", True),
                 WorkDay("To", None, None, "Repo recup ?", True),
                 WorkDay("RF", None, None, "Repo récupération férier", True),
                 WorkDay("CA", None, None, "Congé Annuel", True),
                 WorkDay(".CA", None, None, "Congé Annuel ?", True),
                 WorkDay("Rc", None, None, "Récupération", True),
                 WorkDay("_", None, None, "comment", True),
                 WorkDay("", None, None, "comment", True)]

    def get_work_day(self, name):
        for day in self.work_days:
            if name == day.name:
                return day
        return None

    def get_event(self, ev_date, name, user):
        day = self.get_work_day(name)
        if not day.is_off:
            new_event = Event(
                summary=day.name,
                description="{}\n{}".format(user, day.comment),
                start=datetime.combine(ev_date, day.start),
                end=datetime.combine(ev_date, day.end),
                color=day.color,
                minutes_before_popup_reminder=0
            )
            return new_event
        return None


def main():
    # use creds to create a client to interact with the Google Drive API

    # Config
    work_days = WorkDays()

    sheet_name = "2021"
    calendar_name = 'famille.catoire.brard@gmail.com'
    users = ["Aurélie", "Aurélie"]
    looked_user = users[0]
    looked_month = 1

    my = Service(sheet_name, calendar_name)

    # Lets play
    print("Colors?")
    colors = my.calendar.list_event_colors()
    print(colors)

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
                new_event = work_days.get_event(element_date, element.get(looked_user), looked_user)
                if new_event:
                    print("{} - {}".format(element.get("Date"), element.get(looked_user)))
                    my.calendar.add_event(new_event)

    print("Event list")
    for event in my.calendar:
        # TODO count events
        print("{}".format(event))


main()
