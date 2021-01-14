#!/usr/bin/env python
#
#  utils.py
"""
Test helper utilities.

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
#  is_docker based on https://github.com/jaraco/jaraco.docker
#  Copyright Jason R. Coombs
#  |  Permission is hereby granted, free of charge, to any person obtaining a copy
#  |  of this software and associated documentation files (the "Software"), to deal
#  |  in the Software without restriction, including without limitation the rights
#  |  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  |  copies of the Software, and to permit persons to whom the Software is
#  |  furnished to do so, subject to the following conditions:
#  |
#  |  The above copyright notice and this permission notice shall be included in all
#  |  copies or substantial portions of the Software.
#  |
#  |  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  |  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  |  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  |  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  |  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  |  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  |  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import datetime
import os
import random
from contextlib import contextmanager
from functools import lru_cache
from itertools import chain, permutations
from typing import Any, Iterator, List, Sequence

# 3rd party
import pytest  # nodep

# this package
from domdf_python_tools.iterative import Len
from domdf_python_tools.paths import PathPlus

__all__ = [
		"is_docker",
		"with_fixed_datetime",
		"generate_truthy_values",
		"generate_falsy_values",
		"whitespace",
		"whitespace_perms_list",
		]


def is_docker():
	"""
	Is this current environment running in docker?

	>>> type(is_docker())
	<class 'bool'>

	.. versionadded:: 0.6.0
	"""  # noqa: D400

	if os.path.exists("/.dockerenv"):
		return True

	cgroup = PathPlus("/proc/self/cgroup")

	if cgroup.is_file():
		try:
			return any("docker" in line for line in cgroup.read_lines())
		except FileNotFoundError:
			return False

	return False


@contextmanager
def with_fixed_datetime(fixed_datetime: datetime.datetime):
	"""
	Context manager to set a fixed datetime for the duration of the ``with`` block.

	.. versionadded:: 2.2.0

	:param fixed_datetime:

	.. seealso:: The :fixture:`fixed_datetime` fixture.

	.. attention::

		The monkeypatching only works when datetime is used and imported like:

		.. code-block:: python

			import datetime
			print(datetime.datetime.now())

		Using ``from datetime import datetime`` won't work.
	"""

	class D(datetime.date):

		@classmethod
		def today(cls):
			return datetime.date(
					fixed_datetime.year,
					fixed_datetime.month,
					fixed_datetime.day,
					)

	class DT(datetime.datetime):

		@classmethod
		def today(cls):
			return datetime.datetime(
					fixed_datetime.year,
					fixed_datetime.month,
					fixed_datetime.day,
					)

		@classmethod
		def now(cls, tz=None):
			return datetime.datetime.fromtimestamp(fixed_datetime.timestamp())

	D.__name__ = "date"
	D.__qualname__ = "date"
	DT.__qualname__ = "datetime"
	DT.__name__ = "datetime"
	D.__module__ = "datetime"
	DT.__module__ = "datetime"

	with pytest.MonkeyPatch.context() as monkeypatch:
		monkeypatch.setattr(datetime, "date", D)
		monkeypatch.setattr(datetime, "datetime", DT)

		yield


def generate_truthy_values(
		extra_truthy: Sequence = (),
		ratio: float = 1,
		) -> Iterator[Any]:
	"""
	Returns an iterator of strings, integers and booleans that should be considered :py:obj:`True`.

	Optionally, a random selection of the values can be returned using the ``ratio`` argument.

	.. versionadded:: 0.4.9

	:param extra_truthy: Additional values that should be considered :py:obj:`True`.
	:param ratio: The ratio of the number of values to select to the total number of values.
	"""

	truthy_values = [
			True,
			"True",
			"true",
			"tRUe",
			'y',
			'Y',
			"YES",
			"yes",
			"Yes",
			"yEs",
			"ON",
			"on",
			'1',
			1,
			*extra_truthy,
			]

	if ratio < 1:
		truthy_values = random.sample(truthy_values, int(len(truthy_values) * ratio))

	yield from truthy_values


def generate_falsy_values(extra_falsy: Sequence = (), ratio: float = 1) -> Iterator[Any]:
	"""
	Returns an iterator of strings, integers and booleans that should be considered :py:obj:`False`.

	Optionally, a random selection of the values can be returned using the ``ratio`` argument.

	.. versionadded:: 0.4.9

	:param extra_falsy: Additional values that should be considered :py:obj:`True`.
	:param ratio: The ratio of the number of values to select to the total number of values.
	"""

	falsy_values = [
			False,
			"False",
			"false",
			"falSE",
			'n',
			'N',
			"NO",
			"no",
			"nO",
			"OFF",
			"off",
			"oFF",
			'0',
			0,
			*extra_falsy,
			]

	if ratio < 1:
		falsy_values = random.sample(falsy_values, int(len(falsy_values) * ratio))

	yield from falsy_values


whitespace = " \t\n\r"


@lru_cache(1)
def whitespace_perms_list() -> List[str]:  # noqa: D103
	perms = chain.from_iterable(permutations(whitespace, n) for n in Len(whitespace))
	return list(''.join(x) for x in perms)
