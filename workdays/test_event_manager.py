"""
Test date usage
"""
import datetime
import unittest
from datetime import time

from .workdays import WorkDay, WorkDays


class TestEventUsage(unittest.TestCase):

    test_day_types = {
        "T1-Normal": WorkDay(time(1, 10), time(8, 10),
                             "Test 1 normal timing", color=1),
        "T2-Normal": WorkDay(time(2, 20), time(9, 20),
                             "Test 2 normal timing", color=2),
        "T3-night": WorkDay(time(22, 30), time(8, 30),
                            "Test 3 over night timing (two days event)", color=3)
    }

    def test_event_convert_one_day(self):
        """
        Test the event creation from on day type
        Using a one-day event
        """

        day_manager = WorkDays(self.test_day_types)

        type_test = "T1-Normal"
        test_event = day_manager.get_event(datetime.date(2023, 8, 28), type_test)

        self.assertEqual(type_test, test_event.summary)
        self.assertEqual("Test 1 normal timing", test_event.description)
        self.assertEqual('Europe/Paris', test_event.timezone)
        self.assertEqual(1, test_event.color_id)
        self.assertEqual(28, test_event.start.day)
        self.assertEqual(28, test_event.end.day)

    def test_event_convert_dual_day(self):
        """
        Test the event creation from on day type
        Using a dual-day event
        """

        day_manager = WorkDays(self.test_day_types)

        type_test =  "T3-night"
        test_event = day_manager.get_event(datetime.date(2023, 8, 28), type_test)

        self.assertEqual(type_test, test_event.summary)
        self.assertEqual("Test 3 over night timing (two days event)", test_event.description)
        self.assertEqual('Europe/Paris', test_event.timezone)
        self.assertEqual(3, test_event.color_id)
        self.assertEqual(28, test_event.start.day)
        self.assertEqual(29, test_event.end.day)


if __name__ == '__main__':
    unittest.main()
