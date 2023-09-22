

"""
Family calendar app

Help from:
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
https://stackoverflow.com/a/64509140/14219576
https://github.com/kuzmoyev/google-calendar-simple-api
"""
from copy import copy
from datetime import date, datetime, time, timedelta
from time import sleep

from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials  # For sheet
from google.oauth2 import service_account  # For Calendar

import gspread
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event

YEAR = 2023


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

    def delete_events(self):
        print("Delete old events")

        # TODO manage looked month
        event_list = self.calendar.get_events(time_min=datetime(YEAR, 1, 1),
                                              time_max=datetime(YEAR+1, 1, 1), )
        for event in event_list:
            if event.creator:
                # TODO get email from json
                if event.creator.email == "google@family-calendar-298110.iam.gserviceaccount.com":
                    try:
                        print("Delete : {}".format(event))
                        self.calendar.delete_event(event)
                    except HttpError:
                        # Manage 403 error: Rate limit exceeded
                        print("Http error, wait before retry")
                        sleep(5)
                        print("Delete : {}".format(event))
                        self.calendar.delete_event(event)

    def print_events(self):
        print("Event list")
        for event in self.calendar:
            # TODO count events
            print("{}".format(event))

    def save_user_days(self, looked_month, looked_user):

        work_days = WorkDays()
        event_list = []

        print("Looked event")
        for element in self.data:
            if element.get("Date") != "":
                element_date = date.fromisoformat(element.get("Date").replace("/", "-"))
                if looked_month:
                    # Update only month
                    if element_date.month == looked_month:
                        new_event = work_days.get_event(element_date, element.get(looked_user))
                        event_list.append(new_event)
                else:
                    # Update the whole year
                    new_event = work_days.get_event(element_date, element.get(looked_user))
                    event_list.append(new_event)

        # Merge continues day off events
        i = 0
        while (i < len(event_list)) and (i < len(event_list) - 1):
            if work_days.is_off(event_list[i]) and work_days.is_off(event_list[i+1]):
                event_list[i] = add_events(event_list[i], event_list.pop(i + 1))
            else:
                i += 1

        for event in event_list:
            if event:
                try:
                    print("{} - {}".format(event.start, event.summary))
                    self.calendar.add_event(event)
                except HttpError:
                    # Manage 403 error: Rate limit exceeded
                    print("Http error, wait before retry")
                    sleep(5)
                    print("{} - {}".format(event.start, event.summary))
                    self.calendar.add_event(event)


def add_events(event_1: Event, event_2: Event):

    work_days = WorkDays()
    new_event = copy(event_1)

    if work_days.is_off(event_1) and work_days.is_off(event_2):

        if event_1.summary == "OFF":
            # Already a merged day
            new_event.description = "{}\n{}-{}".format(event_1.description, event_2.start, event_2.description)
        else:
            # First merge
            new_event.summary = "OFF"
            new_event.description = "{}-{}\n{}-{}".format(event_1.start, event_1.description,
                                                          event_2.start, event_2.description)
        new_event.start = event_1.start
        new_event.end = event_2.end + timedelta(days=1)
        new_event.color_id = event_1.color_id

        return new_event

    raise NotImplementedError("You can't add days that are not day off together.")


class WorkDay:
    def __init__(self, start, end, comment, is_off=False, color=None):

        self.start = start
        self.end = end
        self.comment = comment
        self.is_off = is_off
        self.color = color


class WorkDays:
    detail = {"J": WorkDay(time(8, 30), time(16, 30), "J-Jour", color=7),
              "M": WorkDay(time(6, 45), time(14, 15), "M-Matin", color=1),
              "Mc": WorkDay(time(6, 45), time(14, 15), "Mc-Matin changeable", color=1),
              "S": WorkDay(time(13, 45), time(21, 15), "S-Soir", color=5),
              "Sc": WorkDay(time(13, 45), time(21, 15), "Sc-Soir changeables", color=5),
              "N": WorkDay(time(21, 0), time(7, 0), "N-Nuit", color=11),
              "Jca": WorkDay(time(8, 30), time(16, 30), "Jca-Jour modifiable", color=8),
              "Jrp": WorkDay(time(8, 30), time(16, 30), "Jrp-Jour modifiable", color=8),
              "TA": WorkDay(None, None, "TA-Repo rtt ?", is_off=True, color=10),
              "To": WorkDay(None, None, "To-Repo recup ?", is_off=True, color=10),
              "RF": WorkDay(None, None, "RF-Repo récupération férier", is_off=True, color=10),
              "CA": WorkDay(None, None, "CA-Congé Annuel", is_off=True, color=10),
              ".CA": WorkDay(None, None, ".CA-Congé Annuel ?", is_off=True, color=10),
              "Rc": WorkDay(None, None, "Rc-Récupération", is_off=True, color=10),
              "_": WorkDay(None, None, "_-Weekend", is_off=True, color=10),
              "": WorkDay(None, None, "Not specified", is_off=True, color=10),
              "OFF": WorkDay(None, None, "OFF-Multi day off", is_off=True, color=10),
              "EM": WorkDay(None, None, "OFF-Enfant Malade", is_off=True, color=10),
              "AM": WorkDay(None, None, "OFF-Arret Maladie", is_off=True, color=10)}

    def get_event(self, ev_date, name):

        day = self.detail.get(name)
        if day is None:
            raise ValueError(
                f"""The day type "{name}" is not known in the application. Edit the WorkDays.detail dict.""")

        # Create timed or a one day event
        if day.start and day.end:
            if day.start < day.end:
                # Normal day timing
                start = datetime.combine(ev_date, day.start)
                end = datetime.combine(ev_date, day.end)
            else:
                # Work during night
                start = datetime.combine(ev_date, day.start)
                end = datetime.combine(ev_date + timedelta(days=1), day.end)
        else:
            start = ev_date
            end = ev_date

        new_event = Event(
            summary=name,
            description="{}".format(day.comment),
            start=start,
            end=end,
            color=day.color,
            minutes_before_popup_reminder=0
        )
        return new_event

    def is_off(self, event):

        day = self.detail.get(event.summary)
        return day.is_off


def main():

    sheet_name = f"{YEAR}"
    calendar_name = 'famille.catoire.brard@gmail.com'
    users = ["Aurélie", "Axel"]
    looked_user = users[0]
    looked_month = 0

    my = Service(sheet_name, calendar_name)

    # For debug
    # print("Colors?")
    # colors = my.calendar.list_event_colors()
    # print(colors)

    my.delete_events()
    input("Continue?")
    my.save_user_days(looked_month, looked_user)
    input("Continue?")
    my.print_events()


main()
