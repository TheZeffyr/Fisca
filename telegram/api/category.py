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
