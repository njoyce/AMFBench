"""
"""

import pyamf

from pyamf import amf0
from pyamf import amf3

from amfbench import builder


class Codec(object):
    """
    @implements: amfbench.codec.ICodec
    """

    name = 'PyAMF'
    package = 'pyamf'
    version = str(pyamf.__version__)

    def setUp(self):
        pyamf.register_class(builder.SomeClass, builder.aliases[builder.SomeClass])

        builder.SomeStaticClass.__amf__ = {
            'dynamic': False,
            'static': ('name', 'score', 'rank')
        }

        pyamf.register_class(builder.SomeStaticClass,
            builder.aliases[builder.SomeStaticClass])

    def tearDown(self):
        pyamf.unregister_class(builder.SomeClass)
        pyamf.unregister_class(builder.SomeStaticClass)

        del builder.SomeStaticClass.__amf__

    def encode(self, payload, amf3):
        encoding = pyamf.AMF3 if amf3 else pyamf.AMF0

        return pyamf.encode(payload, encoding=encoding).getvalue()

    def decode(self, bytes, amf3):
        encoding = pyamf.AMF3 if amf3 else pyamf.AMF0

        ret = [x for x in pyamf.decode(bytes, encoding=encoding)]

        l = len(ret)

        if l == 0:
            return None
        elif l == 1:
            return ret[0]
        else:
            return ret