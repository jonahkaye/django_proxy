from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
import json

from api.models import APIKey
from api.views import InferenceProxyView

class InferenceProxyViewTests(TestCase):

	def setUp(self):
		# Create the factory for the request.
		self.factory = RequestFactory()
		
		# Create a test user.
		self.user = User.objects.create_user(username='testuser', password='testpass')
		
		# Automatically create an APIKey for the user because of the OneToOne relationship.
		self.api_key = APIKey.objects.create(user=self.user)

	def post_request(self, data):
		# Create the request and include the API key in the headers.
		request = self.factory.post(
			reverse('api:inference_proxy'),
			data=json.dumps(data),
			content_type="application/json",
			HTTP_X_API_KEY=str(self.api_key.key)
		)
		# Get the response by passing the request to the view.
		return InferenceProxyView.as_view()(request)

	def test_successful_validation(self):
		valid_data = {
			'history': [
				{"code": "64", "system": "age", "display": "64"},
				{"code": "E11", "system": "ICD10CM", "display": "Type 2 diabetes mellitus"},
				{"code": "06-12-month", "system": "timegap", "display": "06-12-month"}
			]
		}
		
		response = self.post_request(valid_data)
		self.assertEqual(response.status_code, 200)
	

	def test_missing_key(self):
		invalid_data = {
			'history': [
				{"code": "64", "system": "age"}
			]
		}
		response = self.post_request(invalid_data)
		self.assertEqual(response.status_code, 400)
		self.assertIn('Each object must contain a', response.data['error'])

	def test_invalid_age(self):
		invalid_data = {
			'history': [
				{"code": "122", "system": "age", "display": "122"}
			]
		}
		response = self.post_request(invalid_data)
		self.assertEqual(response.status_code, 400)
		self.assertIn('Invalid age', response.data['error'])

	def test_invalid_gender(self):
		invalid_data = {
			'history': [
				{"code": "alien", "system": "gender", "display": "alien"}
			]
		}
		response = self.post_request(invalid_data)
		self.assertEqual(response.status_code, 400)
		self.assertIn('Invalid gender', response.data['error'])

	def test_invalid_timegap(self):
		invalid_data = {
			'history': [
				{"code": "10-20-month", "system": "timegap", "display": "10-20-month"}
			]
		}
		response = self.post_request(invalid_data)
		self.assertEqual(response.status_code, 400)
		self.assertIn('Invalid timegap', response.data['error'])

	def test_unknown_system(self):
		invalid_data = {
			'history': [
				{"code": "10", "system": "unknown_system", "display": "10"}
			]
		}
		response = self.post_request(invalid_data)
		self.assertEqual(response.status_code, 400)
		self.assertIn('Unknown system', response.data['error'])
