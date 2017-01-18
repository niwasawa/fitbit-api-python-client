#!/usr/bin/python3

import urllib.parse

from mycommon import JsonFile


def get_fitbit_auth_url(auth_url, scope, client_id, redirect_uri):

  # Using OAuth 2.0 — Fitbit Web API Docs
  # Authorization Code Grant Flow: Authorization Page
  # https://dev.fitbit.com/docs/oauth2/#authorization-page

  params = {
    "client_id" : client_id,
    "response_type" : "code",
    "scope" : scope,
    "redirect_uri" : redirect_uri,
  }

  qs = urllib.parse.urlencode(params)

  return auth_url + "?" + qs


auth_url = "https://www.fitbit.com/oauth2/authorize"
scope = "activity heartrate location nutrition profile settings sleep social weight"
auth = JsonFile("fitbit-auth.json").read()

fitbit_auth_url = get_fitbit_auth_url(auth_url, scope, auth["client_id"], auth["callback_url"])
print("{}".format(fitbit_auth_url))

