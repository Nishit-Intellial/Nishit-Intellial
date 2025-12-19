from __future__ import unicode_literals

import json
from io import StringIO


class AppResponse(object):
    @staticmethod
    def msg(code, message):
        msg = {"code": code, "msg": message}
        return json.dumps(msg)

    @staticmethod
    def get(object):
        s = StringIO()
        json.dump(object, s)
        s.seek(0)
        return s.read()

