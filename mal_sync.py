import requests
from bs4 import BeautifulSoup

MAL_URL = "https://myanimelist.net/animelist/Delgear?status=7"


def fetch_mal_list():
    """Scrape anime titles from MAL public list."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    titles = []
    try:
        resp = requests.get(MAL_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        # MAL renders list data in a JSON blob in the page
        import json
        import re
        match = re.search(r'data-items="([^"]*)"', resp.text)
        if match:
            data = match.group(1).replace("&quot;", '"')
            items = json.loads(data)
            for item in items:
                title = item.get("anime_title", "")
                if title:
                    titles.append(title)
        else:
            # Fallback: parse table rows
            rows = soup.select(".list-table-data .data.title .link")
            for row in rows:
                titles.append(row.get_text(strip=True))
    except Exception as e:
        print(f"MAL fetch error: {e}")
    return titles
