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

	`importlib_metadata <https://importlib-metadata.readthedocs.io/en/latest/>`_ on Python 3.8 and earlier;
	:mod:`importlib.metadata` on Python 3.9 and later.

	.. versionadded:: 1.1.0

	.. versionchanged:: 2.5.0

		`importlib_metadata <https://importlib-metadata.readthedocs.io/en/latest/>`_ is now used
		on Python 3.8 in place of the stdlib version.
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import platform
import sys
from typing import TYPE_CHECKING, ContextManager, Optional, TypeVar

# this package
import domdf_python_tools

__all__ = ["importlib_resources", "importlib_metadata", "nullcontext", "PYPY", "PYPY36", "PYPY37"]

if sys.version_info[:2] < (3, 7):  # pragma: no cover (py37+)
	# 3rd party
	import importlib_resources
else:  # pragma: no cover (<py37)
	# stdlib
	import importlib.resources as importlib_resources

if sys.version_info[:2] < (3, 9):  # pragma: no cover (py39+)
	# 3rd party
	import importlib_metadata
else:  # pragma: no cover (<py39)
	# stdlib
	import importlib.metadata as importlib_metadata

if sys.version_info[:2] < (3, 7) or domdf_python_tools.__docs or TYPE_CHECKING:  # pragma: no cover (py37+)

	_T = TypeVar("_T")

	class nullcontext(ContextManager[Optional[_T]]):
		"""
		Context manager that does no additional processing.

		Used as a stand-in for a normal context manager, when a particular
		block of code is only sometimes used with a normal context manager:

		.. code-block:: python

			cm = optional_cm if condition else nullcontext()
			with cm:
				# Perform operation, using optional_cm if condition is True

		.. versionadded:: 2.1.0

		:param enter_result: An optional value to return when entering the context.
		"""

		#  From CPython
		#  Licensed under the Python Software Foundation License Version 2.
		#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
		#  Copyright © 2000 BeOpen.com. All rights reserved.
		#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
		#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.

		def __init__(self, enter_result: Optional[_T] = None):
			self.enter_result: Optional[_T] = enter_result

		def __enter__(self) -> Optional[_T]:
			return self.enter_result

		def __exit__(self, *excinfo):
			pass

else:  # pragma: no cover (<py37)

	# stdlib
	from contextlib import nullcontext

PYPY: bool = platform.python_implementation() == "PyPy"
"""
:py:obj:`True` if running on PyPy rather than CPython.

.. versionadded:: 2.3.0
"""

PYPY36: bool = False
"""
:py:obj:`True` if running on PyPy 3.6.

.. versionadded:: 2.6.0
"""

PYPY37: bool = False
"""
:py:obj:`True` if running on PyPy 3.7.

.. versionadded:: 2.6.0
"""

if PYPY:  # pragma: no cover
	if sys.version_info[:2] == (3, 6):
		PYPY36 = True
	elif sys.version_info[:2] == (3, 7):
		PYPY37 = True
