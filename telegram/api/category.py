import aiohttp
from typing import Optional, List, Dict

async def get_categories_by_filters(
    user_tg_id: int,
    transaction_type: str,  # "income" или "expense"
) -> List[Dict]:

    url = "http://127.0.0.1:8000/categories/filter"
    
    params = {
        "user_tg_id": user_tg_id,
        "transaction_type": transaction_type
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            
            text = await response.text()
            
            if response.status == 404:
                return []  # Нет категорий
            else:
                raise Exception(f"Error {response.status}:{text}")

async def get_by_id(
    id: int
):
    if id <= 0:
        raise ValueError("ID must be positive integer")
    
    url = f"http://127.0.0.1:8000/categories/{id}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                elif response.status == 404:
                    text = await response.text()
                    raise ValueError(f"Category with id {id} not found: {text}")
                else:
                    text = await response.text()
                    raise ValueError(f"Unexpected response {response.status}: {text}")
                    
        except aiohttp.ClientError as e:
            raise aiohttp.ClientError(f"Connection error while fetching category {id}: {e}")