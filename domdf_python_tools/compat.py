#  !/usr/bin/env python
#
#  compat.py
"""
Cross-version compatibility helpers.

.. versionadded :: 0.12.0

Provides the following:

.. py:data:: importlib_resources

	`importlib_resources <https://importlib-resources.readthedocs.io/en/latest/>`_ on Python 3.6;
	:mod:`importlib.resources` on Python 3.7 and later.

.. py:data:: importlib_metadata

	`importlib_metadata <https://importlib-metadata.readthedocs.io/en/latest/>`_ on Python 3.7 and earlier;
	:mod:`importlib.metadata` on Python 3.8 and later.

	.. versionadded:: 1.1.0
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import sys

__all__ = ["importlib_resources", "importlib_metadata"]

if sys.version_info < (3, 7):  # pragma: no cover (>=py37)
	# 3rd party
	import importlib_resources
else:  # pragma: no cover (<py37)
	# stdlib
	import importlib.resources as importlib_resources

if sys.version_info[:2] < (3, 8):  # pragma: no cover (>=py38)
	# 3rd party
	import importlib_metadata  # type: ignore
else:  # pragma: no cover (<py38)
	# stdlib
	import importlib.metadata as importlib_metadata
