from urllib.parse import urlencode, quote_plus, unquote
import requests
from datetime import datetime, time, timedelta
import json

def check_temperature():
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst"

    serviceKey = "vWY0oDGQnKqDmE3eotKVv9vhUfkM2I/tMleRRYrC0/G4I+LqwB9lg2oqSa0oZHP9ziTI907PlaUQnKPMaQCJ0g=="
    serviceKeyDecoded = unquote(serviceKey, 'UTF-8')

    reference_times = [
        time(2, 10),
        time(5, 10),
        time(8, 10),
        time(11, 10),
        time(14, 10),
        time(17, 10),
        time(20, 10),
        time(23, 10)
    ]

    current_datetime = datetime.now()

    if current_datetime.time() < reference_times[0]:
        standard_day = current_datetime.date() - timedelta(days=1)
    else:
        standard_day = current_datetime.date()

    standard_time = None
    for ref_time in reference_times:
        if current_datetime.time() < ref_time:
            standard_time = reference_times[reference_times.index(ref_time) - 1]
            break
    else:
        standard_time = reference_times[-1]

    print("기준 날짜:", standard_day)
    #print("기준 시간:", standard_time)

    base_date = standard_day.strftime("%Y%m%d")
    base_time = standard_time.strftime("%H%M")

    queryParams = '?' + urlencode({quote_plus('serviceKey'): serviceKeyDecoded, quote_plus('base_date'): base_date,
                                   quote_plus('base_time'): '0200', quote_plus('nx'): 63, quote_plus('ny'): 110,
                                   quote_plus('dataType'): 'json', quote_plus('numOfRows'): '2000',
                                   quote_plus('numOfNo'): '1'})
    res = requests.get(url + queryParams, verify=False)
    data = res.json()
    
    if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
        items = data['response']['body']['items']
        
        sky = {}
        high = {}
        

        for item in items['item']:
            fcstDate =  item['fcstDate']
            fcstTime = item['fcstTime']
            category = item['category']
            fcstValue = item['fcstValue']
            
            if fcstDate not in sky:
                sky[fcstDate] = {}
            if fcstTime not in sky[fcstDate]:
                sky[fcstDate][fcstTime] = {}

                
            if fcstDate not in high:
                high[fcstDate] = {}
            
            
            #하늘상태: 맑음(1) 구름많은(3) 흐림(4)
            if category == 'SKY':
                if fcstTime == '1200':
                    sky[fcstDate][fcstTime][category] = fcstValue
            if category == 'PTY':
                if fcstTime == '1200':
                    sky[fcstDate][fcstTime][category] = fcstValue
                

            
                    
                

            if category == 'TMN':
                high[fcstDate][category] = fcstValue
            if category == 'TMX':
                high[fcstDate][category] = fcstValue
                
                
                
                
        result = []
        for date in sorted(sky.keys())[:3]:
            daily_result = {"date": date}
            daily_result.update(sky[date]['1200'])
            if date in high:
                daily_result["TMN"] = high[date].get('TMN')
                daily_result["TMX"] = high[date].get('TMX')
            result.append(daily_result)

        data = {
            "weather_data": json.dumps(result)
        }

    else:
        print("API 응답 데이터에 필요한 키가 존재하지 않습니다.")
    return(data)
