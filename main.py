# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.


import requests
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

import os
from dotenv import load_dotenv
load_dotenv()
ACCOUNT_SID = str(os.getenv("ACCOUNT_SID"))
AUTH_TOKEN = str(os.getenv("AUTH_TOKEN"))

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
APIKEY = "55eb1e68f4406b845475807e659159c5"

#London: lat 51.507351, lon -0.127758
#Bristol: lat 51.455311, lon -2.591900
WEATHER_PARAMS = {
    "lat": 51.455311,
    "lon": -2.591900,
    "cnt": 4,
    "appid": APIKEY
}

response = requests.get(OWM_Endpoint, params=WEATHER_PARAMS)
response.raise_for_status()

weather_data = response.json()

will_rain = False
for current_dict in weather_data["list"]:
    condition_id = current_dict["weather"][0]["id"]
    if int(condition_id) < 700:
        will_rain = True
if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    try:
        message = client.messages.create(
            body="sms_account_alerts",
            from_="+447460077297",
            to="+447756913612"
        )
        print(message.status)
    except TwilioRestException as exc:
        print(f"Twilio SMS send failed: {exc}")
