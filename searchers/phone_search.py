# searchers/phone_search.py
from utils import get_key, fetch
import aiohttp

NUMVERIFY_KEY = get_key("NUMVERIFY_API_KEY")
NUMVERIFY_URL = "http://apilayer.net/api/validate"

async def numverify_phone(phone: str):
    if not NUMVERIFY_KEY:
        return {"error": "No NUMVERIFY_API_KEY set"}
    params = {"access_key": NUMVERIFY_KEY, "number": phone}
    async with aiohttp.ClientSession() as session:
        return await fetch(session, "GET", NUMVERIFY_URL, params=params)

