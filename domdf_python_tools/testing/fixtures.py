#!/usr/bin/env python
#
#  fixtures.py
"""
Pytest fixtures.

.. extras-require:: testing
	:__pkginfo__:

.. versionadded:: 2.2.0
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
import datetime
import os
from pathlib import Path

# 3rd party
import pytest  # nodep

# this package
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.testing.utils import with_fixed_datetime

__all__ = ["fixed_datetime", "original_datadir", "tmp_pathplus"]


@pytest.fixture()
def tmp_pathplus(tmp_path: Path) -> PathPlus:
	"""
	Pytest fixture that returns a temporary directory in the form of a
	:class:`~domdf_python_tools.paths.PathPlus` object.

	The directory is unique to each test function invocation,
	created as a sub directory of the base temporary directory.

	Use it as follows:

	.. code-block:: python

		pytest_plugins = ("domdf_python_tools.testing", )

		def test_something(tmp_pathplus: PathPlus):
			assert True

	.. versionadded:: 0.10.0
	"""  # noqa: D400

	return PathPlus(tmp_path)


@pytest.fixture()
def original_datadir(request) -> Path:  # noqa: D103
	# Work around pycharm confusing datadir with test file.
	return PathPlus(os.path.splitext(request.module.__file__)[0] + '_')


@pytest.fixture()
def fixed_datetime(monkeypatch):
	"""
	Pytest fixture to pretend the current datetime is 2:20 AM on 13th October 2020.

	.. versionadded:: 2.2.0

	.. seealso:: The :func:`with_fixed_datetime` contextmanager.

	.. attention::

		The monkeypatching only works when datetime is used and imported like:

		.. code-block:: python

			import datetime
			print(datetime.datetime.now())

		Using ``from datetime import datetime`` won't work.
	"""

	with with_fixed_datetime(datetime.datetime(2020, 10, 13, 2, 20)):
		yield
