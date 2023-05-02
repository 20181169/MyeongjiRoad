import requests

# API key와 함께 유저 정보 요청
url = "http://localhost:8000/hongbo/get_register_info/"
headers = {
    "Authorization": "a0Zt0hMV.5nrptQvKbY1MobRSiAr9mR4WxOwW44LY"
}
data = {
    "userid": "king8875",
    "password": "King8875!!"
}
response = requests.post(url, headers=headers, data=data)

# 응답 출력
print(response.json())