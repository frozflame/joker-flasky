#!/usr/bin/env python3
# coding: utf-8

from joker.flasky.auth import HashedPassword, URLPathSigner


def test_hashed_password():
    raw_password = 'PW20170401D'
    hp = HashedPassword.generate(raw_password)
    print(hp)
    assert hp.verify(raw_password)
    assert not hp.verify('pW20170401D')


def test_urlpathsigner():
    secrets = ['f0645e5ee834d6570f0ab3edbac7d7ef']
    signer = URLPathSigner(secrets)
    signed_url = signer.sign('/3/library/urllib.parse.html')
    assert signer.verify(signed_url), signed_url
