#!/usr/bin/env python3
# coding: utf-8

import datetime
import decimal
import mimetypes
import re

import flask
import flask.views
from flask import request
from volkanic.utils import merge_dicts


def infer_mime_type(filename: str, default="text/plain") -> str:
    if filename.startswith('.'):
        filename = '_' + filename
    return mimetypes.guess_type(filename)[0] or default


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


def respond_plain_text(text: str):
    resp = flask.make_response(text, 200)
    resp.mimetype = "text/plain"
    return resp


def respond_with_pre_gzipped(content: bytes, content_type=None):
    content_type = content_type or 'text/plain'
    resp = flask.make_response(content)
    resp.headers.set('Content-Type', content_type)
    resp.headers['Content-Encoding'] = 'gzip'
    return resp


def respond_xaccel_redirect(path: str, filename: str = None):
    # nginx: http://wiki.nginx.org/NginxXSendfile
    resp = flask.make_response()
    headers = {
        'X-Accel-Redirect': path,
        'Cache-Control': 'no-cache',
        'Content-Type': infer_mime_type(path, 'application/octet-stream'),
        'Content-Disposition':
            f'attachment; filename={filename}' if filename else 'inline',
    }
    resp.headers.update(headers)
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
    return merge_dicts(data, request.args)


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


_datetime_fmt = '%Y-%m-%d %H:%M:%S'


def _json_default(o):
    if isinstance(o, decimal.Decimal):
        return float(o)
    if isinstance(o, datetime.timedelta):
        return o.total_seconds()
    if isinstance(o, datetime.date) and not isinstance(o, datetime.datetime):
        return o.isoformat()
    if hasattr(o, 'as_json_serializable'):
        return o.as_json_serializable()
    raise TypeError


def json_default(o):
    """usage: json.dumps(some_o, default=json_default)"""
    try:
        return _json_default(o)
    except TypeError:
        pass
    if isinstance(o, datetime.datetime):
        return o.strftime(_datetime_fmt)
    return str(o)


class JSONEncoderPlus(flask.json.JSONEncoder):
    datetime_fmt = _datetime_fmt

    def default(self, o):
        try:
            return _json_default(o)
        except TypeError:
            pass
        if isinstance(o, datetime.datetime):
            return o.strftime(self.datetime_fmt)
        return super().default(o)


def serialize_current_session(app: flask.Flask = None):
    if app is None:
        app = flask.current_app
    ss = app.session_interface.get_signing_serializer(app)
    return ss.dumps(dict(flask.session))


class RequestBoundSingletonMeta(type):
    def __call__(cls, *args, **kwargs):
        cache = flask.g.setdefault('request_bound_cache', {})
        try:
            return cache[cls]
        except KeyError:
            obj = super().__call__(*args, **kwargs)
            return cache.setdefault(cls, obj)


def is_mobile():
    _regex_ua_mobile = re.compile(
        "Mobile|iP(hone|od|ad)|Android|BlackBerry|IEMobile|Kindle"
        "|NetFront|Silk-Accelerated|(hpw|web)OS|Fennec|Minimo"
        "|Opera M(obi|ini)|Blazer|Dolfin|Dolphin|Skyfire|Zune"
    )
    ua = flask.request.headers.get('User-Agent', '')
    return _regex_ua_mobile.search(ua)
