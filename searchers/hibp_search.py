# searchers/hibp_search.py
import os
from utils import get_key, fetch
import aiohttp

API_KEY = get_key("HIBP_API_KEY")
BASE = "https://haveibeenpwned.com/api/v3"

headers = {}
if API_KEY:
    headers["hibp-api-key"] = API_KEY
headers["user-agent"] = "ReddySearch/1.0"

async def hibp_email_search(email: str):
    url = f"{BASE}/breachedaccount/{email}"
    params = {"truncateResponse": "false"}
    async with aiohttp.ClientSession(headers=headers) as session:
        result = await fetch(session, "GET", url, params=params)
        # HIBP returns 404 for no breach; treat that gracefully
        return {"source": "hibp", "email": email, "data": result}
