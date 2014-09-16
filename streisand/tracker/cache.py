# -*- coding: utf-8 -*-


def make_auth_key(key, prefix, version):
    return '{version}:{prefix}:{key}'.format(
        prefix=prefix,
        key=key,
        version=version,
    )
