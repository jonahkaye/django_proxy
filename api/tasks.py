# tasks.py
import random
import logging
from celery import shared_task


from .mock_api import AzureWrapper

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






