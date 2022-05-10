#!/usr/bin/env python3
# coding: utf-8

from joker.flasky.environ import JokerInterface

ji = JokerInterface()


def respond_login_page(username: str = '', password: str = ''):
    tpl = ji.jinja2_env.get_template('login.html')
    return tpl.render(username=username, password=password)


def respond_upload_page(label=None):
    tpl = ji.jinja2_env.get_template('upload.html')
    return tpl.render(label=label)
