import aiohttp


async def get_all_currencies():
    url = f"http://127.0.0.1:8000/currencies"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status in (200, 201):
                return await response.json()
            text = await response.text()
            raise Exception(f"Error {response.status}:{text}")
        
