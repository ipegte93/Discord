#ipegte93의 봇으로 테스트됨
#시발 포기함 이거 안됨
#답은 이거임 https://discord.com/developers/docs/topics/gateway#gateways

import requests

CLIENT_ID = "889476456470687754"
CLIENT_SECRET = "i7_M5Mxn1mPC0L9IRtdq3S037e11vhJT"

url = "https://discord.com/api/v9/oauth2/authorize"
data = {
    "client": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}

response1 = requests.post(url=url, data=data).text
response2 = requests.get(url=url, params=data).text

print("respond1: "+response1)
print("respond2: "+response2)

print(data)