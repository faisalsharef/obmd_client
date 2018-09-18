"""Client support for all obmd related api calls"""
import requests
import os
import json
from base import FailedAPICallException, object_url, check_response

endpoint = os.environ.get('OBMD_ENDPOINT')
user = 'admin'
pw = os.environ.get('OBMD_ADMINTOKEN')


def node_register(node, obm_type, ipmi_ip, ipmi_user, ipmi_passw):
    """Registers a new node"""
    url = object_url(endpoint, 'node', node)
    payload = json.dumps(
        {"type": obm_type,
            "info": {
                "addr": ipmi_ip,
                "user": ipmi_user,
                "ipmi_passw": ipmi_passw
            }
         })
    return check_response(requests.put(url, data=payload, auth=(user, pw)))


def node_delete(node):
    """Delete a node"""
    url = object_url(endpoint, 'node', node)
    return check_response(requests.delete(url, auth=(user, pw)))


def get_token(node):
    """Get node token"""
    url = object_url(endpoint, 'node', node, 'token')
    return check_response(requests.post(url, auth=(user, pw)))


def delete_token(node):
    """Invalidate node token"""
    url = object_url(endpoint, 'node', node, 'token')
    return check_response(requests.delete(url, auth=(user, pw)))
