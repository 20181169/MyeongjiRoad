from django.urls import path
from django.urls.conf import include
from django.contrib import admin
from . import views
from .views import CultureBankListCreateAPIView
from .views import weather_apiListCreateAPIView
from .views import fineDustListCreateAPIView
from .views import Market_DBListCreateAPIView
from .views import Market_DBListCreateAPIView, ImagesListCreateAPIView
from django.conf import settings
from django.conf.urls.static import static
from app.views import update_find_number

urlpatterns = [
    path('', views.index),
    path('register/', views.register, name='register'),
    path('get_register_info/', views.GetUserByCredentialsView.as_view(), name='get_register_info'),
    path('generate_key/', views.GenerateApiKeyView.as_view(), name='generate_key'),
    path('accounts/kakao/login/callback/', views.getUserInfo, name='getUserInfo'),
    path('kakaoGetLogin/', views.kakaoGetLogin, name='kakaoGetLogin'),
    path('account/', include('allauth.urls')),
    path('culturebanks/', CultureBankListCreateAPIView.as_view(), name='culturebank_list_create'),
    path('get_culture_banks/', views.get_culture_banks, name='get_culture_banks'),
    path('get_weather_api/', views.get_weather_api, name='get_weather_api'),
    path('get_fineDust/', views.get_fineDust, name='get_fineDust'),
    path('search/', views.store_search, name='search'),
    path('Market_DB/', Market_DBListCreateAPIView.as_view(), name='Market_DB_list_create'),
    path('get_Market_DB/', views.get_Market_DB, name='get_Market_DB'),
    path('yeouijus/', views.my_view, name='yeouijus'),
    path('category_search/', views.category_search, name='search'),
    path('update-find-number/', update_find_number, name='update_find_number'),
    path('get_Market_DB_List/', views.get_Market_DB_List, name='get_Market_DB_List'),
    #path('save_user_info/', views.saveUserInfoCreateAPIView.as_view(), name='save_user_info'),
    path('create_favorite/', views.create_favorite, name='create_favorite'),
    path('create_review/', views.create_review, name='create_review'),
    path('get_favorite_market_ids/', views.get_favorite_market_ids, name='get_favorite_market_ids'),
    path('get_favorite_review/', views.get_favorite_review, name='get_favorite_review'),
    path('get_review_market_ids/', views.get_review_market_ids, name='get_review_market_ids'),
    path('get_favorite_market_ids_age/', views.get_favorite_market_ids_age, name='get_favorite_market_ids_age'),
    path('get_favorite_market_ids_gender/', views.get_favorite_market_ids_gender, name='get_favorite_market_ids_gender'),
    path('delete_favorite/', views.delete_favorite, name='delete_favorite'),
    path('delete_review/', views.delete_review, name='delete_review'),
    path('save_user_info/', views.save_user_info, name='save_user_info'),
    path('get_user_profile/', views.get_user_profile, name='get_user_profile'),
    path('get_category_statistics/', views.get_category_statistics, name='get_category_statistics'),
    path('get_temperature/', views.get_temperature, name='get_temperature'),
    path('deleteAccount/', views.deleteAccount, name='deleteAccount'),
    path('apple_login/', views.apple_login, name='apple_login'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
