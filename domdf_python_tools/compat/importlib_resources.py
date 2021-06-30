# noqa: D100

# stdlib
import sys

if sys.version_info[:2] < (3, 7):  # pragma: no cover (py37+)
	# 3rd party
	import importlib_resources
	globals().update(importlib_resources.__dict__)
else:  # pragma: no cover (<py39)
	# stdlib
	import importlib.resources
	globals().update(importlib.resources.__dict__)
