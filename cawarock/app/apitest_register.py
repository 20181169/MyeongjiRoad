import requests

url = "http://localhost:8000/hongbo/register/"

# 회원가입에 필요한 데이터를 딕셔너리 형태로 정의합니다.
data = {
    "userid" : "king8875",
    "username" : "서경환",
    "password": "King8875!!",
    "email": "king8875@naver.com"
}

# POST 요청을 보냅니다.
response = requests.post(url, data=data)

# 응답 결과를 출력합니다.
print(response.status_code)  # 응답 상태 코드를 출력합니다.
print(response.json())       # 응답 데이터를 출력합니다.