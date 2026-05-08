# Anime Disc Finder v1.0

Searches Amazon.com, Amazon.co.jp, Crunchyroll Store, and eBay (fallback) for DVD/Blu-ray of anime from your [MyAnimeList](https://myanimelist.net/animelist/Delgear?status=7).

## Features

- Pulls anime titles from your MAL profile
- Cross-references a Google Sheet "want list" and "do not want list"
- Searches multiple stores with individual on/off toggles
- Auto-refreshes on the 1st and 15th of each month
- Displays results with cover image, price, format, and store link (A-Z)
- Runs in Docker, designed for TrueNAS + Dockge deployment

## Quick Start

### Prerequisites

- Docker and Docker Compose (or Dockge)
- A Google Cloud service account with Sheets API access
- Two Google Sheets (want list & do not want list) with titles in column A

### Setup

1. **Clone the repo:**
   ```bash
   git clone https://github.com/Delgear-svg/anime-disc-finder.git
   cd anime-disc-finder
   ```

2. **Google Sheets API credentials:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project → enable Google Sheets API
   - Create a Service Account → download JSON key
   - Place it at `./credentials/google_service_account.json`
   - Share both Google Sheets with the service account email

3. **Configure Sheet IDs:**
   Edit `sheets.py` and set:
   ```python
   WANT_SHEET_ID = "your-want-sheet-id"
   DO_NOT_WANT_SHEET_ID = "your-do-not-want-sheet-id"
   ```
   The sheet ID is the long string in the URL: `https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit`

4. **Run:**
   ```bash
   docker compose up --build -d
   ```

5. **Open:** http://localhost:8501

### TrueNAS + Dockge Deployment

1. Build and push the image:
   ```bash
   docker build -t your-dockerhub-user/anime-disc-finder:latest .
   docker push your-dockerhub-user/anime-disc-finder:latest
   ```

2. Create directories on TrueNAS:
   ```
   /mnt/pool/apps/anime-disc-finder/credentials/  ← google_service_account.json
   /mnt/pool/apps/anime-disc-finder/data/          ← auto-populated
   ```

3. In Dockge, create a stack with:
   ```yaml
   version: "3.8"
   services:
     anime-disc-finder:
       image: your-dockerhub-user/anime-disc-finder:latest
       container_name: anime-disc-finder
       ports:
         - "8501:8501"
       volumes:
         - /mnt/pool/apps/anime-disc-finder/credentials:/app/credentials:ro
         - /mnt/pool/apps/anime-disc-finder/data:/app/data
       restart: unless-stopped
   ```

4. Start the stack. Access at `http://<truenas-ip>:8501`

## Usage

1. Click **Refresh MAL List** to pull your anime list
2. Toggle stores on/off in the sidebar
3. Click **Search Stores Now** to search
4. Toggle **auto-refresh** to enable/disable the twice-monthly cron job

## Notes

- eBay is only searched if no other enabled store returns results for a title
- Delays between requests are built in to reduce rate-limiting
- Amazon may occasionally block scraping — results will be empty for that run
- Cron runs at 3:00 AM on the 1st and 15th of each month

## License

MIT
