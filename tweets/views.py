import random

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404,JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication


ALLOWED_HOSTS = settings.ALLOWED_HOSTS

# Create your views here.
def home_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'pages/feed.html')

def tweet_list_view(request, *args, **kwargs): 
    return render(request, 'tweets/list.html')

def tweet_detail_view(request, tweet_id, *args, **kwargs): 
    return render(request, 'tweets/detail.html', context={"tweet_id": tweet_id})



