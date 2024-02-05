"""Google Cloud Firestore Database Access Object (DAO) module.

Provides classes for reading and writing data to Google Cloud Firestore databases. This implementation utilizes the
official `google-cloud-firestore` library, allowing easy integration into Google Cloud Platform projects.

Example usage:
    >>> from database import FirestoreDAO
    >>> dao = FirestoreDAO('my-project-id')
    >>> user_doc = dao.get_document('users', 'user123')
    >>> print(user_doc)
    {'username': 'john_doe', 'email': '[johndoe@example.com](mailto:johndoe@example.com)', ...}
"""

import json
import base64
from os import getenv

from google.cloud import firestore
from google.oauth2 import service_account
from google.auth.exceptions import DefaultCredentialsError


class FirestoreDAO():
    def __init__(self):
        """Initialize the Firestore DAO object.

        """
        try:
            # Use the default credentials from your env
            # to have it on your dev env execute > gcloud auth application-default login
            self._database_content = firestore.Client(project="family-calendar-298110")
        except DefaultCredentialsError:
            # Provide credentials from base64 env variable if default one is falling
            # tutorial from:
            # https://stackoverflow.com/questions/73965176/authenticating-firebase-connection-in-github-action
            encoded_key = getenv("SERVICE_ACCOUNT_KEY")
            # decode
            service_account_json = json.loads(base64.b64decode(encoded_key).decode('utf-8'))
            google_creds = service_account.Credentials.from_service_account_info(service_account_json)
            # firebase_admin.initialize_app(cred)
            self._database_content = firestore.Client(project="family-calendar-298110",
                                                      credentials=google_creds)

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
