import requests

url = 'http://localhost:8000/hongbo/generate_key/'
# 요청에 필요한 데이터
data = {
    'userid': 'king8875',
    'password': 'King8875!!'
}

# POST 요청 보내기
response = requests.post(url, data=data)

# 응답 결과 확인
if response.status_code == 200:
    api_key = response.json().get('key')
    print(f'생성된 API key는 {api_key}입니다.')
else:
    print(f'에러 발생: {response.status_code}')