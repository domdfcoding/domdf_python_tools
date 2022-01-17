# noqa: D100

# stdlib
import sys
from typing import TextIO

if sys.version_info[:2] < (3, 7):  # pragma: no cover (py37+)
	# 3rd party
	import importlib_resources
	from importlib_resources._common import normalize_path

	globals().update(importlib_resources.__dict__)

	def read_binary(package: importlib_resources.Package, resource: importlib_resources.Resource) -> bytes:
		"""
		Return the binary contents of the resource.
		"""

		return (importlib_resources.files(package) / normalize_path(resource)).read_bytes()

	def open_text(
			package: importlib_resources.Package,
			resource: importlib_resources.Resource,
			encoding: str = 'utf-8',
			errors: str = 'strict',
			) -> TextIO:
		"""
		Return a file-like object opened for text reading of the resource.
		"""

		return (importlib_resources.files(package) / normalize_path(resource)).open(
				'r',
				encoding=encoding,
				errors=errors,
				)

	def read_text(
			package: importlib_resources.Package,
			resource: importlib_resources.Resource,
			encoding: str = 'utf-8',
			errors: str = 'strict',
			) -> str:
		"""
		Return the decoded string of the resource.
		"""

		with importlib_resources.open_text(package, resource, encoding, errors) as fp:
			return fp.read()

else:  # pragma: no cover (<py39)
	# stdlib
	import importlib.resources
	globals().update(importlib.resources.__dict__)
