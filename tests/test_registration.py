import json

from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status

from api.models import APIKey
from api.views import RegisterView


class RegisterViewTests(TestCase):

	def setUp(self):
		# Create the factory for the request.
		self.factory = RequestFactory()

	def register_user(self, data):
		# Create the request for registration.
		request = self.factory.post(
			reverse('api:register'),
			data=json.dumps(data),
			content_type="application/json"
		)
		# Get the response by passing the request to the RegisterView.
		return RegisterView.as_view()(request)

	def test_successful_registration(self):
		# Test data for a new user.
		data = {
			"username": "newuser",
			"password": "newpass"
		}
		response = self.register_user(data)
		# Check if the registration was successful.
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("api_key", response.data)

	def test_duplicate_username_registration(self):
		# Create a user.
		User.objects.create_user(username="existinguser", password="existingpass")

		# Test data with an existing username.
		data = {
			"username": "existinguser",
			"password": "newpass"
		}
		response = self.register_user(data)
		# Check if the registration was denied due to duplicate username.
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data['error'], 'Username already exists')

	def test_missing_username_or_password(self):
		# Test data with a missing password.
		data = {
			"username": "newuser"
		}
		response = self.register_user(data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data['error'], 'Username and password are required')

		# Test data with a missing username.
		data = {
			"password": "newpass"
		}
		response = self.register_user(data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(response.data['error'], 'Username and password are required')

	def test_throttle_register_view(self):
		THRESHOLD = 21

		# Make up to THRESHOLD requests
		for i in range(THRESHOLD):
			data = {
				"username": f"testuser{i}",
				"password": "testpassword"
			}
			response = self.register_user(data)

			# If we get a throttling response before the THRESHOLD, it's a pass
			if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
				return

			# If the request wasn't throttled, it should be 200 OK (or 201 if you change your response for creation)
			self.assertEqual(response.status_code, status.HTTP_200_OK)

		# If we get here, it means no request was throttled within the THRESHOLD
		self.fail("Expected a 429 Too Many Requests response within the THRESHOLD but did not receive one.")
