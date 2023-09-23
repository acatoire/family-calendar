
"""
keyfile_dict file

dict with content of keyfile generated on your Google account.
This is the CI dice version, it should not be edited manually, the CI will replace needed secrets.
On local execution, copy this file into a keyfile_dict_local.py and define a keyfile_dict_local dict.
"""

from os import getenv

keyfile_dict_env = {
  "type": "service_account",
  "project_id": getenv("CI_PROJECT_ID").replace("\\n", "\n"),
  "private_key_id": getenv("CI_PRIVATE_KEY_ID").replace("\\n", "\n"),
  "private_key": getenv("CI_PRIVATE_KEY").replace("\\n", "\n"),
  "client_email": getenv("CI_CLIENT_EMAIL").replace("\\n", "\n"),
  "client_id": getenv("CI_CLIENT_ID").replace("\\n", "\n"),
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": getenv("CI_CLIENT_X509_CERT_URL").replace("\\n", "\n"),
}
