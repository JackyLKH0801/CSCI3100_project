from django.contrib import admin
from django.urls import path

from .views import (
    profile_detail_api_view
)

'''
CLIENT
Base Endpoint /api/profiles/
'''
urlpatterns = [
    path('<str:username>', profile_detail_api_view),   
    path('<str:username>/follow', profile_detail_api_view),   
]
