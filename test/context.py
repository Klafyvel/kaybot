import os
import sys

from kaibot import api

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


__all__ = [api]
