""" This module implements the base for OBMd client library. """

from urlparse import urljoin
import json
import re
import inspect


class BadArgumentError(Exception):
    """Indicate bad arguments"""


class FailedAPICallException(Exception):
    """An exception indicating that the server returned an error.
    Attributes:
        error_type (str): the type of the error.
        message (str): a human readble description of the error.
    """

    def __init__(self, error_type, message):
        Exception.__init__(self, message)
        self.error_type = error_type


def object_url(endpoint, *args):
    """Generate URL from combining endpoint and args as relative URL"""
    rel = "/".join(args)
    url = urljoin(endpoint, rel)
    return url


def check_response(response):
    """
    Check the response from an API call, and do any needed error handling
    Returns the body of the response as (parsed) JSON, or None if there
    was no body. Raises a FailedAPICallException on any non 2xx status.
    """
    if 200 <= response.status_code < 300:
        try:
            return json.loads(response.content)
        except ValueError:  # No JSON request body; typical
                            # For methods PUT, POST, DELETE
            return

    try:
        e = json.loads(response.content)
        raise FailedAPICallException(
            error_type=e['type'],
            message=e['msg'],
        )
    # Catching responses that do not return JSON, and raise a stand-in
    # error.
    except ValueError:
        raise FailedAPICallException(
            error_type="code: " + str(response.status_code),
            message=response.content,
        )
