from django.urls import path
from .views import health_check
from .views import home, health_check, server_info

urlpatterns = [
    path("", home, name="home"),
    path("health/", health_check, name="health_check"),
    path("info/", server_info, name="server_info"),
]