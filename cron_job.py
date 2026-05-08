"""
Cron job that runs twice a month (1st and 15th).
Refreshes MAL list and searches enabled stores.
"""
import time
import random
from datetime import datetime
from mal_sync import fetch_mal_list
from sheets import load_want_list, load_do_not_want_list
from scraper import search_amazon_com, search_amazon_jp, search_crunchyroll_store, search_ebay
from scheduler import load_scheduler_settings, update_status
import json
import os

RESULTS_FILE = "/app/data/results.json"


def run_scheduled_search():
    settings = load_scheduler_settings()

    if not settings.get("auto_refresh", True):
        print("Auto-refresh disabled, skipping.")
        return

    # Refresh MAL
    print("Fetching MAL list...")
    mal_titles = fetch_mal_list()
    update_status("last_mal_refresh")
    print(f"Got {len(mal_titles)} titles from MAL")

    # Load sheets
    want_list = load_want_list()
    do_not_want_list = load_do_not_want_list()

    # Filter
    titles = [t for t in mal_titles if t.lower() not in [d.lower() for d in do_not_want_list]]
    titles = list(set(titles + want_list))
    titles.sort()

    # Search
    results = []
    for title in titles:
        items = []
        if settings.get("amazon_com", True):
            items.extend(search_amazon_com(title))
            time.sleep(random.uniform(2, 4))
        if settings.get("amazon_jp", True):
            items.extend(search_amazon_jp(title))
            time.sleep(random.uniform(2, 4))
        if settings.get("crunchyroll", True):
            items.extend(search_crunchyroll_store(title))
            time.sleep(random.uniform(2, 4))
        if settings.get("ebay", True) and not items:
            items.extend(search_ebay(title))
            time.sleep(random.uniform(2, 4))
        results.extend(items)

    # Save results
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    with open(RESULTS_FILE, "w") as f:
        json.dump(sorted(results, key=lambda x: x["title"].lower()), f, indent=2)

    update_status("last_search")
    print(f"Search complete. Found {len(results)} items.")


if __name__ == "__main__":
    run_scheduled_search()
