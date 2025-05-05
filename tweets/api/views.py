import random

from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404,JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from ..models import Tweet
from ..forms import TweetForm
from ..serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(['GET'])  #http method the client == POST
def tweet_detailed_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response ({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status = 200)

@api_view(['GET'])  #http method the client == POST
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username')
    if username != None:
        qs = qs.filter(user__username__iexact = username)
    serializer = TweetSerializer(qs, many = True)
    return Response(serializer.data)

def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweet_list
    }
    return JsonResponse(data)

@api_view(['POST']) #http method the client == POST
# @authentication_classes([SessionAuthentication]) #session authentication
@permission_classes([IsAuthenticated]) #only authenticated users can create tweets
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data = request.data or None)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data, status = 201)
    return Response({}, status = 400)

def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.user.is_ajax():
            return JsonResponse({}, status = 401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save() 
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': # test ajax
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and url_has_allowed_host_and_scheme(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest': # If ajax request
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form}, status=200)

@api_view(['DELETE', 'POST']) #http method the client == DELETE or POST
@permission_classes([IsAuthenticated]) #only authenticated users can delete tweets
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists(): #tweet not found
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists(): #unauthorized user
        return Response({"message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet deleted"}, status=200)   #delete success

@api_view(['POST']) #http method the client == POST
@permission_classes([IsAuthenticated]) #only authenticated users 
def tweet_action_view(request, *args, **kwargs):
    """
    id is required
    Action options are like, unlike, retweet
    """
    serializer = TweetActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        action = data.get("action")
        tweet_id = data.get("id")  
        content = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id)
        if not qs.exists(): #tweet not found
            return Response({}, status=404)
        obj = qs.first()
        if action == "like": #like tweet
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "unlike": #unlike tweet
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == "retweet": #retweet
            new_tweet = Tweet.objects.create(user=request.user, parent=obj, content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)    #201 for creating new tweet
    return Response(serializer.data, status=200)