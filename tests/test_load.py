from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
import json

from api.models import APIKey
from api.views import InferenceProxyView

class LoadTest(TestCase):

    def setUp(self):
        # Create the factory for the request.
        self.factory = RequestFactory()

        # Create 10 test users and their associated API keys.
        self.users = [User.objects.create_user(username=f'testuser{i}', password='testpass') for i in range(10)]
        self.api_keys = [APIKey.objects.create(user=user) for user in self.users]

        # Setup the URL and data for the request.
        self.url = reverse('api:inference_proxy')
        self.data = {
            'history': [
                {
                    'code': '64',
                    'system': 'age',
                    'display': '64',
                },
                {
                    'code': 'E11',
                    'system': 'ICD10CM',
                    'display': 'Type 2 diabetes mellitus',
                },
                {
                    'code': 'E11.3551',
                    'system': 'ICD10CM',
                    'display': 'Type 2 diabetes mellitus with stable proliferative diabetic retinopathy, right eye',
                },
            ],
            'num_predictions': 1,
            'generation_length': 10,
            'inference_threshold': 0.95,
            'inference_temperature': 0.95,
        }

    def send_request(self, api_key):
        headers = {
            "Content-Type": "application/json",
            "HTTP_X_API_KEY": str(api_key.key)  # Use the provided API key.
        }

        request = self.factory.post(
            self.url, 
            data=json.dumps(self.data), 
            content_type="application/json", 
            **headers
        )
        response = InferenceProxyView.as_view()(request)
        return response

    def test_load(self):
        NUMBER_OF_REQUESTS_PER_USER = 1

        responses = []

        # Iterate through each request, cycling users for each subsequent request
        for _ in range(NUMBER_OF_REQUESTS_PER_USER):
            for api_key in self.api_keys:
                responses.append(self.send_request(api_key))

        # Assert all responses are 200 OK.
        self.assertTrue(all([res.status_code == 200 for res in responses]))
