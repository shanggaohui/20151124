# coding: utf8

import datetime
import copy

from flask import json, Response
from playhouse.shortcuts import model_to_dict

default_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS, DELETE',
    'Access-Control-Allow-Credentials': 'true',
    'Content-Type': 'application/json',
    "Access-Control-Allow-Headers": "Content-Type, X-Requested-With",
}


def not_valid_user():
    return error('not valid user')


def not_allowed():
    return error('not allowed')


def not_found(reason='not found'):
    return error(reason)


def jsonify(data, status_code=200):
    res = Response(json.dumps(data, default=default_json_format))
    # res = Response(json.dumps(data))
    res.headers = default_headers
    res.status = str(status_code)
    return res


def ok(content=''):
    msg = {
        'status': 'ok',
        'content': content,
    }
    res = jsonify(msg)
    return res


def error(error='', status_code=400):
    if isinstance(error, (tuple, list)):
        msg = {
            'status': 'error',
            'code': error[0],
            'msg': error[1],
        }
    else:
        msg = {
            'status': 'error',
            'msg': error,
        }

    res = jsonify(msg, status_code=status_code)
    return res


def redirect(location):
    headers = copy.copy(default_headers)
    headers['Location'] = location
    res = Response()
    res.status = '302'
    res.headers.extend(headers)
    return res


def default_json_format(obj):
    """Default JSON serializer."""
    if isinstance(obj, datetime.datetime):
        obj = str(obj)
    if isinstance(obj, int):
        obj = str(obj)
    if isinstance(obj, datetime.date):
        obj = str(obj)
    if obj.__class__.__name__ == "Order":
        return model_to_dict(obj, recurse=False)
    if obj.__class__.__name__ == "Shop":
        return model_to_dict(obj, recurse=False)
    if obj.__class__.__name__ == "Address":
        return model_to_dict(obj, recurse=False)

    return obj
