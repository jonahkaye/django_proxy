import json
import random

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from api.models import APIKey
from api.views import InferenceProxyView

data_bundles = [
{'history': [
    {'code': '67', 'system': 'age', 'display': '67'}, 
    {'code': 'I10', 'system': 'ICD10CM', 'display': 'Essential hypertension'},
    {'code': 'I10.90', 'system': 'ICD10CM', 'display': 'Essential hypertension without complications'}],
 'num_predictions': 1,
 'generation_length': 10,
 'inference_threshold': 0.95,
 'inference_temperature': 0.95},

{'history': [
    {'code': '72', 'system': 'age', 'display': '72'},
    {'code': 'E78', 'system': 'ICD10CM', 'display': 'Pure hypercholesterolemia'},
    {'code': 'E78.01', 'system': 'ICD10CM', 'display': 'Familial hypercholesterolemia'}],
 'num_predictions': 1, 
 'generation_length': 10,
 'inference_threshold': 0.95,
 'inference_temperature': 0.95},

{'history': [
    {'code': '56', 'system': 'age', 'display': '56'},
    {'code': 'J44', 'system': 'ICD10CM', 'display': 'Chronic obstructive pulmonary disease'},
    {'code': 'J44.9', 'system': 'ICD10CM', 'display': 'Chronic obstructive pulmonary disease, unspecified'}],
 'num_predictions': 1,
 'generation_length': 10, 
 'inference_threshold': 0.95,
 'inference_temperature': 0.95},

{'history': [
    {'code': '45', 'system': 'age', 'display': '45'},
    {'code': 'K21', 'system': 'ICD10CM', 'display': 'Gastroesophageal reflux disease'},
    {'code': 'K21.9', 'system': 'ICD10CM', 'display': 'Gastroesophageal reflux disease without esophagitis'}],
 'num_predictions': 1,
 'generation_length': 10,
 'inference_threshold': 0.95,
 'inference_temperature': 0.95},

{'history': [
    {'code': '71', 'system': 'age', 'display': '71'},
    {'code': 'N18', 'system': 'ICD10CM', 'display': 'Chronic kidney disease'},
    {'code': 'N18.3', 'system': 'ICD10CM', 'display': 'Chronic kidney disease, stage 3 moderate'}],
 'num_predictions': 1,
 'generation_length': 10,
 'inference_threshold': 0.95, 
 'inference_temperature': 0.95},

{'history': [
    {'code': '59', 'system': 'age', 'display': '59'},
    {'code': 'M54', 'system': 'ICD10CM', 'display': 'Dorsalgia'},
    {'code': 'M54.5', 'system': 'ICD10CM', 'display': 'Low back pain'}],
 'num_predictions': 1,
 'generation_length': 10,
 'inference_threshold': 0.95,
 'inference_temperature': 0.95},

{'history': [
    {'code': '34', 'system': 'age', 'display': '34'},
    {'code': 'F41', 'system': 'ICD10CM', 'display': 'Anxiety disorder'},
    {'code': 'F41.1', 'system': 'ICD10CM', 'display': 'Generalized anxiety disorder'}],
 'num_predictions': 1,
 'generation_length': 10,
 'inference_threshold': 0.95,
 'inference_temperature': 0.95},

{'history': [
    {'code': '48', 'system': 'age', 'display': '48'},
    {'code': 'I83', 'system': 'ICD10CM', 'display': 'Varicose veins of lower extremities'},
    {'code': 'I83.90', 'system': 'ICD10CM', 'display': 'Varicose veins of unspecified lower extremity without complications'}],
 'num_predictions': 1,
 'generation_length': 10,
 'inference_threshold': 0.95,
 'inference_temperature': 0.95},

{'history': [
    {'code': '62', 'system': 'age', 'display': '62'},
    {'code': 'M16', 'system': 'ICD10CM', 'display': 'Osteoarthritis of hip'},
    {'code': 'M16.12', 'system': 'ICD10CM', 'display': 'Unilateral osteoarthritis, left hip'}],
 'num_predictions': 1,
 'generation_length': 10,
 'inference_threshold': 0.95,
 'inference_temperature': 0.95},

{'history': [
    {'code': '57', 'system': 'age', 'display': '57'},
    {'code': 'H25', 'system': 'ICD10CM', 'display': 'Age-related cataract'},
    {'code': 'H25.11', 'system': 'ICD10CM', 'display': 'Age-related nuclear cataract, right eye'}],
 'num_predictions': 1,
 'generation_length': 10, 
 'inference_threshold': 0.95,
 'inference_temperature': 0.95}
]

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

        # Randomly select a data bundle for the request
        self.data = random.choice(data_bundles)

        request = self.factory.post(
            self.url, 
            data=json.dumps(self.data), 
            content_type="application/json", 
            **headers
        )
        response = InferenceProxyView.as_view()(request)
        return response

    # synchronous testing
    def test_load(self):
        NUMBER_OF_REQUESTS_PER_USER = 1

        responses = []

        # Iterate through each request, cycling users for each subsequent request
        for _ in range(NUMBER_OF_REQUESTS_PER_USER):
            for api_key in self.api_keys:
                responses.append(self.send_request(api_key))

        # Assert all responses are 200 OK.
        self.assertTrue(all([res.status_code == 200 for res in responses]))
