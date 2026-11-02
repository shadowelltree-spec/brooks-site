#!/usr/bin/env python3
"""termix_listings.py - print a Markdown table of an agent's public Termix listings.

Read-only, no API key, standard library only.
Usage: python3 termix_listings.py <agentId> [--json]
"""
import json
import sys
import urllib.request

API = "https://platform-backend.prod.termix.live/api/v1/listings"  # BNB Chain
WEB = "https://www.agent.family/listing?id="


def fetch(agent_id: str) -> list[dict]:
    url = f"{API}?providerAgentId={agent_id}&pageSize=100"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp).get("items", [])


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    items = [i for i in fetch(sys.argv[1]) if i.get("status") == "PUBLISHED"]
    if "--json" in sys.argv:
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return 0
    print("| Service | Price | Delivery | Buy | Link |")
    print("|---|---|---|---|---|")
    for i in items:
        buy = "instant" if i.get("instantBuyable") else "quote"
        print(f"| {i['title'][:48]} | {i['basePrice']} {i['currency']} "
              f"| {i['deliveryDays']} d | {buy} | {WEB}{i['id']} |")
    print(f"\n{len(items)} published listing(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
