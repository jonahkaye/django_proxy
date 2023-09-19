# tasks.py
import random
import logging
import requests
from django.conf import settings

from celery import shared_task


@shared_task
def call__mock_inference_api():
	# This is a mock endpoint. Replace with your actual endpoint.	
	# generate a random number between 1 and 10:
	logging.info(f"Starting task {call__mock_inference_api.request.id}")

	# num = random.randint(1, 10)
	# prompt = f'''You are a medical code random generator. Respond with a random list of {str(num)} CPT codes. Respond only with codes, and nothing else'''
	# messages = [ 
	# 			{'role': 'user', 'content': prompt}
	# 		]
	# model = "gpt-3.5-turbo"
	# azure_wrapper = AzureWrapper()
	# response = azure_wrapper.create_chat_completion(model=model, messages=messages)
	response = {"data": "finished task"}
	logging.info(f"Finished task {call__mock_inference_api.request.id}")
	return response


@shared_task
def call__inference_api(data):
	logging.info(f"Starting task {call__inference_api.request.id}")
	headers = {
		'Content-Type': 'application/json',
		'Authorization': f'Token {settings.GEN_HEALTH_KEY}',
	}
	logging.info(f"Finished task {call__inference_api.request.id}")
	response = requests.post('https://api.genhealth.ai/predict', headers=headers, json=data)
	result = {
        "status_code": response.status_code,
        "content": response.json()  # Assumes that the response from the endpoint is JSON formatted.
    }
	logging.critical(result)
	return result






