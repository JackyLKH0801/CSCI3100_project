from django.contrib import admin
from django.urls import path

from .views import (
    tweet_detailed_view,
    tweet_list_view,
    tweet_feed_view,
    tweet_create_view, 
    tweet_delete_view,
    tweet_action_view,
)

urlpatterns = [
    path('', tweet_list_view),
    path('feed/', tweet_feed_view),
    path('create/', tweet_create_view),
    path('action/', tweet_action_view),
    path('<int:tweet_id>/', tweet_detailed_view),
    path('<int:tweet_id>/delete/', tweet_delete_view),   
]
