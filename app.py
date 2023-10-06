
"""
Family calendar app

Help from:
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
https://stackoverflow.com/a/64509140/14219576
https://github.com/kuzmoyev/google-calendar-simple-api
"""
import sys
from copy import copy
from datetime import date, datetime, time, timedelta
from time import sleep
from sys import argv

from googleapiclient.errors import HttpError
from google.oauth2 import service_account

import gspread
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event

try:
    from client_secret_local import keyfile_dict_local
    print("Local secrets found.")
except ModuleNotFoundError:
    print("No local secrets found.")

try:
    from client_secret_env import keyfile_dict_env
    print("Found ENV secrets.")
except AttributeError:
    print("No ENV secrets found.")

# TODO #2 use logging


class Service:  # pylint: disable=too-many-instance-attributes
    def __init__(self, year: str, month: int, user: str):
        """

        :param year:
        :param month: The month to read or 0 for the full year
        :param user: THe user to read
        """
        self.use_local = False
        self.keyfile_dict = None

        self._calendar = None
        self._gspread_client = None

        self.looked_month = month
        self.looked_user = user
        self.calendar_id = ''
        self.work_days = WorkDays()
        self.event_list = []

        self.last_update = 'unknown'

        # Get config secrets (keyfile)
        try:
            # Priority to ENV secrets
            self.keyfile_dict = keyfile_dict_env
            print("Use ENV secrets.")
        except NameError:
            self.keyfile_dict = keyfile_dict_local
            print("Use Local secrets.")
            self.use_local = True

        secret_error_message = """ERROR: client_secret is not defined.
            - On local execution you need to create client_secret_local.py to store google auth secret.
            - On CI you need to replace secrets stored in client_secret_env.py"""

        # Get database content
        try:
            self._gspread_client = gspread.service_account_from_dict(self.keyfile_dict)

        except ValueError as exception:
            print(secret_error_message)
            print(exception)
            sys.exit()

        # TODO #4 spread sheet is user dependent
        # Get the database (spreadsheet)
        self.sheet_obj = self._gspread_client.open(year).get_worksheet(0)

        # TODO #5 validate spreadsheet format/content
        self._search_calendar_id()
        self.init_event_list_from_database()

        # Connect to calendar
        try:
            self._calendar = GoogleCalendar(
                self.calendar_id,
                credentials=service_account.Credentials.from_service_account_info(self.keyfile_dict))

        except ValueError as exception:
            print(secret_error_message)
            print(exception)
            sys.exit()

    def need_update(self) -> bool:
        # Check update time
        self.last_update = self.sheet_obj.spreadsheet.get_lastUpdateTime()
        calendar_update = "not detected"  # TODO finish later #11 to manage last edition date
        print(f"Last database change: {self.last_update}")
        print(f"Last calendar update: {calendar_update}")

        return self.last_update != calendar_update

    def delete_events(self, year: int, month: int):
        print("Delete old events")
        # TODO #6 Delete only needed ones
        start_month, end_month, end_year = calculate_dates(year, month)
        print(f"The app will delete events from 01/{start_month}/{year} to 01/{end_month}/{end_year}")

        event_list = self._calendar.get_events(time_min=datetime(year, start_month, 1),
                                               time_max=datetime(end_year, end_month, 1))
        for event in event_list:
            if event.creator:
                if event.creator.email == self.keyfile_dict.get('client_email'):
                    try:
                        print(f"Delete : {event}")
                        self._calendar.delete_event(event)
                    except HttpError:
                        # Manage 403 error: Rate limit exceeded
                        print("Http error, wait before retry")
                        sleep(5)
                        print(f"Delete : {event}")
                        self._calendar.delete_event(event)

    def print_events(self):
        print("Event list")
        for event in self._calendar:
            # TODO count events
            # TODO use month
            print(event)

    def save_user_days(self):

        # Merge continues day off events
        i = 0
        while (i < len(self.event_list)) and (i < len(self.event_list) - 1):
            if self.work_days.is_off(self.event_list[i]) and self.work_days.is_off(self.event_list[i + 1]):
                self.event_list[i] = add_events(self.event_list[i], self.event_list.pop(i + 1))
            else:
                i += 1

        for event in self.event_list:
            # Add edition datetime to description
            event.description = f"{event.description}\n\nLast update: {datetime.now()}"
            if event:
                try:
                    print(f"{event.start} - {event.summary}")
                    self._calendar.add_event(event)
                except HttpError:
                    # Manage 403 error: Rate limit exceeded
                    print("Http error, wait before retry")
                    sleep(5)
                    print(f"{event.start} - {event.summary}")
                    self._calendar.add_event(event)

    def _search_calendar_id(self):
        """
        Initialize the calendar id from database
        :return:
        """
        print("Get calendars from database (spreadsheet)")

        sheet_dict = self.sheet_obj.get_all_records()

        for element in sheet_dict:
            if element.get('Type') == 'Calendar':
                # Get the calendar id
                self.calendar_id = element.get(self.looked_user)
                # Clean return char from data
                self.calendar_id = self.calendar_id.replace("\r", "").replace("\n", "")
                return  # calendar found, done!

        # calendar not found, raise!
        raise FileNotFoundError(f"Calendar id not found for user {self.looked_user}")

    def init_event_list_from_database(self):
        """
        Initialize the event_list content from database
        :return:
        """
        print("Get events from database (spreadsheet)")
        sheet_dict = self.sheet_obj.get_all_records()

        for element in sheet_dict:

            if element.get("Date") != "":  # Event line has a non empty date column value.
                element_date = date.fromisoformat(element.get("Date").replace("/", "-"))

                if self.looked_month:
                    # Update only month
                    if element_date.month == self.looked_month:
                        new_event = self.work_days.get_event(element_date, element.get(self.looked_user))
                        self.event_list.append(new_event)
                else:
                    # Update the whole year
                    new_event = self.work_days.get_event(element_date, element.get(self.looked_user))
                    self.event_list.append(new_event)


def add_events(event_1: Event, event_2: Event):

    work_days = WorkDays()
    new_event = copy(event_1)

    if work_days.is_off(event_1) and work_days.is_off(event_2):

        if event_1.summary == "OFF":
            # Already a merged day
            new_event.description = f"{event_1.description}\n{event_2.start}-{event_2.description}"
        else:
            # First merge
            new_event.summary = "OFF"
            new_event.description = f"{event_1.start}-{event_1.description}\n{event_2.start}-{event_2.description}"
        new_event.start = event_1.start
        new_event.end = event_2.end + timedelta(days=1)
        new_event.color_id = event_1.color_id

        return new_event

    raise NotImplementedError("You can't add days that are not day off together.")


class WorkDay:
    def __init__(self,
                 start: time or None,
                 end: time or None,
                 comment: str,
                 is_off: bool = False,
                 color: int = None):

        # TODO #10 add color validation (with test)

        self.start = start
        self.end = end
        self.comment = comment
        self.is_off = is_off
        self.color = color


class WorkDays:
    # TODO #7 get them from dedicated sheet
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

    def get_event(self, event_date: date, name: str) -> Event:
        """
        Create a valid event from given a date and type
        :param event_date: event date
        :param name: event type
        :return: the event
        """

        day = self.detail.get(name)
        if day is None:
            raise ValueError(
                f"""The day type "{name}" is not known in the application. Edit the WorkDays.detail dict.""")

        # Create timed or a one-day event
        if day.start and day.end:
            if day.start < day.end:
                # Normal day timing
                start = datetime.combine(event_date, day.start)
                end = datetime.combine(event_date, day.end)
            else:
                # Work during night
                start = datetime.combine(event_date, day.start)
                end = datetime.combine(event_date + timedelta(days=1), day.end)
        else:
            start = event_date
            end = event_date

        new_event = Event(
            summary=name,
            description=f"{day.comment}",
            start=start,
            end=end,
            color=day.color,
            minutes_before_popup_reminder=0
        )
        return new_event

    def is_off(self, event):

        day = self.detail.get(event.summary)
        return day.is_off


def calculate_dates(year: int, month: int):
    end_year = year
    if month:
        start_month = month
        if month == 12:
            end_month = 1
            end_year = year + 1
        else:
            end_month = month + 1
    else:
        start_month = 1
        end_month = 1
        end_year = year + 1
    return start_month, end_month, end_year


def wait_before_continue(active: bool):
    if active:
        input("Continue?")


def main():

    year = None
    month = None
    user = None
    # config from parameters
    try:
        year = int(argv[1])
        month = int(argv[2])
        user = argv[3]
    except IndexError:
        # Parameters are optionals
        pass

    # Load default values
    if (year or month or user) is None:
        print("Use default time config")
        year = datetime.now().year
        # month = datetime.now().month
        month = 1
        user = 'Aurore'  # Supported values are ['Aurélie', 'Axel', 'Aurore']

    sheet_name = f"{year}"

    print(f"Work on {user} calendar with year {year} and month {month}")
    calendar_service = Service(sheet_name,
                               month,
                               user)

    # For debug
    # print("Colors?")
    # colors = my.calendar.list_event_colors()
    # print(colors)

    if calendar_service.need_update():

        wait_before_continue(calendar_service.use_local)
        calendar_service.delete_events(year, month)

        wait_before_continue(calendar_service.use_local)
        calendar_service.save_user_days()

        wait_before_continue(calendar_service.use_local)
        calendar_service.print_events()

    else:
        print(f"No need to update since {calendar_service.last_update}")


if __name__ == '__main__':
    main()
