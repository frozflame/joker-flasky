joker-flasky
============

Reusable components for flask-based web development.


recent change
-------------

#### 0.5.0

- python_requires >= 3.8
- add ViewEntry
- add respond_upload_page(), respond_login_page()

#### 0.4.8 and 0.4.9

- add URLPathSigner
- add ctxmap_views.py
- do not require joker
- add test_urlpathsigner() and fix URLPathSigner.sign()
- fix respond_content()
- use volkanic~=0.4.0, joker~=0.3.0, joker-redis~=0.0.3
- rename infer_mime_type => infer_mimetype; infer_mimetype('png') acceptable
- add respond_content()
- add DeprecationWarning

#### 0.3

- improve load_contextmap

#### 0.2

- rename j.f.context.load_standard_ctxmap to load_contextmap with improvements

#### 0.1

- remove j.f.context.{ContextFile,RealContextFile,ContextDirectory,RealContextDirectory,context_load}
- add j.f.context.load_standard_ctxmap

#### 0.0.8

- bug fix: contextmap[path] -> contextmap[name]
- remove indented_json_print_legacy

#### 0.0.7

- _create_flaskapp(): update with _global before requests, _sver removed
