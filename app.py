
"""
Family calendar app

Help from:
https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
https://stackoverflow.com/a/64509140/14219576
https://github.com/kuzmoyev/google-calendar-simple-api
"""

from datetime import datetime
from sys import argv
from calendar_service.calendar_service import Service

# TODO #2 use logging


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
