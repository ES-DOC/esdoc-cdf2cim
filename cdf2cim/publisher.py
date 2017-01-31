# -*- coding: utf-8 -*-

"""
.. module:: publish.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishes cdf2cim data to web-service.

.. moduleauthor:: David Hassel <david.hassell@ncas.ac.uk>


"""
import json
import os

import requests

from cdf2cim.file_io import encode
from cdf2cim.exceptions import WebServiceConnectionError
from cdf2cim.exceptions import WebServiceProcessingError

# Default web-service host.
_DEFAULT_WS_HOST = r"https://cdf2cim.ws.es-doc.org"

# Environment variable: web-service host (optional)
_ENV_VAR_WS_HOST = "CDF2CIM_WS_HOST"

# Environment variable: GitHub user.
_ENV_VAR_GH_USER = "CDF2CIM_CLIENT_GITHUB_USER"

# Environment variable: GitHub access token.
_ENV_VAR_GH_ACCESS_TOKEN = "CDF2CIM_CLIENT_GITHUB_ACCESS_TOKEN"



def execute(target):
    """Uploads target to cdf2cim web-service.

    """
    # Prepare request.
    payload = _get_payload(target)
    endpoint = _get_ws_endpoint(payload['mip_era'])
    credentials = _get_ws_credentials()
    headers = {'Content-Type': 'application/json'}

    # Post to web-service.
    try:
        r = requests.post(
            endpoint,
            data=json.dumps(payload),
            headers=headers,
            auth=credentials
            )
    except requests.exceptions.ConnectionError:
        raise WebServiceConnectionError()

    # Validate web-service response.
    if r.status_code != 200:
        raise WebServiceProcessingError(r.status_code, r.text)


def _get_payload(target):
    """Returns JSON payload to be posted to server.

    """
    if os.path.isfile(target):
        with open(target, 'r') as fstream:
            return json.loads(fstream.read())

    return encode(target)


def _get_ws_endpoint(mip_era):
    """Returns web-service endpoint.

    """
    return "{}/1/{}".format(_get_ws_host(), mip_era.lower())


def _get_ws_host():
    """Returns web-service host.

    """
    host = os.getenv(_ENV_VAR_WS_HOST)

    return host if host is not None else _DEFAULT_WS_HOST


def _get_ws_credentials():
    """Returns web-service credentials.

    """
    return os.getenv(_ENV_VAR_GH_USER), os.getenv(_ENV_VAR_GH_ACCESS_TOKEN)
