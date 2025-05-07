from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework.test import APIClient
from .models import Profile

User = get_user_model()

class ProfileTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='testpassword1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2'
        )

    def get_client(self):
        client = APIClient()
        client.login(username=self.user1.username, password='testpassword1')
        return client
    
    def test_profile_created(self):
        qs = Profile.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_following(self):
        first = self.user1
        second = self.user2
        first.profile.followers.add(second)
        user2_following_whom = second.following.all()
        qs = user2_following_whom.filter(user__username=first.username)
        user1_following_whom = first.following.all()
        self.assertTrue(qs.exists())
        self.assertFalse(user1_following_whom.exists())

    def test_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(f"/api/profiles/{self.user2.username}/follow", {"action": "follow"})
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 1)

    def test_unfollow_api_endpoint(self):
        first = self.user1
        second = self.user2
        first.profile.followers.add(second)
        client = self.get_client()
        response = client.post(f"/api/profiles/{self.user2.username}/follow", {"action": "unfollow"})
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 0)

    def test_following_self(self):
        client = self.get_client()
        response = client.post(f"/api/profiles/{self.user1.username}/follow", {"action": "follow"})
        r_data = response.json()
        count = r_data.get("count")
        self.assertEqual(count, 0)