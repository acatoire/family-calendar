"""
Workdays class management
To convert data to calendar events
"""
from datetime import date, datetime, time, timedelta

from gcsa.event import Event


class WorkDay:
    """
    A workday definition as find in database
    """
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
    """
    Workdays class containing all workdays actually managed
    """

    def __init__(self, type_details: dict):
        """
        Create the workdays manager
        :param type_details: dict that contains all days description
        """

        self.type_details = type_details

    def get_event(self, event_date: date, day_type: str) -> Event:
        """
        Create a valid event from given a date and type
        :param event_date: event date
        :param day_type: event type
        :return: the event
        """

        day = self.type_details.get(day_type)
        if day is None:
            raise ValueError(
                f"""The day type "{day_type}" is not known in the application. Edit the WorkDays.detail dict.""")

        # Create single or dual day event
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
            summary=day_type,
            description=f"{day.comment}",
            start=start,
            end=end,
            color_id=day.color,
            minutes_before_popup_reminder=0,
            timezone='Europe/Paris'
        )
        return new_event

    def is_off(self, event: Event) -> bool:
        """
        Say if an event from the calendar is off or not regarding its summary content
        :param event:
        :return:
        """

        day = self.type_details.get(event.summary)
        return day.is_off
