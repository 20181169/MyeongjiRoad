import requests

# API key와 함께 유저 정보 요청
url = "http://localhost:8000/hongbo/get_register_info/"
headers = {
    "Authorization": ""
}
data = {
    "userid": "",
    "password": ""
}
response = requests.post(url, headers=headers, data=data)

# 응답 출력
print(response.json())