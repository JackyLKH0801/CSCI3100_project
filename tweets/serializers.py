from django.conf import settings
from rest_framework import serializers
from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['content']
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError(f"Max length is {MAX_TWEET_LENGTH} characters.")
        return value
    
class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    
    def validate_action(self, value):
        value = value.lower().strip() # turn to lowercase: Like -> like
        if value not in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("Action is not valid.")
        return value
