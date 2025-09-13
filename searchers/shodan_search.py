
# searchers/shodan_search.py
import os
from utils import get_key, fetch
import aiohttp

SHODAN_API = "https://api.shodan.io"
API_KEY = get_key("SHODAN_API_KEY")

async def shodan_ip_search(ip: str):
    if not API_KEY:
        return {"error": "No SHODAN_API_KEY set in environment"}
    url = f"{SHODAN_API}/shodan/host/{ip}?key={API_KEY}"
    async with aiohttp.ClientSession() as session:
        result = await fetch(session, "GET", url)
        return {"source": "shodan", "ip": ip, "data": result}
