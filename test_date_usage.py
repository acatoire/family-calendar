"""
Test date usage
"""

import unittest

from app import calculate_dates


class TestDateUsage(unittest.TestCase):
    def test_single_month(self):

        (start_month, end_month, end_year) = calculate_dates(2023, 1)
        self.assertEqual(1, start_month)
        self.assertEqual(2, end_month)
        self.assertEqual(2023, end_year)

        (start_month, end_month, end_year) = calculate_dates(2023, 10)
        self.assertEqual(10, start_month)
        self.assertEqual(11, end_month)
        self.assertEqual(2023, end_year)

    def test_rolling_month(self):

        (start_month, end_month, end_year) = calculate_dates(2023, 12)
        self.assertEqual(12, start_month)
        self.assertEqual(1, end_month)
        self.assertEqual(2024, end_year)

    def test_full_year(self):

        (start_month, end_month, end_year) = calculate_dates(2023, 0)
        self.assertEqual(1, start_month)
        self.assertEqual(1, end_month)
        self.assertEqual(2024, end_year)


if __name__ == '__main__':
    unittest.main()
