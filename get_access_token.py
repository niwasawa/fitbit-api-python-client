#!/usr/bin/python3

import base64
import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from mycommon import JsonFile


def get_auth_value(client_id, client_secret):

    a = "{}:{}".format(client_id, client_secret)
    b = base64.encodestring(a.encode("utf-8"))[:-1]
    return "Basic {}".format(b.decode("utf-8"))


def get_access_token_json(token_url, code, auth_value, redirect_uri):

    # Using OAuth 2.0 — Fitbit Web API Docs
    # Authorization Code Grant Flow: Access Token Request
    # https://dev.fitbit.com/docs/oauth2/#access-token-request

    params = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
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


token_url = "https://api.fitbit.com/oauth2/token"

jsonfile = JsonFile("fitbit-auth.json")
auth = jsonfile.read()

auth_value = get_auth_value(auth["client_id"], auth["client_secret"])
print(auth_value)

access_token_json = get_access_token_json(
    token_url, auth["code"], auth_value, auth["callback_url"])
print(access_token_json)

data = json.loads(access_token_json)
auth["access_token"] = data["access_token"]
auth["refresh_token"] = data["refresh_token"]
auth["user_id"] = data["user_id"]
jsonfile.write(auth)
