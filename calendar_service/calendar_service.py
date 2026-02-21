"""
Calendar class management
"""

import sys
from copy import copy
from datetime import date, datetime, timedelta
from time import sleep

from googleapiclient.errors import HttpError
from google.oauth2 import service_account

import gspread
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from days_types.chu_nantes import chu_days_types
from workdays.workdays import WorkDays

try:
    from client_secret_local import keyfile_dict_local
    print("Local secrets found.")
except ModuleNotFoundError:
    print("No local secrets found.")

try:
    from client_secret_env import keyfile_dict_env  # facultative file, pylint: disable=import-error
    print("Found ENV secrets.")
except AttributeError:
    print("No ENV secrets found.")


class Service:  # pylint: disable=too-many-instance-attributes
    def __init__(self,
                 year: str,
                 month: int,
                 user: str):
        """

        :param year:
        :param month: The month to read or 0 for the full year
        :param user: The user to read
        """
        self.use_local = False
        self.keyfile_dict = None

        self._calendar = None
        self._gspread_client = None

        self.looked_month = month
        self.looked_user = user
        self.calendar_id = ''
        self.work_days = WorkDays(chu_days_types)
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
        self.sheet_obj = self._gspread_client.open(f"CHU_{year}").worksheet(self.looked_user)

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
        # TODO #17 Add the possibility to delete only starting on current month.
        # TODO #6 Delete only needed ones.
        start_month, end_month, end_year = calculate_dates(year, month)
        print(f"The app will delete events from 01/{start_month}/{year} to 01/{end_month}/{end_year}")
        print(f"In calendar: {self.calendar_id} for user: {self.looked_user}")

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
                        sleep(10)
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


def add_events(event_1: Event, event_2: Event):

    work_days = WorkDays(chu_days_types)
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
