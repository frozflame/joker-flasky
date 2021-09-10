#!/usr/bin/env python3
# coding: utf-8

from functools import cached_property

import joker.flasky.views.admin_views
import volkanic
from joker.flasky.app import Application
from joker.flasky.loggers import ErrorInterface
from redis import Redis


class _GlocalInterface(volkanic.GlobalInterface):
    package_name = 'example'

    @cached_property
    def redis(self):
        return Redis()

    @cached_property
    def error_interface(self):
        return ErrorInterface(self.redis, self.project_name)


gi = _GlocalInterface()

app = Application(__name__)
app.use_default_error_handlers(gi.error_interface)
app.register_blueprint(joker.flasky.views.admin_views.bp, url_prefix='/admin')

app.run()
