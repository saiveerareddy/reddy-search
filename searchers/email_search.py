# searchers/email_search.py
from utils import get_key, fetch
import aiohttp

HUNTER_KEY = get_key("HUNTER_API_KEY")
HUNTER_URL = "https://api.hunter.io/v2/email-verifier"

async def hunter_email_verifier(email: str):
    if not HUNTER_KEY:
        return {"error": "No HUNTER_API_KEY set"}
    params = {"email": email, "api_key": HUNTER_KEY}
    async with aiohttp.ClientSession() as session:
        return await fetch(session, "GET", HUNTER_URL, params=params)

