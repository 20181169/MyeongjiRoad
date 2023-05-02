from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
    def ready(self):
        from .models import WeatherDB
        from .views import cron_weather
        from .models import fineDustDB
        from .views import cron_fineDust
        cron_weather()
        cron_fineDust()