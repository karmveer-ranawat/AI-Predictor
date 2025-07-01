from kiteconnect import KiteConnect
from dotenv import load_dotenv
import os, json

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
TOKEN_FILE = "../token.json"

kite = KiteConnect(api_key=api_key)

def save_token(data):
    data = {k: (v.isoformat() if hasattr(v, 'isoformat') else v) for k, v in data.items()}
    with open(TOKEN_FILE, "w") as f:
        json.dump(data, f)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return json.load(f)
    return None

def login_and_cache():
    print("Login URL:", kite.login_url())
    request_token = input("Enter request token: ")
    session_data = kite.generate_session(request_token, api_secret)
    save_token(session_data)
    kite.set_access_token(session_data["access_token"])
    return kite

def get_kite():
    token_data = load_token()
    if token_data:
        try:
            kite.set_access_token(token_data["access_token"])
            kite.profile()  # test validity
            return kite
        except:
            print("Cached token invalid. Logging in again.")
    return login_and_cache()