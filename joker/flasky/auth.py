#!/usr/bin/env python3
# coding: utf-8

import flask
import re
import hashlib
import time
from joker.flasky import errors, viewutils
from joker.flasky.viewutils import RequestBoundSingletonMeta
import functools


def _make_salt():
    return hex(int(time.time() * 65555))[-10:][::-1]


class HashedPassword(object):
    def __init__(self, digest: str, algo: str, salt: str):
        self.digest = digest
        self.algo = algo
        self.salt = salt

    @classmethod
    def parse(cls, hp_string: str):
        digest, algo, salt = hp_string.split(':')
        return cls(digest, algo, salt)

    @classmethod
    def generate(cls, password: str, algo: str = 'sha256', salt: str = None):
        if salt is None:
            salt = _make_salt()
        p = password.encode('utf-8')
        s = salt.encode('utf-8')
        h = hashlib.new(algo, p + s)
        return cls(h.hexdigest(), algo, salt)

    def __str__(self):
        return '{}:{}:{}'.format(self.digest, self.algo, self.salt)

    def verify(self, password: str):
        hp1 = self.generate(password, self.algo, self.salt)
        return self.digest == hp1.digest


class LoginInterfaceBase(metaclass=RequestBoundSingletonMeta):
    _user_id_session_key = 'user_id'
    _not_logged_in_message = 'You are not logged-in.'

    def __init__(self, user_id, user_info=None):
        self.user_id = user_id
        self.user_info = user_info

    @staticmethod
    def _get_default_user_id():
        return

    @classmethod
    def get_current_user_id(cls):
        if user_id := flask.session.get('user_id'):
            return user_id
        elif user_id := cls._get_default_user_id():
            return user_id
        else:
            raise errors.OperationalError(cls._not_logged_in_message)

    @classmethod
    def check(cls):
        return cls(cls.get_current_user_id())

    @classmethod
    def login_required(cls, func):
        """Decorate a view function to ensure user logged-in."""

        @functools.wraps(func)
        def _func(*args, **kwargs):
            cls.get_current_user_id()
            return func(*args, **kwargs)

        return _func

    @classmethod
    def _login(cls, user_id):
        flask.session[cls._user_id_session_key] = user_id
        return cls(user_id)

    @classmethod
    def _logout(cls):
        flask.session.pop(cls._user_id_session_key)

    @staticmethod
    def serialize_current_session():
        return viewutils.serialize_current_session()

    @staticmethod
    def guess_name_type(login_name):
        if re.match(r'\+?\d+[\d-]+', login_name):
            return 'phone'
        # xxxxx@xxxxx.xxx => an email address
        elif re.match(
                r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$',
                login_name):
            return 'email'
