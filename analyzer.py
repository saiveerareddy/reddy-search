# analyzer.py
import os
from typing import Dict, Any
from utils import get_key
import requests

OPENAI_KEY = get_key("OPENAI_API_KEY")

def simple_score(aggregated: Dict[str, Any]) -> int:
    """Heuristic risk / relevance score 0-100"""
    score = 0
    # example heuristics:
    if "hibp" in aggregated and aggregated["hibp"].get("data"):
        score += 40
    if "shodan" in aggregated and aggregated["shodan"].get("data"):
        # if open ports found
        data = aggregated["shodan"]["data"]
        if isinstance(data, dict) and data.get("ports"):
            score += min(40, len(data.get("ports")) * 5)
    if aggregated.get("email_enrichment"):
        score += 10
    if score > 100:
        score = 100
    return score

def ai_summarize(aggregated: Dict[str, Any]) -> Dict[str, str]:
    """Optional: use an LLM to produce a short human-friendly summary."""
    if not OPENAI_KEY:
        return {"summary": "No OPENAI_API_KEY set — install one to enable AI summaries."}
    # Use the requests library to keep dependency minimal; you can swap to openai SDK
    prompt = (
        "You are an OSINT assistant. Summarize the following findings in plain English, "
        "give likely relevance, and suggest next safe steps for further investigation. Do not advise on illegal activity.\n\n"
        f"Findings:\n{aggregated}\n\nSummary:"
    )
    headers = {
        "Authorization": f"Bearer {OPENAI_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",   # pick available model; adjust to your account
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 400,
        "temperature": 0.2
    }
    r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
    if r.status_code != 200:
        return {"error": f"OpenAI error {r.status_code}: {r.text}"}
    data = r.json()
    # tolerate different shapes
    try:
        summary = data["choices"][0]["message"]["content"]
    except Exception:
        summary = str(data)
    return {"summary": summary}
