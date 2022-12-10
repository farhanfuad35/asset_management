from django.test import TestCase
from .models import User
from rest_framework.authtoken.models import Token

# Create your tests here.
class TestTokenAuthentication(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="fuad", password="password")
        token = Token.objects.create(user=self.user)

    def test_tokenAuth(self):
        url = "/api-token-auth/"
        response = self.client.post(
            path=url, data={"username": "fuad", "password": "password"}
        )
        print(response.json())
        self.assertEqual(response.status_code, 200)
