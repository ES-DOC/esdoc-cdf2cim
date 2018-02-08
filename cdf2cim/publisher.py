# -*- coding: utf-8 -*-

"""
.. module:: publisher.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishes cdf2cim data to web-service.

.. moduleauthor:: David Hassell <david.hassell@ncas.ac.uk>


"""
import json

import requests

from cdf2cim.constants import HTTP_RESPONSE_AUTHENTICATION_ERROR
from cdf2cim.constants import HTTP_RESPONSE_AUTHORIZATION_ERROR
from cdf2cim.exceptions import ClientError
from cdf2cim.exceptions import WebServiceAuthenticationError
from cdf2cim.exceptions import WebServiceAuthorizationError
from cdf2cim.exceptions import WebServiceConnectionError
from cdf2cim.exceptions import WebServiceProcessingError
from cdf2cim.options import WS_ACCESS_TOKEN
from cdf2cim.options import WS_HOST
from cdf2cim.options import WS_USER



def execute(fpath):
    """Uploads target to cdf2cim web-service.

    :param str fpath: Path to a previously saved cdf2cim file.

    :returns: Exception if an exception occurred otherwise None.
    :rtype: Exception | None

    """
    # Prepare request info.
    payload = _get_payload(fpath)
    endpoint = _get_endpoint(payload['mip_era'])
    credentials = (WS_USER, WS_ACCESS_TOKEN)
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
    except Exception as err:
        raise ClientError(err)
    else:
        if r.status_code == HTTP_RESPONSE_AUTHENTICATION_ERROR:
            raise WebServiceAuthenticationError()
        elif r.status_code == HTTP_RESPONSE_AUTHORIZATION_ERROR:
            raise WebServiceAuthorizationError()
        elif r.status_code != 200:
            raise WebServiceProcessingError(r.status_code, r.text)


def verify_credentials():
    """Verifies that passed credentials are deemed valid by ES-DOC cdf2cim web-service.

    """
    # Prepare request info.
    endpoint = "{}/verify-authorization".format(WS_HOST)
    params = {
        'login': WS_USER,
        'token': WS_ACCESS_TOKEN
    }

    # Post to web-service.
    try:
        r = requests.get(endpoint, params=params)
    except requests.exceptions.ConnectionError:
        raise WebServiceConnectionError()
    except Exception as err:
        raise ClientError(err)
    else:
        if r.status_code == HTTP_RESPONSE_AUTHENTICATION_ERROR:
            raise WebServiceAuthenticationError()
        elif r.status_code == HTTP_RESPONSE_AUTHORIZATION_ERROR:
            raise WebServiceAuthorizationError()
        elif r.status_code != 200:
            raise WebServiceProcessingError(r.status_code, r.text)


def _get_payload(fpath):
    """Returns JSON payload to be posted to web-service.

    """
    with open(fpath, 'r') as fstream:
        return json.loads(fstream.read())


def _get_endpoint(mip_era):
    """Returns web-service endpoint.

    """
    return "{}/1/{}".format(WS_HOST, mip_era.lower())
