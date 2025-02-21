import requests
import json
import hmac
import hashlib
import time
from datetime import datetime
import urllib3
from urllib.parse import urlencode
# from splynxGetAccessToken import access_token, refresh_token, access_token_expiration, BASE_URL,headers

domain_name = "tj.splynx.app"
BASE_URL = f"https://tj.splynx.app/api/2.0/admin"

def renew_token(refresh_token):
    url = f"{BASE_URL}/auth/tokens/{refresh_token}"
    headers = {
        'Content-Type': 'application/json',
    }

    new_access_token = requests.get(url,headers=headers)
    return new_access_token.json()['access_token'],new_access_token.json()['refresh_token'],new_access_token.json()['access_token_expiration']

if time.time() + 5 > 1738582731:
    print(renew_token("714deaedd8806cbc7b6bbfd8850888da"))
else:
    print("Token is still valid")
    