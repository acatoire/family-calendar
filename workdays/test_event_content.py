"""
Test date usage
"""

import unittest
from datetime import time

from .workdays import WorkDay


class TestEventUsage(unittest.TestCase):
    """
    This class tests the creatiuon of events in the WorkDay class.
    """
    def test_event_creation(self):
        """
        This method tests the creation of an event in the WorkDay class.
        It checks if the start time, end time, comment, off status, and color of the event are correctly set.
        """

        test_day = WorkDay(start=time(1),
                           end=time(10),
                           comment="comment content",
                           is_off=False,
                           color=1)

        self.assertEqual(time(1), test_day.start)
        self.assertEqual(time(10), test_day.end)
        self.assertEqual("comment content", test_day.comment)
        self.assertEqual(False, test_day.is_off)
        self.assertEqual(1, test_day.color)


if __name__ == '__main__':
    unittest.main()
