from django.conf import settings
from rest_framework import serializers
from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS
    
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(required=False, allow_blank=True)
    
    def validate_action(self, value):
        value = value.lower().strip() # turn to lowercase: Like -> like
        if value not in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("Action is not valid.")
        return value
    
class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'image', 'timestamp']
        
    def get_likes(self, obj):
        return obj.likes.count() # count the number of likes
    
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError(f"Max length is {MAX_TWEET_LENGTH} characters.")
        return value

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'is_retweet', 'parent','image', 'timestamp']
        
    def get_likes(self, obj):
        return obj.likes.count() # count the number of likes
    
