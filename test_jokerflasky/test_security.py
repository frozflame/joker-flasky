#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

from joker.flasky.security import HashedPassword


def test_hashed_password():
    raw_password = 'PW20170401D'
    hp = HashedPassword.generate(raw_password)
    print(hp)
    assert hp.verify(raw_password)
    assert not hp.verify('pW20170401D')
