# tasks.py
import random
import logging
import requests
from django.conf import settings

from celery import shared_task, current_app


from celery.signals import task_prerun, task_postrun

# A simple counter for running tasks
running_tasks_counter = 0
max_pool_size = 5

@task_prerun.connect
def task_prerun_handler(*args, **kwargs):
	global running_tasks_counter
	running_tasks_counter += 1
	if running_tasks_counter == max_pool_size:
		logging.info("Task pool is full.")

@task_postrun.connect
def task_postrun_handler(*args, **kwargs):
	global running_tasks_counter
	running_tasks_counter -= 1

@shared_task
def call__inference_api(data):
	logging.critical(f"Starting task {call__inference_api.request.id}. Currently {running_tasks_counter} tasks are running.")
	headers = {
		'Content-Type': 'application/json',
		'Authorization': f'Token {settings.GEN_HEALTH_KEY}',
	}
	response = requests.post('https://api.genhealth.ai/predict', headers=headers, json=data)
	result = {
		"status_code": response.status_code,
		"content": response.json()  # Assumes that the response from the endpoint is JSON formatted.
	}
	logging.critical(f"Finished task {call__inference_api.request.id}, result: {result}")
	return result



# @shared_task
# def call__mock_inference_api():
# 	# This is a mock endpoint. Replace with your actual endpoint.	
# 	# generate a random number between 1 and 10:
# 	logging.info(f"Starting task {call__mock_inference_api.request.id}")

# 	# num = random.randint(1, 10)
# 	# prompt = f'''You are a medical code random generator. Respond with a random list of {str(num)} CPT codes. Respond only with codes, and nothing else'''
# 	# messages = [ 
# 	# 			{'role': 'user', 'content': prompt}
# 	# 		]
# 	# model = "gpt-3.5-turbo"
# 	# azure_wrapper = AzureWrapper()
# 	# response = azure_wrapper.create_chat_completion(model=model, messages=messages)
# 	response = {"data": "finished task"}
# 	logging.info(f"Finished task {call__mock_inference_api.request.id}")
# 	return response
