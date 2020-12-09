

"""
Family calendar app

Tuto from: https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html
"""
from datetime import date

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# use creds to create a client to interact with the Google Drive API
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet = client.open("2021").sheet1

# Extract and print all of the values
list_of_hashes = sheet.get_all_records()


users = ["Aurélie", "Aurélie"]

looked_user = users[0]
looked_month = 1
looked_day = 1

for element in list_of_hashes:
    if element.get("Date") != "":
        element_date = date.fromisoformat(element.get("Date").replace("/", "-"))
        if element_date.month == looked_month:
            if element_date.day == looked_day:
                print("{} - {}".format(element.get("Date"), element.get(looked_user)))
