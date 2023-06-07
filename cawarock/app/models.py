from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_api_key.models import AbstractAPIKey
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_api_key.models import APIKey



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    date_joined = models.DateTimeField(default=timezone.now)
    userid = models.CharField(max_length=20, unique=True,default="")
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    # related_name 변경
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='myuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='myuser_set',
        blank=True,
    )
    
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class WeatherDB(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    temp = models.IntegerField(blank=True, null=True) #온도
    humidity = models.IntegerField(blank=True, null=True) #습도
    rainType = models.IntegerField(blank=True, null=True) #강우 형태
    rainfall = models.CharField(max_length=20, blank=True, null=True) #한시간 동안 강수량
    sky = models.IntegerField(blank=True, null=True) # 하늘 상태

    def __str__(self):
        return str(self.timestamp)
    
class fineDustDB(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    dataTime = models.CharField(max_length=20, blank=True, null=True) #측정시간
    pm10 = models.IntegerField(blank=True, null=True) #미세먼지
    pm10Grade = models.CharField(max_length=20, blank=True, null=True) #미세먼지 수준
    pm2_5 = models.IntegerField(blank=True, null=True) #초미세먼지
    pm2_5Grade = models.CharField(max_length=20, blank=True, null=True) # 초미세먼지 수준

    def __str__(self):
        return str(self.timestamp)
    
class CultureBank(models.Model):
    idx = models.IntegerField(null=True)
    name = models.CharField(max_length=50,default='some_value')
    explanation = models.CharField(max_length=1000, null=True)
    grade = models.FloatField(max_length=20,null=True)
    reivew = models.CharField(max_length=1000,null=True)
    main_item = models.CharField(max_length=50,null=True)
    market_hours = models.CharField(max_length=50,null=True)
    phone_number = models.CharField(max_length=20,null=True)
    address = models.CharField(max_length=100,null=True)
    category = models.CharField(max_length=50,null=True)
    section_number = models.IntegerField(null=True)
    market_img = models.ImageField(upload_to='images/', null=True)

    def __str__(self):
        return self.name
"""
class Account(models.Model):
    social_login_id = models.CharField(max_length=1000,null=True)
    email = models.CharField(max_length=1000,null=True)

    def __str__(self):
        return self.email 
"""

class Account(models.Model):
    social_login_id = models.CharField(max_length=1000,null=True)
    email = models.CharField(max_length=1000,null=True)
    gender = models.CharField(max_length=20, null=True)
    age = models.CharField(max_length=100 , null=True, default=0)
    nickname = models.CharField(max_length=1000,null=True, default=None)
    review = models.CharField(max_length=1000,null=True, default=None)
    profile_img = models.IntegerField(null=True, default=None)
    step = models.IntegerField(null=True, default=None)
    point = models.IntegerField(null=True, default=None)
    picklist = models.CharField(max_length=1000,null=True, default=None)
    # yeouijus = models.CharField(max_length=20,null=True)


    def __str__(self):
        return self.email


class Market_DB(models.Model):

    lot_number = models.CharField(max_length=70, null=True, blank=True) #지번
    market_name = models.CharField(max_length=100, null=True, blank=True) #상호
    cawarock = models.CharField(max_length=100, null=True, blank=True) #와락 URL
    category = models.IntegerField(null=True, blank=True) # 카테고리
    floor = models.CharField(max_length=20, null=True, blank=True) #층수
    open_check = models.CharField(max_length=50, null=True, blank=True) # 영업여부 (1 => 영업중 // 2 => 영업안함)
    #img = models.ImageField(upload_to='images/', null=True, blank=True) # 간판이미지
    keyword_common = models.CharField(max_length=1000, null=True, blank=True) # 공통키워드
    keyword_detail = models.CharField(max_length=1000, null=True, blank=True) # 공통키워드
    address = models.CharField(max_length=300, null=True, blank=True) # 주소
    phone = models.CharField(max_length=50, null=True, blank=True) # 전화번호
    open_hours = models.CharField(max_length=1000, null=True, blank=True) # 영업시간
    item = models.CharField(max_length=1000, null=True, blank=True) #메인아이템
    explain = models.CharField(max_length=2000, null=True, blank=True) # 설명
    section = models.CharField(max_length=70, null=True, blank=True) # 섹션 넘버
    #review = models.JSONField(max_length=1000, null=True, blank=True) # 리뷰
    #grade = models.JSONField(max_length=1000, null=True, blank=True) # 평점
    

    def __str__(self):
        return self.market_name



class Images(models.Model):
    
    market = models.ForeignKey(Market_DB, on_delete=models.CASCADE, related_name="img", null=True, db_column="market")
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return str(self.market)
    


class review(models.Model):
    market = models.ForeignKey(Market_DB, on_delete=models.CASCADE, related_name="review", null=True, db_column="market")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="reviews", null=True, db_column="account")
    content = models.TextField(help_text="reivew contents", blank=False, null=False) #리뷰글
    grade = models.IntegerField(null=True, blank=True) # 평점
    

    
    
class Yeouijus(models.Model):
    yeouijus = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.yeouijus 
