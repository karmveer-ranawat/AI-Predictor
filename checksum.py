import hashlib
from dotenv import load_dotenv
import os

load_dotenv()

def get_checksum(request_token):
    # Your three variables
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")

    # Concatenate them in the required order
    combined = api_key + request_token + api_secret

    # Generate SHA-256 hash
    hash_object = hashlib.sha256(combined.encode())
    combined_checksum = hash_object.hexdigest()

    return combined_checksum

checksum = get_checksum("request_token")
print(checksum)