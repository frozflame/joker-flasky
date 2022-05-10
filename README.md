joker-flasky
============

Reusable components for flask-based web development.


recent change
-------------

### version 0.5.1
- rewrite of `ViewEntry`
- add `viewutils.find_matching_rule()`

### version 0.5.0

- python_requires >= 3.8
- add `ViewEntry`
- add `respond_upload_page()` and `respond_login_page()`

### version 0.4.8 and 0.4.9

- add URLPathSigner
- add ctxmap_views.py
- do not require joker
- add test_urlpathsigner() and fix URLPathSigner.sign()
- fix respond_content()
- use volkanic~=0.4.0, joker~=0.3.0, joker-redis~=0.0.3
- rename infer_mime_type => infer_mimetype; infer_mimetype('png') acceptable
- add respond_content()
- add DeprecationWarning

### version 0.3

- improve load_contextmap

### version 0.2

- rename j.f.context.load_standard_ctxmap to load_contextmap with improvements

