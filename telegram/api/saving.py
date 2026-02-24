import aiohttp
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


async def create_saving(
    user_tg_id: int,
    name: str,
    final_amount: int,
    deadline: datetime,
):
    url = f"http://127.0.0.1:8000/savings"
    payload = {
        "user_tg_id": user_tg_id,
        "name": name,
        "final_amount": final_amount,
        "deadline": deadline.isoformat()
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status in (200, 201):
                logger.info(
                    f"💰 Creating saving for \
                    user {user_tg_id}: final_amount={final_amount}"
                )
                return await response.json()
            text = await response.text()
            raise Exception(f"Error {response.status}:{text}")


async def get_savings_by_user_tg_id(
    user_tg_id: int
):
    params  = {
        "user_tg_id": user_tg_id
    }
    url = f"http://127.0.0.1:8000/savings"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()
            
            text = await response.text()
            
            if response.status == 404:
                return []
            else:
                raise Exception(f"Error {response.status}:{text}")
        
