import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404,JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from ..models import Profile
from ..serializers import PublicProfileSerializer

User = get_user_model()
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

@api_view(['GET'])
def profile_detail_api_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username__iexact=username)
    if not qs.exists():
        raise Response({"detail": "User not found"}, status = 404)
    profile_obj = qs.first()
    data = PublicProfileSerializer(instance=profile_obj, context={"request": request}).data
    return Response(data, status = 200)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated]) #only authenticated users can create tweets
def user_follow_view(request, username, *args, **kwargs):
    current_user = request.user
    to_follow_user_qs = User.objects.filter(username = username)
    if current_user.username == username:
        my_followers_qs = current_user.profile.followers.all()
        return Response({"count": my_followers_qs.count()}, status = 200)
    if not to_follow_user_qs.exists():
        return Response({}, status = 404)
    to_follow_user = to_follow_user_qs.first()
    profile = to_follow_user.profile
    data = request.data or {}
    action = data.get('action')
    if action == 'follow':
        profile.followers.add(current_user)
    elif action == 'unfollow':
        profile.followers.remove(current_user)
    else:
        pass
    data = PublicProfileSerializer(instance=profile, context={"request": request}).data
    return Response(data, status = 200)