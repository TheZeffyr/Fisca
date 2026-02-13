import aiohttp
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


async def create_transaction(
    user_tg_id: int,
    category_id: int,
    saving_id: int | None,
    amount: int,
    date_time: datetime,
    transaction_type: str
):
    url = f"http://127.0.0.1:8000/transactions"
    payload = {
        "user_tg_id": user_tg_id,
        "category_id": category_id,
        "saving_id": saving_id,
        "amount": amount,
        "date_time": date_time.isoformat(),
        "transaction_type": transaction_type
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status in (200, 201):
                logger.info(
                    f"💰 Creating transaction for \
                    user {user_tg_id}: amount={amount}, \
                    type={transaction_type}"
                )
                return await response.json()
            text = await response.text()
            raise Exception(f"Error {response.status}:{text}")

        
