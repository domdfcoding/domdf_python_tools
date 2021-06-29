# stdlib
import sys

if sys.version_info[:2] < (3, 7):  # pragma: no cover (py37+)
	# 3rd party
	from importlib_resources import *
else:  # pragma: no cover (<py39)
	# stdlib
	from importlib.resources import *
