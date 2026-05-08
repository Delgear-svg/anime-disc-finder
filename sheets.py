import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
CREDENTIALS_FILE = "/app/credentials/google_service_account.json"

# Set these to your Google Sheet IDs or URLs
WANT_SHEET_ID = ""  # Your "I want" sheet ID
DO_NOT_WANT_SHEET_ID = ""  # Your "Do not want" sheet ID


def _get_client():
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return gspread.authorize(creds)


def load_want_list():
    """Load titles from the 'I want' Google Sheet."""
    if not WANT_SHEET_ID:
        return []
    try:
        client = _get_client()
        sheet = client.open_by_key(WANT_SHEET_ID).sheet1
        # Assumes titles are in column A
        return [row for row in sheet.col_values(1) if row.strip()]
    except Exception as e:
        print(f"Error loading want list: {e}")
        return []


def load_do_not_want_list():
    """Load titles from the 'Do not want' Google Sheet."""
    if not DO_NOT_WANT_SHEET_ID:
        return []
    try:
        client = _get_client()
        sheet = client.open_by_key(DO_NOT_WANT_SHEET_ID).sheet1
        return [row for row in sheet.col_values(1) if row.strip()]
    except Exception as e:
        print(f"Error loading do-not-want list: {e}")
        return []
