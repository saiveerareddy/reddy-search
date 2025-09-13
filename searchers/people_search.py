# searchers/people_search.py
from utils import get_key, fetch
import aiohttp

# This is a placeholder; name searches are noisy and often require paid services (Pipl, People Data Labs, Clearbit)
PDL_KEY = get_key("PDL_API_KEY")  # People Data Labs as an example

async def pdl_people_search(name: str):
    if not PDL_KEY:
        return {"error": "No PDL_API_KEY set"}
    url = "https://api.peopledatalabs.com/v5/person/enrich"
    params = {"name": name, "api_key": PDL_KEY}
    async with aiohttp.ClientSession() as session:
        return await fetch(session, "GET", url, params=params)

