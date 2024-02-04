"""Google Cloud Firestore Database Access Object (DAO) module.

Provides classes for reading and writing data to Google Cloud Firestore databases. This implementation utilizes the
official `google-cloud-firestore` library, allowing easy integration into Google Cloud Platform projects.

Example usage:
    >>> from my_module import FirestoreDAO
    >>> dao = FirestoreDAO('my-project-id')
    >>> user_doc = dao.get_document('users', 'user123')
    >>> print(user_doc)
    {'username': 'john_doe', 'email': '[johndoe@example.com](mailto:johndoe@example.com)', ...}
"""

from google.cloud import firestore

class FirestoreDAO():
    def __init__(self):
        """Initialize the Firestore DAO object.

        """
        self._database_content = firestore.Client(project='family-calendar-298110')

    def get_document(self, collection_name, document_id):
        """Get a single document by ID.

        Args:
            collection_name (str): Name of the collection where the document resides.
            document_id (str): Unique identifier of the document within its collection.

        Returns:
            dict or None: A dictionary representation of the document, or None if it doesn't exist.
        """
        doc_ref = self._database_content.collection(collection_name).document(document_id)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def create_document(self, collection_name, document_data):
        """Create a new document with the given data.

        Args:
            collection_name (str): Name of the collection where the document should be created.
            document_data (dict): Data to populate the new document.
        """
        doc_ref = self._database_content.collection(collection_name).document()
        doc_ref.create(document_data)

    def update_document(self, collection_name, document_id, updated_fields):
        """Update existing document fields.

        Args:
            collection_name (str): Name of the collection where the document resides.
            document_id (str): Unique identifier of the document within its collection.
            updated_fields (dict): Fields to update along with their values.
        """
        doc_ref = self._database_content.collection(collection_name).document(document_id)
        doc_ref.update(updated_fields)

    def delete_document(self, collection_name, document_id):
        """Delete a document by ID.

        Args:
            collection_name (str): Name of the collection where the document resides.
            document_id (str): Unique identifier of the document within its collection.
        """
        doc_ref = self._database_content.collection(collection_name).document(document_id)
        doc_ref.delete()
