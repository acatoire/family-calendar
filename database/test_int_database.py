"""Test cases for Firestore DAOs using real connections."""

import unittest
from database import FirestoreDAO

COLLECTION_NAME = "update"
DOC_NAME = 'template'


class TestFirestoreDAORealConnection(unittest.TestCase):
    """Tests for Firestore DAOs using real connections."""

    @classmethod
    def setUpClass(cls):
        """Set up the class by instantiating the DAO object."""
        cls.dao = FirestoreDAO()

    @classmethod
    def tearDownClass(cls):
        """Clean up resources used during testing."""

    def setUp(self):
        """Create collections needed for individual tests."""

    def tearDown(self):
        """Delete collections used during individual tests."""

    def test_get_document_existing(self):
        """Fetching existing document from Firestore returns correct data."""
        result = self.dao.get_document(COLLECTION_NAME, DOC_NAME)

        self.assertTrue(isinstance(result, dict), "Result should be a dictionary.")
        self.assertGreaterEqual(len(result), 1, "Dictionary should contain some keys.")

    def test_get_document_non_existent(self):
        """Fetching non-existent document from Firestore returns None."""
        non_existent_resource = "some-random-nonexistent-resource"
        result = self.dao.get_document(COLLECTION_NAME, non_existent_resource)

        self.assertIsNone(result, f"Expected {non_existent_resource} to be nonexistent.")

    # def test_create_document(self):

    # def test_update_document(self):

    # def test_delete_document(self):


if __name__ == "__main__":
    unittest.main()
