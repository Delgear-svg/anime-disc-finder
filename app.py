import streamlit as st
import pandas as pd
from scraper import search_amazon_com, search_amazon_jp, search_crunchyroll_store, search_ebay
from mal_sync import fetch_mal_list
from sheets import load_want_list, load_do_not_want_list
from scheduler import get_scheduler_status, save_scheduler_settings, load_scheduler_settings
import time
import random

st.set_page_config(page_title="Anime Disc Finder", layout="wide")
st.title("🎬 Anime Disc Finder")

# Load settings
settings = load_scheduler_settings()

# Sidebar controls
with st.sidebar:
    st.header("Settings")

    st.subheader("🔄 Auto-Refresh")
    auto_refresh = st.toggle("Enable auto-refresh (twice monthly)", value=settings.get("auto_refresh", True))

    st.subheader("🏪 Store Toggles")
    enable_amazon_com = st.toggle("Amazon.com", value=settings.get("amazon_com", True))
    enable_amazon_jp = st.toggle("Amazon.co.jp", value=settings.get("amazon_jp", True))
    enable_crunchyroll = st.toggle("Crunchyroll Store", value=settings.get("crunchyroll", True))
    enable_ebay = st.toggle("eBay (fallback)", value=settings.get("ebay", True))

    # Save settings if changed
    new_settings = {
        "auto_refresh": auto_refresh,
        "amazon_com": enable_amazon_com,
        "amazon_jp": enable_amazon_jp,
        "crunchyroll": enable_crunchyroll,
        "ebay": enable_ebay,
    }
    if new_settings != settings:
        save_scheduler_settings(new_settings)

    st.divider()

    if st.button("🔄 Refresh MAL List"):
        with st.spinner("Fetching from MyAnimeList..."):
            titles = fetch_mal_list()
            st.session_state["mal_titles"] = titles
            st.success(f"Loaded {len(titles)} titles from MAL")

    if st.button("🔍 Search Stores Now"):
        st.session_state["searching"] = True

    st.divider()
    status = get_scheduler_status()
    st.caption(f"Last MAL refresh: {status.get('last_mal_refresh', 'Never')}")
    st.caption(f"Last search: {status.get('last_search', 'Never')}")

# Load lists
want_list = load_want_list()
do_not_want_list = load_do_not_want_list()

# Get MAL titles
if "mal_titles" not in st.session_state:
    st.session_state["mal_titles"] = []

# Filter: MAL titles minus "do not want"
titles_to_search = [
    t for t in st.session_state["mal_titles"]
    if t.lower() not in [d.lower() for d in do_not_want_list]
]
titles_to_search = list(set(titles_to_search + want_list))
titles_to_search.sort()

st.sidebar.write(f"**Titles to search:** {len(titles_to_search)}")

# Search and display
if st.session_state.get("searching") and titles_to_search:
    results = []
    progress = st.progress(0)
    for i, title in enumerate(titles_to_search):
        items = []
        if enable_amazon_com:
            items.extend(search_amazon_com(title))
            time.sleep(random.uniform(1, 2))
        if enable_amazon_jp:
            items.extend(search_amazon_jp(title))
            time.sleep(random.uniform(1, 2))
        if enable_crunchyroll:
            items.extend(search_crunchyroll_store(title))
            time.sleep(random.uniform(1, 2))
        if enable_ebay and not items:
            items.extend(search_ebay(title))
            time.sleep(random.uniform(1, 2))
        results.extend(items)
        progress.progress((i + 1) / len(titles_to_search))
    st.session_state["results"] = sorted(results, key=lambda x: x["title"].lower())
    st.session_state["searching"] = False

# Load cached results from cron if no manual search done yet
if "results" not in st.session_state:
    import json, os
    cached = "/app/data/results.json"
    if os.path.exists(cached):
        with open(cached) as f:
            st.session_state["results"] = json.load(f)

# Display results
if "results" in st.session_state and st.session_state["results"]:
    st.header(f"Found {len(st.session_state['results'])} items")
    for item in st.session_state["results"]:
        col1, col2 = st.columns([1, 3])
        with col1:
            if item.get("image"):
                st.image(item["image"], width=120)
        with col2:
            st.subheader(item["title"])
            st.write(f"**Price:** {item['price']}")
            st.write(f"**Format:** {item['format']}")
            st.write(f"**Store:** {item['store']}")
            st.write(f"**Availability:** {item['availability']}")
            if item.get("url"):
                st.markdown(f"[View listing]({item['url']})")
        st.divider()
elif "results" in st.session_state:
    st.info("No results found.")
