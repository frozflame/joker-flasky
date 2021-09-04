#!/usr/bin/env python3
# coding: utf-8

import flask
from flask import Blueprint, current_app

from joker.flasky.loggers import ErrorInterface
from joker.flasky.viewutils import respond, respond_plain_text

bp = Blueprint('_admin', __name__)


@bp.route('/r')
def admin_raise_error():
    raise RuntimeError('error raised intentionally')


@bp.route('/g')
def admin_g():
    return vars(flask.g)


@bp.route('/site-map')
def admin_site_map():
    """
    site-map
    """
    urls = [r.rule for r in current_app.url_map.iter_rules()]
    urls.sort()
    if flask.request.args.get('fmt') == 'text':
        text = '\n'.join(urls)
        return respond_plain_text(text)
    return respond(urls)


@bp.route('/e/<error_key>')
def admin_query_error(error_key: str):
    ei = getattr(current_app, 'error_interface')
    if isinstance(ei, ErrorInterface):
        info = ei.query(error_key)
        exc = info.get("exc")
        if 'i' in flask.request.args:
            if isinstance(exc, str):
                info['excl'] = exc.splitlines()
            return info
        url = flask.url_for(
            flask.request.url_rule.endpoint,
            error_key=error_key
        )
        return f'<pre>{exc}<br/><a href="{url}?i">{error_key}</a></pre>'
