from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
import json

from api.models import APIKey
from api.views import InferenceProxyView

class RateLimitingTest(TestCase):

    def setUp(self):
        # Create the factory for the request.
        self.factory = RequestFactory()

        # Create a test user and the associated API key.
        self.user = User.objects.create_user(username='ratelimituser', password='testpass')
        self.api_key = APIKey.objects.create(user=self.user)

        # Setup the URL and data for the request.
        self.url = reverse('api:inference_proxy')
        self.data = {
			'history': [
				{"code": "64", "system": "age", "display": "64"},
				{"code": "E11", "system": "ICD10CM", "display": "Type 2 diabetes mellitus"},
				{"code": "06-12-month", "system": "timegap", "display": "06-12-month"}
			]
		}

    def send_request(self):
        headers = {
            "Content-Type": "application/json",
            "HTTP_X_API_KEY": str(self.api_key.key)
        }

        request = self.factory.post(
            self.url, 
            data=json.dumps(self.data), 
            content_type="application/json", 
            **headers
        )
        response = InferenceProxyView.as_view()(request)
        return response

    def test_rate_limiting(self):
        # Send 100 requests without issues.
        for _ in range(100):
            response = self.send_request()
            self.assertEqual(response.status_code, 200)

        # The 101st request should trigger the rate limiter.
        response = self.send_request()
        self.assertEqual(response.status_code, 429)
