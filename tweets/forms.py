from django import forms
from .models import Tweet
from django.conf import settings
MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['content']
        
    def clean_content(self):
        content = self.cleaned_data.get("content")
        if content == "":
            raise forms.ValidationError("This field is required.")
        if len(content) > MAX_TWEET_LENGTH:
            raise forms.ValidationError(f"Max length is {MAX_TWEET_LENGTH} characters.")
        return content
