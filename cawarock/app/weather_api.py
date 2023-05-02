from urllib.parse import urlencode, quote_plus, unquote
import requests # HTTP 요청을 보내는 모듈
import datetime # 날짜시간 모듈
from datetime import date, datetime, timedelta # 현재 날짜 외의 날짜 구하기 위한 모듈


def check_weather(nx, ny):

    url = "https://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst"

    serviceKey = "1IhghHgJ2H1GObn8T8iTTzXd+Ez8LnCk/ZzXiMLdYi9+5lRG9+37x94zeihhhLV6HRIdag0Wnsyf9z971ztAbg=="
    serviceKeyDecoded = unquote(serviceKey, 'UTF-8')

    now = datetime.now()
    today = datetime.today().strftime("%Y%m%d")
    y = date.today() - timedelta(days=1)
    yesterday = y.strftime("%Y%m%d")

    if now.minute<45: # base_time와 base_date 구하는 함수
        if now.hour==0:
            base_time = "2330"
            base_date = yesterday
        else:
            pre_hour = now.hour-1
            if pre_hour<10:
                base_time = "0" + str(pre_hour) + "30"
            else:
                base_time = str(pre_hour) + "30"
            base_date = today
    else:
        if now.hour < 10:
            base_time = "0" + str(now.hour) + "30"
        else:
            base_time = str(now.hour) + "30"
        base_date = today

    queryParams = '?' + urlencode({ quote_plus('serviceKey') : serviceKeyDecoded, quote_plus('base_date') : base_date,
                                    quote_plus('base_time') : base_time, quote_plus('nx') : 63, quote_plus('ny') : 110,
                                    quote_plus('dataType') : 'json', quote_plus('numOfRows') : '60'})

    # 값 요청 (웹 브라우저 서버에서 요청 - url주소와 )
    res = requests.get(url + queryParams, verify=False)
    items = res.json().get('response').get('body').get('items')
    #print(items)
    data = dict()
    data['date'] = base_date

    weather_data = dict()

    for item in items['item']:
        category = item['category']
        fcstValue = item['fcstValue']
        if category not in weather_data:
            # 기온
            if category == 'T1H':
                weather_data[category] = fcstValue
            # 습도
            if category == 'REH':
                weather_data[category] = fcstValue
            # 하늘상태: 맑음(1) 구름많은(3) 흐림(4)
            if category == 'SKY':
                weather_data[category] = fcstValue
             # 강우 형태: 없음(0) 비(1) 비/눈(2) 눈(3) 빗방울(5) 빗방울눈날림(6) 눈날림(7)
            if category == 'PTY':
                weather_data[category] = fcstValue
            # 1시간 동안 강수량
            if category == 'RN1':
                weather_data[category] = fcstValue

    print("response: ", weather_data)
    #print(weather_data['tmp'])
    return weather_data
