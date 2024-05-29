import requests
from twilio.rest import Client
import os

KEY = os.environ.get("KEY")
MG_LAT = -27.536810
MG_LON = 153.077957
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")


def send_message(msg: str):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=msg,
        from_='+18436066048',
        to='+61414531124'
    )
    print(message.status)


parameters = {
    "lat": MG_LAT,
    "lon": MG_LON,
    "appid": KEY,
    "cnt": 4,
}
response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
weather_data = response.json()
sky = [weather_data["list"][n]["weather"][0]["id"] for n in range(0, 4)]
rain = False
clear = False
cloudy = False
for condition in sky:
    if condition < 700:
        rain = True

if rain:
    send_message('🌧️ Ame ga furu kamoshirenai kara, kasa wo motte ikinasai ☔')


