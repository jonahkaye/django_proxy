import aiohttp
import asyncio

API_ENDPOINT = "http://127.0.0.1:8000/api/inference_proxy/"
HEADERS = {
    "Content-Type": "application/json",
    "X-API-KEY": "cc0f2766-47bb-416f-8b09-40342a77f439"
}
DATA = {"data": "your_inference_data_here"}

async def send_request(session):
    await asyncio.sleep(0.1)
    async with session.post(API_ENDPOINT, headers=HEADERS, json=DATA) as response:
        return await response.text()
                  # Introduce a delay of 0.1 seconds


async def main(num_requests: int):
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session) for _ in range(num_requests)]
        responses = await asyncio.gather(*tasks)
        for i, response in enumerate(responses):
            print(f"Response {i + 1}:", response)

if __name__ == "__main__":
    NUMBER_OF_REQUESTS = 1000  # Adjust this number based on your needs
    asyncio.run(main(NUMBER_OF_REQUESTS))
