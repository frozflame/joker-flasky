#!/usr/bin/env python3
# coding: utf-8

from joker.flasky import viewutils


def test_infer_mime_type():
    assert viewutils.infer_mime_type('.png', '-') == 'image/png'
    assert viewutils.infer_mime_type('a.png', '-') == 'image/png'
    assert viewutils.infer_mime_type('a/a.png', '-') == 'image/png'


if __name__ == '__main__':
    test_infer_mime_type()