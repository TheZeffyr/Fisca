import aiohttp


async def register_user(tg_id: int, currency_id: int):
    """
    Register a new user via FastAPI backend API.
    
    Sends a POST request to the user registration endpoint to create
    a new user in the system with the provided Telegram ID and currency.
    
    Args:
        tg_id: Telegram user identifier. Must be a positive integer 
               and unique across the system.
        currency_id: ID of the user's default currency. References
                    the currency in the database.
    
    Returns:
        Dictionary containing the created user data, typically including:
        - id: Database-generated user ID
        - tg_id: Provided Telegram ID
        - currency_id: Provided currency ID
        - created_at: ISO-formatted timestamp of creation
    """
    url = "http://127.0.0.1:8000/users/register"
    payload = {
        "tg_id": tg_id,
        "currency_id": currency_id
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status in (200, 201):
                return await response.json()
            text = await response.text()
            raise Exception(f"Error {response.status}:{text}")
        
