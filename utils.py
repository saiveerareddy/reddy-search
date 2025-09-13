# utils.py
import os
import json
import asyncio
import aiohttp
from dotenv import load_dotenv
from typing import Dict, Any
import pandas as pd

load_dotenv()

def get_key(name: str) -> str:
    return os.getenv(name, "")

async def fetch(session: aiohttp.ClientSession, method: str, url: str, **kwargs):
    async with session.request(method, url, **kwargs) as resp:
        try:
            text = await resp.text()
            # try JSON
            try:
                return await resp.json()
            except Exception:
                return {"status": resp.status, "text": text}
        except Exception as e:
            return {"error": str(e), "status": getattr(resp, 'status', None)}

async def gather_with_concurrency(tasks):
    return await asyncio.gather(*tasks)

def export_json(data: Dict[str, Any], path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def export_csv(data: Dict[str, Any], path: str):
    # flatten for CSV: best-effort
    rows = []
    for k,v in data.items():
        if isinstance(v, dict):
            rows.append({"key": k, **{f"{k}_{ik}": iv for ik, iv in v.items()}})
        else:
            rows.append({"key": k, "value": v})
    df = pd.json_normalize(data, sep="_")
    df.to_csv(path, index=False)
