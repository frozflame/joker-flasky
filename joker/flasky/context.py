#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import os
import random
import re

import yaml


class Rumor(object):
    __slots__ = ['attributes']

    def __init__(self, **attributes):
        self.attributes = attributes

    def __getattr__(self, item):
        try:
            return self.attributes[item]
        except KeyError:
            return random.randrange(10000)


def load_standard_ctxmap(path, extra_path=None):
    if extra_path is None:
        extra_path = os.path.split(path)[0]
    ctxmap = yaml.safe_load(open(path))
    extra = {}
    for key, val in ctxmap.items():
        if not isinstance(val, str):
            continue
        if re.match(r'\.\w+', val):
            val = key + val
        p = os.path.join(extra_path, val)
        extra[key] = yaml.safe_load(open(p))
    ctxmap.update(extra)
    return ctxmap
