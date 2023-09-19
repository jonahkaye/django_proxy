from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth.models import User
from .models import APIKey

import uuid

from .tasks import call__mock_inference_api, call__inference_api
from .validation import validate_history

def is_valid_uuid(val):
	try:
		uuid.UUID(str(val))
		return True
	except ValueError:
		return False

class RegisterView(APIView):

	def post(self, request):
		username = request.data.get('username')
		password = request.data.get('password')

		# Check if the username already exists
		if User.objects.filter(username=username).exists():
			return Response({'error': 'Username already exists'}, status=400)
		
		user = User.objects.create_user(username=username, password=password)
		api_key = APIKey.objects.create(user=user)

		return Response({"api_key": api_key.key})

class APIKeyAuthentication(BaseAuthentication):

	def authenticate(self, request):
		api_key = request.headers.get('X-API-KEY')
		if not is_valid_uuid(api_key):
			raise AuthenticationFailed('Invalid API key')
		if not api_key:
			return AuthenticationFailed('No API key')
		try:
			key = APIKey.objects.get(key=api_key)
		except APIKey.DoesNotExist:
			raise AuthenticationFailed('No such key')
		request.user = key.user
		return (key.user, api_key)

class InferenceProxyView(APIView):
	authentication_classes = [APIKeyAuthentication] # Who is making this request?
	permission_classes = [IsAuthenticated] # Does the identified user have the right to do what they're asking?
	throttle_classes = [UserRateThrottle]


	def post(self, request):
		# Extract data from the incoming request
		data = request.data

		# Optional: Do some preprocessing or validation here
		try:
			history_data = data.get('history', [])
			validate_history(history_data)
		except Exception as e:
			return Response({"error": str(e)}, status=400)

		# Forward request to the inference API
		task_result = call__inference_api.delay(data).get()

		# Return the response to the client
		return Response(task_result["content"], status=task_result["status_code"])
