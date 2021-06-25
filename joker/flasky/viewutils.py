#!/usr/bin/env python3
# coding: utf-8

import datetime
import decimal

import flask
import flask.views
from flask import request


def safe_merge_dicts(*dicts):
    retdic = {}
    for dic in dicts:
        retdic.update(dic)
    return retdic


def respond(*args, **kwargs):
    resp = kwargs
    for arg in args:
        if 'message' not in resp and isinstance(arg, str):
            resp['message'] = arg
            continue
        if 'data' not in resp:
            if isinstance(arg, (dict, int, float, str)):
                resp['data'] = arg
                continue
            if isinstance(arg, (list, tuple, set, frozenset)):
                resp['data'] = list(arg)
                continue
        r = repr(arg)
        msg = f'redundant or invalid argument for respond(): {r}'
        raise TypeError(msg)
    if resp.setdefault('code', 0):
        msg = 'for non-zero code, raise DomainError/TechnicalError instead.'
        raise TypeError(msg)
    return resp


def get_request_data(force_json=False):
    if request.method == 'GET':
        return request.args.to_dict()
    if force_json or request.is_json:
        data = request.get_json(force=force_json)
        if not isinstance(data, dict):
            data = {'': data}
    else:
        data = request.form.to_dict()
    return safe_merge_dicts(data, request.args)


class _ReducedViewMixin:
    force_json = False

    def get_request_data(self):
        return get_request_data(self.force_json)


class ReducedView(flask.views.View, _ReducedViewMixin):
    def dispatch_request(self):
        return self.__call__()

    def __call__(self):
        return respond()


class ReducedRestfulView(flask.views.MethodView, _ReducedViewMixin):
    pass


def jsonp(resp, callback):
    return flask.current_app.response_class(
        callback + '(' + flask.json.dumps(resp) + ');\n',
        mimetype='application/javascript'
    )


class JSONEncoderPlus(flask.json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'as_json_serializable'):
            return o.as_json_serializable()
        if isinstance(o, decimal.Decimal):
            return float(o)
        if isinstance(o, datetime.timedelta):
            return o.total_seconds()
        if isinstance(o, (datetime.datetime, datetime.date)):
            return o.isoformat()
        return super(JSONEncoderPlus, self).default(o)
