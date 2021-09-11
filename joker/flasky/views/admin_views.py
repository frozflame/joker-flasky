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


@bp.route('/echo', methods=['GET', 'POST'])
def admin_echo():
    flask.session['a'] = 1
    return {
        # '_': vars(flask.request),
        'method': flask.request.method,
        'headers': dict(flask.request.headers),
        'args': flask.request.args,
        'json': flask.request.json,
        'form': flask.request.form,
    }


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
        if 'i' in flask.request.args:
            return ei.query(error_key, human=True)
        url = flask.url_for(
            flask.request.url_rule.endpoint,
            error_key=error_key, i='',
        )
        return ei.query_html(error_key, url)
