import logging

from . import api, schema

logging.getLogger().setLevel(logging.DEBUG)
# logging.getLogger("kairoyst").addHandler(logging.NullHandler())

__all__ = ["api", "schema"]
