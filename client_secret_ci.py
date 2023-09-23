
"""
keyfile_dict file

dict with content of keyfile generated on your Google account.
This is the CI dice version, it should not be edited manually, the CI will replace needed secrets.
On local execution, copy this file into a keyfile_dict_local.py and define a keyfile_dict_local dict.
"""

keyfile_dict_ci = {
  "type": "service_account",
  "project_id": "CI_PROJECT_ID",
  "private_key_id": "CI_PRIVATE_KEY_ID",
  "private_key": "CI_PRIVATE_KEY",
  "client_email": "CI_CLIENT_EMAIL",
  "client_id": "CI_CLIENT_ID",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "CI_CLIENT_X509_CERT_URL"
}
