#!/usr/bin/env python3
# coding: utf-8

import importlib

from volkanic.introspect import find_all_plain_modules

from joker.flasky.environ import GlobalInterface  # noqa

gi = GlobalInterface()


def test_module_imports():
    for dotpath in find_all_plain_modules(gi.under_project_dir()):
        if dotpath.startswith('joker.flasky.'):
            print(dotpath)
            importlib.import_module(dotpath)


if __name__ == '__main__':
    test_module_imports()
