import requests
import json
import hmac
import hashlib
import time
from datetime import datetime
import urllib3
from urllib.parse import urlencode


api_key = '1a7ec7b154db00e5d0f659812eb5d55d'
api_secret = '0d8a9b2a2b3d43b8a8261ea17332bff8'

# api_key = '3e9f237e522fb47ad3f78b7f94f671af'
# api_secret = 'e0663ebaa54d1a9fddd65b1b66b49a03'
# https://demo.splynx.com/admin/login/
domain_name = "tj.splynx.app"

t_now = datetime.now()
nonce = round((time.mktime(t_now.timetuple()) + t_now.microsecond / 1000000.0) * 100)
st = "%s%s" % (nonce, api_key)
signature = hmac.new(bytes(api_secret.encode('latin-1')), bytes(st.encode('latin-1')), hashlib.sha256).hexdigest()
BASE_URL = f"https://tj.splynx.app/api/2.0/admin"

def get_access_token():

    auth_data = {
        "auth_type": "admin",
        "login": "admin",
        "password": "SplynxAdewaletj08@#$"
    }

    params = json.dumps(auth_data)

    
    headers = {
        'Content-Type': 'application/json',
    }

    url = f"{BASE_URL}/auth/tokens"

    response = requests.request("POST",url, headers=headers, data=params, verify=True)
    return response.json()['access_token'],response.json()['refresh_token'],response.json()['access_token_expiration']

access_token, refresh_token, access_token_expiration = get_access_token()
print(access_token, refresh_token, access_token_expiration)

