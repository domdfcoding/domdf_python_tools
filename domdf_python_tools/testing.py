#!/usr/bin/env python
#
#  testing.py
"""
Handy functions for testing code.

.. extras-require:: testing
	:__pkginfo__:

.. versionadded:: 0.4.9
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
import itertools
import random
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator, List, Optional, Sequence, Tuple, Union

# 3rd party
import _pytest
import pytest
from _pytest.mark import MarkDecorator

# this package
from domdf_python_tools.doctools import PYPY
from domdf_python_tools.iterative import Len
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.versions import Version

__all__ = [
		"generate_truthy_values",
		"generate_falsy_values",
		"testing_boolean_values",
		"whitespace",
		"whitespace_perms_list",
		"whitespace_perms",
		"count",
		"min_version",
		"max_version",
		"not_windows",
		"only_windows",
		"not_pypy",
		"only_pypy",
		"pytest_report_header",
		]

MarkDecorator.__module__ = "_pytest.mark"


def generate_truthy_values(extra_truthy: Sequence = (), ratio: float = 1) -> Iterator[Any]:
	"""
	Returns an iterator of strings, integers and booleans that should be considered :py:obj:`True`.

	Optionally, a random selection of the values can be returned, using the ``ratio`` argument.

	:param extra_truthy: Additional values that should be considered :py:obj:`True`.
	:param ratio: The ratio of the number of values to select to the total number of values.

	:rtype:

	.. versionadded:: 0.4.9
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

	Optionally, a random selection of the values can be returned, using the ``ratio`` argument.

	:param extra_falsy: Additional values that should be considered :py:obj:`True`.
	:param ratio: The ratio of the number of values to select to the total number of values.

	:rtype:

	.. versionadded:: 0.4.9
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


def testing_boolean_values(
		extra_truthy: Sequence = (),
		extra_falsy: Sequence = (),
		ratio: float = 1,
		) -> MarkDecorator:
	"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`_
	decorator that provides a list of strings, integers and booleans, and the boolean representations of them.

	The parametrized arguments are ``boolean_string`` for the input value,
	and ``expected_boolean`` for the expected output.

	Optionally, a random selection of the values can be returned, using the ``ratio`` argument.

	:param extra_truthy: Additional values that should be considered :py:obj:`True`.
	:param extra_falsy: Additional values that should be considered :py:obj:`False`.
	:param ratio: The ratio of the number of values to select to the total number of values.

	:rtype:

	.. versionadded:: 0.4.9
	"""  # noqa D400

	truthy = generate_truthy_values(extra_truthy, ratio)
	falsy = generate_falsy_values(extra_falsy, ratio)

	boolean_strings = [
			*itertools.zip_longest(truthy, [], fillvalue=True),
			*itertools.zip_longest(falsy, [], fillvalue=False),
			]

	return pytest.mark.parametrize("boolean_string, expected_boolean", boolean_strings)


whitespace = " \t\n\r"


@lru_cache(1)
def whitespace_perms_list() -> List[str]:
	chain = itertools.chain.from_iterable(itertools.permutations(whitespace, n) for n in Len(whitespace))
	return list(''.join(x) for x in chain)


def whitespace_perms(ratio: float = 0.5) -> MarkDecorator:
	r"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`_
	decorator that provides permutations of whitespace (strictly only ``␣\n\t\r``).
	Not all permutations are returned, as there are a lot of them;
	instead a random selection of the permutations is returned.
	By default ½ of the permutations are returned, but this can be configured using the ``ratio`` argument.

	The single parametrized argument is ``char``.

	:param ratio: The ratio of the number of permutations to select to the total number of permutations.

	:rtype:

	.. versionadded:: 0.4.9
	"""  # noqa D400

	perms = whitespace_perms_list()
	return pytest.mark.parametrize("char", random.sample(perms, int(len(perms) * ratio)))


def count(stop: int, start: int = 0, step: int = 1) -> MarkDecorator:
	"""
	Returns a `pytest.mark.parametrize <https://docs.pytest.org/en/stable/parametrize.html>`_
	decorator that provides a list of numbers between ``start`` and ``stop`` with an interval of ``step``.

	The single parametrized argument is ``count``.

	:param stop: The stop value passed to :class:`range`.
	:param start: The start value passed to :class:`range`.
	:param step: The step passed to :class:`range`.

	:rtype:

	.. versionadded:: 0.4.9
	"""  # noqa D400

	return pytest.mark.parametrize("count", range(start, stop, step))


def _make_version(version: Union[str, float, Tuple[int, ...]]) -> Version:
	if isinstance(version, float):
		return Version.from_float(version)
	elif isinstance(version, str):
		return Version.from_str(version)
	else:
		return Version.from_tuple(version)


def min_version(
		version: Union[str, float, Tuple[int]],
		reason: Optional[str] = None,
		) -> _pytest.mark.structures.MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator that will
	skip a test if the current Python version is less than the required one.

	:param version: The version number to compare to :py:data:`sys.version_info`.
	:param reason: The reason to display when skipping.
	:default reason: :file:`'Requires Python {<version>} or greater.'`

	:rtype:

	.. versionadded:: 0.9.0
	"""  # noqa D400

	version_ = _make_version(version)

	if reason is None:
		reason = f"Requires Python {version_} or greater."

	return pytest.mark.skipif(condition=sys.version_info[:3] < version_, reason=reason)


def max_version(
		version: Union[str, float, Tuple[int]],
		reason: Optional[str] = None,
		) -> _pytest.mark.structures.MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator that will
	skip a test if the current Python version is greater than the required one.

	:param version: The version number to compare to :py:data:`sys.version_info`.
	:param reason: The reason to display when skipping.
	:default reason: :file:`'Not needed after Python {<version>}.'`

	:rtype:

	.. versionadded:: 0.9.0
	"""  # noqa D400

	version_ = _make_version(version)

	if reason is None:
		reason = f"Not needed after Python {version_}."

	return pytest.mark.skipif(condition=sys.version_info[:3] > version_, reason=reason)


def not_windows(reason: str = "Not required on Windows.", ) -> _pytest.mark.structures.MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator that will
	skip a test if the current platform is Windows.

	:param reason: The reason to display when skipping.

	:rtype:

	.. versionadded:: 0.9.0
	"""  # noqa D400

	return pytest.mark.skipif(condition=sys.platform == "win32", reason=reason)


def only_windows(reason: str = "Only required on Windows.", ) -> _pytest.mark.structures.MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator that will
	skip a test if the current platform is **not** Windows.

	:param reason: The reason to display when skipping.

	:rtype:

	.. versionadded:: 0.9.0
	"""  # noqa D400

	return pytest.mark.skipif(condition=sys.platform != "win32", reason=reason)


def not_pypy(reason: str = "Not required on PyPy.") -> _pytest.mark.structures.MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator that will
	skip a test if the current Python implementation is PyPy.

	:param reason: The reason to display when skipping.

	:rtype:

	.. versionadded:: 0.9.0
	"""  # noqa D400

	return pytest.mark.skipif(condition=PYPY, reason=reason)


def only_pypy(reason: str = "Only required on PyPy.") -> _pytest.mark.structures.MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator that will
	skip a test if the current Python implementation is not PyPy.

	:param reason: The reason to display when skipping.

	:rtype:

	.. versionadded:: 0.9.0
	"""  # noqa D400

	return pytest.mark.skipif(condition=not PYPY, reason=reason)


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

		def my_test(tmp_pathplus: PathPlus):
			assert True

	:rtype:

	.. versionadded:: 0.10.0
	"""  # noqa: D400

	return PathPlus(tmp_path)


def pytest_report_header(config, startdir):
	"""
	Prints the start time of the pytest session.

	.. versionadded:: 1.2.0
	"""

	return f"Test session started at {datetime.datetime.now():%H:%M:%S}"
