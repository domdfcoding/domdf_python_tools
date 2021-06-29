# stdlib
import sys

if sys.version_info[:2] < (3, 9):  # pragma: no cover (py39+)
	# 3rd party
	from importlib_metadata import *
else:  # pragma: no cover (<py39)
	# stdlib
	from importlib.metadata import *
