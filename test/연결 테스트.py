import requests
import json

#TODO 디코 봇을 통해 메세지 정보 얻기
#TODO 디코 봇을 통해 메세지 쓰기

base_api_url = "https://discord.com/api/v9/"

get_message = "channels/862348023764746279/message/862603484171599872" #메세지 읽기용
get_info = "users/@me" #정보 읽기용

#TODO 인증 과정 거치기
#TODO 스노우플레이크에 대해 알아보기
url = base_api_url + get_info #이거 정보를 얻기 위함, 근데 인증이 안되서 작동 안함

response = requests.get(url=url);
print(response)