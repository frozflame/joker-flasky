#!/usr/bin/env python3
# coding: utf-8

import flask

from joker.flasky.viewutils import JSONEncoderPlus


def decorate_all_view_funcs(app, decorator):
    keys = list(app.view_functions)
    for key in keys:
        func = app.view_functions[key]
        app.view_functions[key] = decorator(func)


class FlaskPlus(flask.Flask):
    json_encoder = JSONEncoderPlus

    def decorate_all_view_funcs(self, decorator):
        decorate_all_view_funcs(self, decorator)
