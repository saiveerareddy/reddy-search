# main.py
import argparse
import asyncio
import json
from searchers import shodan_search, hibp_search, email_search, phone_search, people_search
from analyzer import simple_score, ai_summarize
from utils import export_json, export_csv

async def run_ip(ip):
    shodan_task = shodan_search.shodan_ip_search(ip)
    done = await asyncio.gather(shodan_task)
    aggregated = {"shodan": done[0]}
    aggregated["score"] = simple_score(aggregated)
    aggregated["ai"] = ai_summarize(aggregated)
    return aggregated

async def run_email(email):
    hibp_task = hibp_search.hibp_email_search(email)
    hunter_task = email_search.hunter_email_verifier(email)
    hibp_res, hunter_res = await asyncio.gather(hibp_task, hunter_task)
    aggregated = {"hibp": hibp_res, "email_enrichment": hunter_res}
    aggregated["score"] = simple_score(aggregated)
    aggregated["ai"] = ai_summarize(aggregated)
    return aggregated

async def run_phone(phone):
    res = await phone_search.numverify_phone(phone)
    aggregated = {"phone": res}
    aggregated["score"] = simple_score(aggregated)
    aggregated["ai"] = ai_summarize(aggregated)
    return aggregated

async def run_name(name):
    res = await people_search.pdl_people_search(name)
    aggregated = {"people": res}
    aggregated["score"] = simple_score(aggregated)
    aggregated["ai"] = ai_summarize(aggregated)
    return aggregated

def parse_args():
    p = argparse.ArgumentParser(prog="Reddy Search")
    p.add_argument("--type", choices=["ip","email","phone","name"], required=True)
    p.add_argument("--value", required=True, help="IP/email/phone/name to search")
    p.add_argument("--export", choices=["json","csv"], default=None)
    return p.parse_args()

def main():
    args = parse_args()
    loop = asyncio.get_event_loop()
    if args.type == "ip":
        aggregated = loop.run_until_complete(run_ip(args.value))
    elif args.type == "email":
        aggregated = loop.run_until_complete(run_email(args.value))
    elif args.type == "phone":
        aggregated = loop.run_until_complete(run_phone(args.value))
    else:
        aggregated = loop.run_until_complete(run_name(args.value))
    print(json.dumps(aggregated, indent=2, ensure_ascii=False))
    if args.export == "json":
        export_json(aggregated, "reddy_result.json")
        print("Exported reddy_result.json")
    if args.export == "csv":
        export_csv(aggregated, "reddy_result.csv")
        print("Exported reddy_result.csv")

if __name__ == "__main__":
    main()
