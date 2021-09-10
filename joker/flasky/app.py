#!/usr/bin/env python3
# coding: utf-8

import flask
# noinspection PyPackageRequirements
import werkzeug.exceptions

from joker.flasky import errors, viewutils
from joker.flasky.loggers import ErrorInterface
from joker.flasky.viewutils import decorate_all_view_funcs


class Application(flask.Flask):
    json_encoder = viewutils.JSONEncoderPlus
    decorate_all_view_funcs = decorate_all_view_funcs
    serialize_current_session = viewutils.serialize_current_session

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_interface = None

    def fmt_error_key_query_url(self, error_key: str, **kwargs):
        bp = self.blueprints.get('_admin')
        if not bp or bp.import_name != 'joker.flasky.views.admin_views':
            return
        return flask.url_for(
            '_admin.admin_query_error',
            error_key=error_key, _external=True, **kwargs
        )

    def use_default_error_handlers(self, error_interface: ErrorInterface):
        if self.error_interface is not None:
            return
        self.error_interface = error_interface

        @self.errorhandler(errors.KnownError)
        def on_known_error(error: errors.KnownError):
            return error.to_dict()

        @self.errorhandler(Exception)
        def on_error(error: Exception):
            # https://flask.palletsprojects.com/en/2.0.x/errorhandling/#generic-exception-handlers
            if isinstance(error, werkzeug.exceptions.HTTPException):
                return error
            errinfo = error_interface.dump()
            info = errinfo.to_dict()
            if url := self.fmt_error_key_query_url(errinfo.error_key):
                info['_url'] = url
            return info


__all__ = ['Application']
