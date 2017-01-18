#!/usr/bin/python3

import base64
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from mycommon import JsonFile


def get_auth_value(client_id, client_secret):

    a = "{}:{}".format(client_id, client_secret)
    b = base64.encodestring(a.encode("utf-8"))[:-1]
    return "Basic {}".format(b.decode("utf-8"))


def get_refreshed_access_token_json(token_url, refresh_token, auth_value):

    # Using OAuth 2.0 — Fitbit Web API Docs
    # Refreshing Tokens
    # https://dev.fitbit.com/docs/oauth2/#refreshing-tokens

    params = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }

    body = urlencode(params).encode("utf-8")

    req = Request(token_url)
    req.add_header("Authorization", auth_value)
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        # HTTP POST
        res = urlopen(req, body)
    except URLError as e:
        print(e)
        content = e.read().decode("utf-8")
        e.close()
        return content
    else:
        content = res.read().decode("utf-8")
        res.close()
        return content

jsonfile = JsonFile("fitbit-auth.json")
auth = jsonfile.read()
client_id = auth["client_id"]
client_secret = auth["client_secret"]
token_url = "https://api.fitbit.com/oauth2/token"
refresh_token = auth["refresh_token"]

auth_value = get_auth_value(client_id, client_secret)
print(auth_value)

access_token_json = get_refreshed_access_token_json(
    token_url, refresh_token, auth_value)
print(access_token_json)
