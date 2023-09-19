import aiohttp
import asyncio
import random
import json

API_ENDPOINT = "http://127.0.0.1:8000/api/inference_proxy/"

# This is a placeholder; in practice, you'll fill this up with the 10 API keys you have.
API_KEYS = ["cc0f2766-47bb-416f-8b09-40342a77f439"]

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

async def send_request(session, api_key):
    headers = {
        "Content-Type": "application/json",
        "X-API-KEY": api_key
    }
    
    data = random.choice(data_bundles)
    
    async with session.post(API_ENDPOINT, headers=headers, json=data) as response:
        return await response.text()

async def main(num_requests: int):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_requests):
            api_key = API_KEYS[i % len(API_KEYS)]  # Rotate through the API keys.
            tasks.append(send_request(session, api_key))
        
        responses = await asyncio.gather(*tasks)
        
        for i, response in enumerate(responses):
            print(f"Response {i + 1}:", response)

if __name__ == "__main__":
    NUMBER_OF_REQUESTS = 20  # Adjust this number based on your needs
    asyncio.run(main(NUMBER_OF_REQUESTS))
