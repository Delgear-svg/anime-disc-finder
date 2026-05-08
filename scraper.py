import requests
from bs4 import BeautifulSoup
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def search_amazon_com(title):
    """Search Amazon.com for DVD/Bluray of a title."""
    query = f"{title} anime Blu-ray DVD"
    url = f"https://www.amazon.com/s?k={requests.utils.quote(query)}&i=movies-tv"
    results = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select('[data-component-type="s-search-result"]')
        for item in items[:3]:
            title_el = item.select_one("h2 a span")
            price_el = item.select_one(".a-price .a-offscreen")
            img_el = item.select_one("img.s-image")
            link_el = item.select_one("h2 a")
            if title_el:
                results.append({
                    "title": title_el.get_text(strip=True),
                    "price": price_el.get_text(strip=True) if price_el else "N/A",
                    "image": img_el["src"] if img_el else None,
                    "url": "https://www.amazon.com" + link_el["href"] if link_el else None,
                    "store": "Amazon.com",
                    "format": "DVD/Blu-ray",
                    "availability": "Available" if price_el else "Check listing",
                })
    except Exception as e:
        print(f"Amazon.com error for '{title}': {e}")
    return results


def search_amazon_jp(title):
    """Search Amazon.co.jp for DVD/Bluray of a title."""
    query = f"{title} Blu-ray DVD"
    url = f"https://www.amazon.co.jp/s?k={requests.utils.quote(query)}&i=dvd"
    results = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select('[data-component-type="s-search-result"]')
        for item in items[:3]:
            title_el = item.select_one("h2 a span")
            price_el = item.select_one(".a-price .a-offscreen")
            img_el = item.select_one("img.s-image")
            link_el = item.select_one("h2 a")
            if title_el:
                results.append({
                    "title": title_el.get_text(strip=True),
                    "price": price_el.get_text(strip=True) if price_el else "N/A",
                    "image": img_el["src"] if img_el else None,
                    "url": "https://www.amazon.co.jp" + link_el["href"] if link_el else None,
                    "store": "Amazon.co.jp",
                    "format": "DVD/Blu-ray",
                    "availability": "Available" if price_el else "Check listing",
                })
    except Exception as e:
        print(f"Amazon.co.jp error for '{title}': {e}")
    return results


def search_crunchyroll_store(title):
    """Search Crunchyroll store for DVD/Bluray."""
    query = f"{title}"
    url = f"https://store.crunchyroll.com/search?q={requests.utils.quote(query)}&category=home-video"
    results = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select(".product-tile")
        for item in items[:3]:
            title_el = item.select_one(".product-tile__title")
            price_el = item.select_one(".product-tile__price")
            img_el = item.select_one("img")
            link_el = item.select_one("a")
            if title_el:
                results.append({
                    "title": title_el.get_text(strip=True),
                    "price": price_el.get_text(strip=True) if price_el else "N/A",
                    "image": img_el["src"] if img_el else None,
                    "url": "https://store.crunchyroll.com" + link_el["href"] if link_el else None,
                    "store": "Crunchyroll Store",
                    "format": "DVD/Blu-ray",
                    "availability": "Available" if price_el else "Check listing",
                })
    except Exception as e:
        print(f"Crunchyroll error for '{title}': {e}")
    return results


def search_ebay(title):
    """Search eBay for DVD/Bluray (fallback if not found elsewhere)."""
    query = f"{title} anime Blu-ray DVD"
    url = f"https://www.ebay.com/sch/i.html?_nkw={requests.utils.quote(query)}&_sacat=617"
    results = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        items = soup.select(".s-item")
        for item in items[:3]:
            title_el = item.select_one(".s-item__title")
            price_el = item.select_one(".s-item__price")
            img_el = item.select_one(".s-item__image-img")
            link_el = item.select_one(".s-item__link")
            if title_el and "Shop on eBay" not in title_el.get_text():
                results.append({
                    "title": title_el.get_text(strip=True),
                    "price": price_el.get_text(strip=True) if price_el else "N/A",
                    "image": img_el["src"] if img_el else None,
                    "url": link_el["href"] if link_el else None,
                    "store": "eBay",
                    "format": "DVD/Blu-ray",
                    "availability": "Available",
                })
    except Exception as e:
        print(f"eBay error for '{title}': {e}")
    return results


def search_all_stores(title):
    """Search all stores. Use eBay only if others return nothing."""
    results = []
    results.extend(search_amazon_com(title))
    time.sleep(random.uniform(1, 2))
    results.extend(search_amazon_jp(title))
    time.sleep(random.uniform(1, 2))
    results.extend(search_crunchyroll_store(title))
    time.sleep(random.uniform(1, 2))

    if not results:
        results.extend(search_ebay(title))
        time.sleep(random.uniform(1, 2))

    return results
