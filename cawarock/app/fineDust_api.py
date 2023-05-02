from urllib.parse import urlencode, quote_plus, unquote
import requests # HTTP 요청을 보내는 모듈
import datetime # 날짜시간 모듈
import json
from datetime import date, datetime, timedelta

def check_fineDust():

    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
    key = '1IhghHgJ2H1GObn8T8iTTzXd+Ez8LnCk/ZzXiMLdYi9+5lRG9+37x94zeihhhLV6HRIdag0Wnsyf9z971ztAbg=='
    params ={'serviceKey' : key, 'returnType' : 'json', 'numOfRows' : '100', 'pageNo' : '1', 'sidoName' : '충남', 'ver' : '1.0' }

    response = requests.get(url, params=params)
    res_json = json.loads(response.content)
    items = res_json["response"]["body"]["items"]


   

    ## pm10 =>미세먼지
    ## pm2_5 =>초미세먼지
    ## pm10Grade => 미세먼지 수준
    ## pm2_5Grade => 미세먼지 수준
    ## dataTime => 측정 시간


    fineDust_data = {'dataTime': 0,'pm10': 0, 'pm10Grade': 0, 'pm2_5': 0, 'pm2_5Grade': 0 }

    for i in items:
        if i['stationName'] == '신방동':
            
            fineDust_data['dataTime']=i['dataTime']
            fineDust_data['pm10']=int(i['pm10Value'])
            fineDust_data['pm2_5']=int(i['pm25Value'])
            
            #미세먼지 기준치
            if int(i['pm10Value']) <= 30:
                fineDust_data['pm10Grade']= '좋음'
            elif int(i['pm10Value']) <= 80:
                fineDust_data['pm10Grade']= '보통'
            elif int(i['pm10Value']) <= 150:
                fineDust_data['pm10Grade']= '나쁨'
            else :
                fineDust_data['pm10Grade']= '매우나쁨'
                
            #초미세먼지 기준치
            if int(i['pm25Value']) <= 15:
                fineDust_data['pm2_5Grade']= '좋음'
            elif int(i['pm25Value']) <= 35:
                fineDust_data['pm2_5Grade']= '보통'
            elif int(i['pm25Value']) <= 75:
                fineDust_data['pm2_5Grade']= '나쁨'
            else :
                fineDust_data['pm2_5Grade']= '매우나쁨'

    print("response: ", fineDust_data)
    
    return fineDust_data