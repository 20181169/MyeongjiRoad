from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime, timedelta
from rest_framework_api_key.models import APIKey
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.serializers import MyUserSerializer
from django.http import JsonResponse
from app.models import MyUser
from rest_framework import generics
from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from apscheduler.schedulers.background import BackgroundScheduler
import time
from .weather_api import check_weather
from .fineDust_api import check_fineDust
from .models import WeatherDB, Account
from .models import fineDustDB
import requests
from .models import CultureBank
from .serializers import CultureBankSerializer
from .serializers import weather_apiSerializer
from .serializers import fineDustSerializer
from django.http import JsonResponse
import json
from django.shortcuts import redirect
from cawarock.settings import SOCIAL_OUTH_CONFIG
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.urls import reverse
import jwt
from django.shortcuts import render
from django.db.models import Q 
from .serializers import Market_DBSerializer
from .models import Market_DB
from .models import Yeouijus
import random
from .serializers import accountSerializer



def index(request):
    return HttpResponse("알렉")


class CultureBankListCreateAPIView(generics.ListCreateAPIView):
    queryset = CultureBank.objects.all()
    serializer_class = CultureBankSerializer

def get_culture_banks(request):
    if request.method == 'GET':
        culture_banks = CultureBank.objects.all()
        serializer = CultureBankSerializer(culture_banks, many=True)
        json_data = json.dumps(serializer.data, ensure_ascii=False)
        return JsonResponse(json_data, safe=False, charset='utf-8')


class saveUserInfoCreateAPIView(generics.ListCreateAPIView):
    queryset=Account.objects.all()
    serializer_class = accountSerializer

@api_view(['POST'])
def saveUserInfo(request):
    serializer = accountSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            'message': 'Data saved successfully',
        }
        return Response(response_data)
    else:
        return Response(serializer.errors, status=400)



class weather_apiListCreateAPIView(generics.ListCreateAPIView):
    queryset = WeatherDB.objects.all()
    serializer_class = weather_apiSerializer

def get_weather_api(request):
    if request.method == 'GET':
        weather_api = WeatherDB.objects.all()
        serializer = weather_apiSerializer(weather_api, many=True)
        json_data = json.dumps(serializer.data, ensure_ascii=False)
        return JsonResponse(json_data, safe=False, charset='utf-8')
    

class fineDustListCreateAPIView(generics.ListCreateAPIView):
    queryset = fineDustDB.objects.all()
    serializer_class = fineDustSerializer

def get_fineDust(request):
    if request.method == 'GET':
        fineDust = fineDustDB.objects.all()
        serializer = fineDustSerializer(fineDust, many=True)
        json_data = json.dumps(serializer.data, ensure_ascii=False)
        return JsonResponse(json_data, safe=False, charset='utf-8')




@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = MyUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'status': 'success',
                'data': 'User has been created successfully!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'data': serializer.errors
            })
    else:
        return JsonResponse({
            'status': 'error',
            'data': 'Only POST method is allowed!'
        }, status=405)

@api_view(['GET'])
#@permission_classes([HasUserAPIKey])
def get_register_info(request):
    if request.method == 'GET':
        user = request.user
        if hasattr(user, 'apikey'):
            serializer = MyUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                'status': 'error',
                'data': 'User does not have API key!'
            }, status=403)
    else:
        return JsonResponse({
            'status': 'error',
            'data': 'Only GET method is allowed!'
        }, status=405)
    
class GenerateApiKeyView(generics.CreateAPIView):
    queryset = MyUser.objects.all()

    def create(self, request, *args, **kwargs):
        userid = request.data.get('userid')
        password = request.data.get('password')
        try:
            user = MyUser.objects.get(userid=userid)
        except MyUser.DoesNotExist:
            return Response({'error': 'User not found'})
        if not user.check_password(password):
            return Response({'error': 'Invalid password'})
        
        # staff 유저만 API key 생성
        if user.is_staff:
            # 기존 API 키가 있다면 삭제
            try:
                api_key = APIKey.objects.get(name=user.email)
                api_key.delete()
            except APIKey.DoesNotExist:
                pass
            # 새로운 API 키 생성
            api_key, key = APIKey.objects.create_key(name=user.email)
            return Response({'key': key})
        else:
            return Response({'error': 'Permission denied. Staff users only.'})
        

class GetUserByCredentialsView(APIView):
    def post(self, request):
        # API key 검증
        api_key = request.META.get('HTTP_AUTHORIZATION')
        try:
            api_key = api_key.split(' ')[1]
            api_key_obj = APIKey.objects.get_from_key(api_key)
        except:
            return Response({'error': 'Invalid API key'})
        
        # 유저 정보 검증
        userid = request.data.get('userid')
        password = request.data.get('password')
        try:
            user = MyUser.objects.get(userid=userid)
        except MyUser.DoesNotExist:
            return Response({'error': 'User not found'})
        if not check_password(password, user.password):
            return Response({'error': 'Invalid password'})

        # API key와 유저 정보가 일치하는지 확인
        if isinstance(api_key_obj, User):
           
            return Response({'error': 'API key does not match user'})
        
        # 유저 정보 반환
        serializer = MyUserSerializer(user)
        return Response(serializer.data)
    

def job():
    print(f'******{time.strftime("%H:%M:%S")}******')

    data = check_weather(63, 110)
    weather, created = WeatherDB.objects.get_or_create(all)
    weather.temp = data['T1H']
    weather.humidity = data['REH']
    weather.rainType = data['PTY']
    weather.rainfall = data['RN1']
    weather.sky = data['SKY']
    weather.save()

    print(weather)

    print("************************")

def cron_weather():
    sched = BackgroundScheduler()
    # interval - 일정주기로 수행(테스트용 5초)
    sched.add_job(job, 'interval', seconds=1000, id='cron_weather')
    sched.start()

def fineDust_job():
    print(f'******{time.strftime("%H:%M:%S")}******')

    data = check_fineDust()
    fineDust, created = fineDustDB.objects.get_or_create(all)
    fineDust.dataTime = data['dataTime']
    fineDust.pm10 = data['pm10']
    fineDust.pm10Grade = data['pm10Grade']
    fineDust.pm2_5 = data['pm2_5']
    fineDust.pm2_5Grade = data['pm2_5Grade']
    fineDust.save()

    print(fineDust)

    print("************************")

def cron_fineDust():
    sched = BackgroundScheduler()
    # interval - 일정주기로 수행(테스트용 5초)
    sched.add_job(fineDust_job, 'interval', seconds=1000, id='cron_fineDust')
    sched.start()





@api_view(['GET'])
@permission_classes([AllowAny, ])
def kakaoGetLogin(request):
    CLIENT_ID = SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY']
    REDIRET_URL = SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI']
    print(CLIENT_ID)
    url = "https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={0}&redirect_uri={1}".format(
        CLIENT_ID, REDIRET_URL)
    res = redirect(url)
    #data = json.loads(res.content)
    #print(data)
    # "id" 값 추출
    #user_id = data['user_info']['id']
    print(res)
    params = {'res' : res}
    #return redirect(reverse('kakaoregister'), url=url)
    return res


"""
@api_view(['GET'])
@permission_classes([AllowAny, ])
def getUserInfo(reqeust):
    CODE = reqeust.query_params['code']
    url = "https://kauth.kakao.com/oauth/token"
    res = {
            'grant_type': 'authorization_code',
            'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
            'redirect_url': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
            'client_secret': SOCIAL_OUTH_CONFIG['KAKAO_SECRET_KEY'],
            'code': CODE
        }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    response = requests.post(url, data=res, headers=headers)
    tokenJson = response.json()
    userUrl = "https://kapi.kakao.com/v2/user/me" # 유저 정보 조회하는 uri
    auth = "Bearer "+tokenJson['access_token'] ## 'Bearer '여기에서 띄어쓰기 필수!!
    HEADER = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    #res = requests.get(userUrl, headers=HEADER)
    #return JsonResponse({"user_info":res.json()})
    kakao_response=requests.post(userUrl, headers=HEADER)
    kakao_response = json.loads(kakao_response.text)
    print(kakao_response)
    if  Account.objects.filter(social_login_id=kakao_response['id']).exists():  # 지금 접속한 카카오 아이디가 데이터베이스에 존재하는지 확인
            user_info = Account.objects.get(social_login_id=kakao_response['id'])  # 존재하는 카카오 아이디를 가진 유저 객체를 가져옴
            encoded_jwt = jwt.encode({'id': user_info.id}, 'SECRET_KEY', algorithm='HS256')  # jwt토큰 발행
            return HttpResponse(f'id:{user_info.id}, token:{encoded_jwt}, exist:true')

    # 저장되어 있지 않다면 회원가입
    else:
        Account(
            social_login_id = kakao_response['id'],
            email = kakao_response['kakao_account'].get('email', None), # 이메일 선택동의여서 없을 수도 잇음
        ).save()
        user_info = Account.objects.get(social_login_id=kakao_response['id'])
        encoded_jwt = jwt.encode({'id' : user_info.id}, 'SECRET_KEY', algorithm='HS256') #JWT 토큰 발행
        #return HttpResponse(f'id:{user_info.id}, token:{encoded_jwt}, exist:false')
        return HttpResponse(f'id:{user_info.id}, token:{encoded_jwt}, exist:false')
"""
def store_search(request):
    query = request.GET.get('query')
    if query:
        cultures = CultureBank.objects.filter(Q(name__icontains=query) | Q(phone_number__icontains=query))
    else:
        cultures = CultureBank.objects.all()

    data = {"cultures": list(cultures.values())}
    return JsonResponse(data)

class Market_DBListCreateAPIView(generics.ListCreateAPIView):
    queryset = Market_DB.objects.all()
    serializer_class = Market_DBSerializer

def get_Market_DB(request):
    if request.method == 'GET':
        market_DB = Market_DB.objects.all()
        serializer = Market_DBSerializer(market_DB, many=True)
        json_data = json.dumps(serializer.data, ensure_ascii=False)
        return JsonResponse(json_data, safe=False, charset='utf-8')
    
def my_view(request):
    if request.method == "GET":
        data = list(Yeouijus.objects.all().values())
        random_data = random.choice(data)
        json_data = json.dumps(random_data, ensure_ascii=False)
        return JsonResponse(json_data, safe=False, charset="utf-8")

def print_data():
    # HTTP GET 요청 보내기
    response = requests.get('http://localhost:8000/hongbo/yeouijus/')
    response.encoding = 'utf-8'  # 인코딩 지정
    data = response.json()
    print(data)

sched = BackgroundScheduler()

def random_repeat():
    sched.add_job(print_data, "interval", seconds=3600, id="print_data") #5초에 한번 출력
    return sched

sched=random_repeat()
sched.start()



@api_view(['GET'])
@permission_classes([AllowAny, ])
def getUserInfo(reqeust):
    CODE = reqeust.query_params['code']
    url = "https://kauth.kakao.com/oauth/token"
    res = {
            'grant_type': 'authorization_code',
            'client_id': SOCIAL_OUTH_CONFIG['KAKAO_REST_API_KEY'],
            'redirect_url': SOCIAL_OUTH_CONFIG['KAKAO_REDIRECT_URI'],
            'client_secret': SOCIAL_OUTH_CONFIG['KAKAO_SECRET_KEY'],
            'code': CODE
        }
    headers = {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    response = requests.post(url, data=res, headers=headers)
    tokenJson = response.json()
    userUrl = "https://kapi.kakao.com/v2/user/me" # 유저 정보 조회하는 uri
    auth = "Bearer "+tokenJson['access_token'] ## 'Bearer '여기에서 띄어쓰기 필수!!
    HEADER = {
        "Authorization": auth,
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    #res = requests.get(userUrl, headers=HEADER)
    #return JsonResponse({"user_info":res.json()})
    account = Account.objects.last()
    

    kakao_response=requests.post(userUrl, headers=HEADER)
    kakao_response = json.loads(kakao_response.text)
    print(kakao_response)
    # print(kakao_response['kakao_account']['gender'])
    # print(kakao_response['kakao_account']['age_range'])
    # print(account.profile_img)
    # print(account.point)
    # print(account.step)
    # print(account.nickname)
    # print(account.review)
    # print(account.picklist)


    if  Account.objects.filter(social_login_id=kakao_response['id']).exists():
        user_info = Account.objects.get(social_login_id=kakao_response['id'])
        encoded_jwt = jwt.encode({'id': user_info.id}, 'SECRET_KEY', algorithm='HS256')
        point = user_info.point
        profile_img = user_info.profile_img
        step = user_info.step
        nickname = user_info.nickname
        review = user_info.review
        picklist = user_info.picklist
        class_object = Account.objects.get(gender=kakao_response['kakao_account']['gender'], age=kakao_response['kakao_account']['age_range'], social_login_id=kakao_response['id'])

            # yeouijus = Account.objects.get(yeouijus = account.yeouijus)
       


        response = HttpResponse("", status=302)
        response['Location'] = "toonjido://mylink?"+encoded_jwt

        return response
    # 저장되어 있지 않다면 회원가입
    else:
        account = Account.objects.create(
            social_login_id=kakao_response['id'],
            email=kakao_response['kakao_account'].get('email', None),
            gender=kakao_response['kakao_account'].get('gender',None),
            age=kakao_response['kakao_account'].get('age_range', None),
        )
        user_info = account
        encoded_jwt = jwt.encode({'id': user_info.id}, 'SECRET_KEY', algorithm='HS256')

        return HttpResponse(f'id:{user_info.id}, token:{encoded_jwt}, exist:false')

def store_search(request):              # 가게 상호명 & 지번 & 섹션별 가게 검색( 섹션은 글자그대로 정확히 입력 ex) Section1 )
    query = request.GET.get('query')
    
    if query:
        cultures = Market_DB.objects.filter(Q(market_name__icontains=query) | Q(lot_number__iexact=query) | Q(section__iexact=query) | Q(keyword_common__icontains=query) | Q(keyword_detail__icontains=query))
        serializer = Market_DBSerializer(cultures, many=True)
    else:
        cultures = Market_DB.objects.all()
        serializer = Market_DBSerializer(cultures, many=True)

    json_data = json.dumps(serializer.data, ensure_ascii=False)

    data = {
        "cultures": serializer.data  # Use 'serializer.data' instead of 'list(cultures.values())'
    }
    return JsonResponse(data, safe=False)


def category_search(request):                   # 카테고리별 섹션별 가게 수 
        query = request.GET.get('query')
        if query:
            cultures = Market_DB.objects.filter(Q(category__iexact=query))
            serializer = Market_DBSerializer(cultures, many=True)
            section1_count = cultures.filter(section='Section1').count()
            section2_count = cultures.filter(section='Section2').count()
            section3_count = cultures.filter(section='Section3').count()
            section4_count = cultures.filter(section='Section4').count()
            section5_count = cultures.filter(section='Section5').count()
            section6_count = cultures.filter(section='Section6').count()
            section7_count = cultures.filter(section='Section7').count()
            section8_count = cultures.filter(section='Section8').count()
            section9_count = cultures.filter(section='Section9').count()
            section10_count = cultures.filter(section='Section10').count()
            section11_count = cultures.filter(section='Section11').count()
            section12_count = cultures.filter(section='Section12').count()
            section13_count = cultures.filter(section='Section13').count()
            section14_count = cultures.filter(section='Section14').count()
            section15_count = cultures.filter(section='Section15').count()

        else:
            cultures = Market_DB.objects.all()
            serializer = Market_DBSerializer(cultures, many=True)

            section1_count = cultures.filter(section='Section1').count()
            section2_count = cultures.filter(section='Section2').count()
            section3_count = cultures.filter(section='Section3').count()
            section4_count = cultures.filter(section='Section4').count()
            section5_count = cultures.filter(section='Section5').count()
            section6_count = cultures.filter(section='Section6').count()
            section7_count = cultures.filter(section='Section7').count()
            section8_count = cultures.filter(section='Section8').count()
            section9_count = cultures.filter(section='Section9').count()
            section10_count = cultures.filter(section='Section10').count()
            section11_count = cultures.filter(section='Section11').count()
            section12_count = cultures.filter(section='Section12').count()
            section13_count = cultures.filter(section='Section13').count()
            section14_count = cultures.filter(section='Section14').count()
            section15_count = cultures.filter(section='Section15').count()

        section_counts = {}
        for i in range(1, 16):
            section = f'Section{i}'
            section_counts[section] = cultures.filter(section=section).count()
        data = {
            "cultures": serializer.data,
            "section1_count": section1_count,
            "section2_count": section2_count,
            "section3_count": section3_count,
            "section4_count": section4_count,
            "section5_count": section5_count,
            "section6_count": section6_count,
            "section7_count": section7_count,
            "section8_count": section8_count,
            "section9_count": section9_count,
            "section10_count": section10_count,
            "section11_count": section11_count,
            "section12_count": section12_count,
            "section13_count": section13_count,
            "section14_count": section14_count,
            "section15_count": section15_count,
            
            "count": len(cultures)  # 검색된 결과의 개수
        }
        return JsonResponse(data)



from .serializers import Market_DBSerializer, ImagesSerializer, reviewSerializer
from app.models import Images, review


class ImagesListCreateAPIView(generics.ListCreateAPIView):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer

class reviewListCreateAPIView(generics.ListCreateAPIView):
    queryset = review.objects.all()
    serializer_class = reviewSerializer


def get_Market_DB_List(request):
    if request.method == 'GET':
        cultures = Market_DB.objects.all()
        serializer = Market_DBSerializer(cultures, many=True)
        json_data = json.dumps(serializer.data, ensure_ascii=False)

        data = {
            "cultures": serializer.data  # Use 'serializer.data' instead of 'list(cultures.values())'
        }
        return JsonResponse(data, safe=False)
