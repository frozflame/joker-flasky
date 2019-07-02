Changes of joker-flasky
========================

#### 0.1
* remove j.f.context.{ContextFile,RealContextFile,ContextDirectory,RealContextDirectory,context_load}
* add j.f.context.load_standard_ctxmap

#### 0.0.8
* bug fix: contextmap[path] -> contextmap[name]
* remove indented_json_print_legacy

#### 0.0.7
* _create_flaskapp(): update with _global before requests, _sver removed

#### 0.0.6
* path without .html
* no redirect for "/"

#### 0.0.5
* function _make_salt
* bug fix: _global dict altered

#### 0.0.4
* replace JSONEncoderExt with JSONEncoderPlus (flask-based)

#### 0.0.3
* remove module level import flask in j.f.serialize
* add Decimal support in j.f.ser.JSONEncoderExt

#### 0.0.2
* remove j.f.ser.jsonencoder_default
* remove j.f.dev.JSONEncoderFlasky
* new j.f.ser.JSONEncoderExt extending flask.json.Encoder

