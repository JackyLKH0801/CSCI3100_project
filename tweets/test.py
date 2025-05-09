from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from .models import Tweet

User = get_user_model()

class TweetTestCase(TestCase):
    def setUp(self):
        # Create a user and a tweet for testing
        User.objects.create_user(username='testuser', password='testpassword')
        User.objects.create_user(username='testuser2', password='testpassword')
        Tweet.objects.create(content='Hello world, this is my first tweet', user=User.objects.get(username='testuser'))
        Tweet.objects.create(content='second tweet', user=User.objects.get(username='testuser'))
        Tweet.objects.create(content='third tweet', user=User.objects.get(username='testuser2'))
        self.currentCount = Tweet.objects.all().count()
        
    def test_user_exists(self):
        user = User.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        
    def test_tweet_creation(self):
        # Create the second tweet
        tweet = Tweet.objects.create(content='forth tweet', user=User.objects.get(username='testuser'))
        # Check if the id is 2
        self.assertEqual(tweet.id, 4)
        # Check if the content is correct
        self.assertEqual(tweet.content, 'forth tweet')
        # Check if the user is correct
        self.assertEqual(tweet.user.username, 'testuser')
        
    def get_client(self):
        client = APIClient()
        client.login(username='testuser', password='testpassword')
        return client
    
    # test if can create a tweet
    def test_tweet_create_api_view(self):
        request_data = {'content': 'This is my test tweet'}
        client = self.get_client()
        response = client.post('/api/tweets/create/', request_data)
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get('id')
        # Check if the new tweet is created
        self.assertEqual(new_tweet_id, self.currentCount + 1)
    
    # test if can login and grab tweets
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    # test the detail view of a tweet
    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get('/api/tweets/1/')
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        # Check if the tweet id is correct
        _id = response_data.get('id')
        self.assertEqual(_id, 1)
        # Check if the content is correct
        content = response_data.get('content')
        self.assertEqual(content, 'Hello world, this is my first tweet')

    # test if can like a tweet
    def test_action_like(self):
        client = self.get_client()
        response = client.post('/api/tweets/action/', {'id': 1, 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['likes'], 1)
        
    # test if can unlike a tweet
    def test_action_unlike(self):
        client = self.get_client()
        # First like the tweet
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'like'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['likes'], 1)
        # Then unlike the tweet
        response = client.post('/api/tweets/action/', {'id': 2, 'action': 'unlike'})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        # Check if the like count is 0
        self.assertEqual(like_count, 0)

    # test if can retweet a tweet
    def test_action_retweet(self):
        client = self.get_client()
        currentCount = Tweet.objects.all().count()
        # First retweet the tweet
        response = client.post('/api/tweets/action/', {'id': 3, 'action': 'retweet'})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get('id')
        # Check if the new tweet is a retweet
        self.assertNotEqual(new_tweet_id, 3)
        self.assertEqual(currentCount + 1, new_tweet_id)
        
    
        