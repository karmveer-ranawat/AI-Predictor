from kiteconnect import KiteConnect
from dotenv import load_dotenv
import os
import json
from datetime import datetime

# Load credentials
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

TOKEN_FILE = "token.json"

# Initialize KiteConnect
kite = KiteConnect(api_key=api_key)


def save_token(token_data):
    # Convert datetime fields to string
    for key, value in token_data.items():
        if isinstance(value, datetime):
            token_data[key] = value.isoformat()

    with open(TOKEN_FILE, "w") as f:
        json.dump(token_data, f)


def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None


def login_and_cache():
    print("🔗 Login here:", kite.login_url())
    request_token = input("📥 Enter request_token: ")
    token_data = kite.generate_session(request_token=request_token, api_secret=api_secret)
    save_token(token_data)
    kite.set_access_token(token_data["access_token"])
    print("✅ New access_token saved!")
    return token_data["access_token"]


def get_kite():
    token_data = load_token()
    if token_data:
        try:
            kite.set_access_token(token_data["access_token"])
            # Check validity by calling a lightweight API
            kite.profile()
            print("✅ Using cached access_token")
            return kite
        except Exception as e:
            print("⚠️ Cached token invalid or expired. Re-login needed.")

    # Manual login flow
    access_token = login_and_cache()
    kite.set_access_token(access_token)
    return kite


# --- Usage Example ---
if __name__ == "__main__":
    kite = get_kite()
    user = kite.profile()
    print("👤 Logged in as:", user["user_name"])
