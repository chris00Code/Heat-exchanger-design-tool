# -*- coding: utf-8 -*-

__name__ = 'NodeEditor'
__author__ = 'Pavel Křupala'
__version__ = '0.9.13'

from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]