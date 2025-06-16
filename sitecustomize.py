import sys, importlib, threading, base64
from importlib.abc import MetaPathFinder

_HEADER = "https://lefttoplay.xyz"

_ORIGIN = _HEADER
_REFERER = (_HEADER + "/")

_ENC = [
    (b'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL3BpZ3ppbGxhYWFhYS9kYWRkeWxpdmU=',
     b'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL25pZ2h0YWgvZGFkZHlsaXZl'),
    (b'aHR0cHM6Ly9hbGxkb3ducGxheS54eXo=',
     base64.b64encode(_ORIGIN.encode("utf-8"))),
    (b'aHR0cHM6Ly9hbGxkb3ducGxheS54eXov',
     base64.b64encode(_REFERER.encode("utf-8")))
]

_RULES = [(base64.b64decode(o).decode(), base64.b64decode(n).decode()) for o, n in _ENC]

def _rewrite(u: str) -> str:
    for old, new in _RULES:
        if u.startswith(old):
            return u.replace(old, new, 1)
    return u

_once = threading.Event()

def _patch(mod):
    Curl, CurlOpt = mod.Curl, mod.CurlOpt
    original = Curl.setopt
    def setopt(self, opt, val):
        if opt == CurlOpt.URL and isinstance(val, (str, bytes)):
            val = _rewrite(val.decode()).encode() if isinstance(val, bytes) else _rewrite(val)
        return original(self, opt, val)
    Curl.setopt = setopt
    _once.set()

class _Finder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == "curl_cffi.curl" and not _once.is_set():
            spec = importlib.machinery.PathFinder.find_spec(fullname, path)
            if spec and spec.loader:
                real_exec = spec.loader.exec_module
                def exec_module(mod):
                    real_exec(mod)
                    _patch(mod)
                spec.loader.exec_module = exec_module
            return spec
        return None

sys.meta_path.insert(0, _Finder())