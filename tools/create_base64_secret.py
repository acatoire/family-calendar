"""
Use this script to generate base 64 key
"""

import json
import base64


service_key = {
  # replace by the client_secret content
}

# convert json to a string
service_key = json.dumps(service_key)

# encode service key
SERVICE_ACCOUNT_KEY = base64.b64encode(service_key.encode('utf-8'))

print(SERVICE_ACCOUNT_KEY)
