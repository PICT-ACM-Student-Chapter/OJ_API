import base64


def b64_encode(s):
    return base64.b64encode(s.encode('utf-8')).decode("utf8")


def b64_decode(s):
    return base64.b64decode(s.encode('utf-8')).decode("utf8")


def b64_sub_str(s, length):
    if len(s) > (4 // 3 * length):
        return b64_encode(b64_decode(s)[:length] + ' ...truncated')
    return s
