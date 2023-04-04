from django.urls import path
from .views import my_api

urlpatterns = [
    path('my_api/', my_api, name='my_api'),
]