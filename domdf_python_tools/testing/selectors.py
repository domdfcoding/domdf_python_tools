#!/usr/bin/env python
#
#  selectors.py
"""
Pytest decorators for selectively running tests.

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
import sys
from textwrap import dedent
from typing import Callable, Optional, Tuple, Union, cast

# 3rd party
import pytest  # nodep
from _pytest.mark import MarkDecorator  # nodep

# this package
from domdf_python_tools.compat import PYPY
from domdf_python_tools.testing.utils import is_docker
from domdf_python_tools.versions import Version

__all__ = [
		"max_version",
		"min_version",
		"only_version",
		"not_windows",
		"only_windows",
		"not_pypy",
		"only_pypy",
		"not_macos",
		"only_macos",
		"not_docker",
		"only_docker",
		"platform_boolean_factory",
		]


def _make_version(version: Union[str, float, Tuple[int, ...]]) -> Version:
	if isinstance(version, float):
		return Version.from_float(version)
	elif isinstance(version, str):
		return Version.from_str(version)
	else:
		return Version.from_tuple(version)


def min_version(
		version: Union[str, float, Tuple[int, ...]],
		reason: Optional[str] = None,
		) -> MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator that will
	skip a test if the current Python version is less than the required one.

	.. versionadded:: 0.9.0

	:param version: The version number to compare to :py:data:`sys.version_info`.
	:param reason: The reason to display when skipping.
	:default reason: :file:`'Requires Python {<version>} or greater.'`
	"""  # noqa D400

	version_ = _make_version(version)

	if reason is None:
		reason = f"Requires Python {version_} or greater."

	return pytest.mark.skipif(condition=sys.version_info[:3] < version_, reason=reason)


def max_version(
		version: Union[str, float, Tuple[int, ...]],
		reason: Optional[str] = None,
		) -> MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator that will
	skip a test if the current Python version is greater than the required one.

	.. versionadded:: 0.9.0

	:param version: The version number to compare to :py:data:`sys.version_info`.
	:param reason: The reason to display when skipping.
	:default reason: :file:`'Not needed after Python {<version>}.'`
	"""  # noqa D400

	version_ = _make_version(version)

	if reason is None:
		reason = f"Not needed after Python {version_}."

	return pytest.mark.skipif(condition=sys.version_info[:3] > version_, reason=reason)


def only_version(
		version: Union[str, float, Tuple[int, ...]],
		reason: Optional[str] = None,
		) -> MarkDecorator:
	"""
	Factory function to return a ``@pytest.mark.skipif`` decorator that will
	skip a test if the current Python version not the required one.

	.. versionadded:: 2.0.0

	:param version: The version number to compare to :py:data:`sys.version_info`.
	:param reason: The reason to display when skipping.
	:default reason: :file:`'Not needed on Python {<version>}.'`
	"""  # noqa D400

	version_ = _make_version(version)

	if reason is None:
		reason = f"Not needed on Python {version_}."

	return pytest.mark.skipif(condition=sys.version_info[:2] != version_[:2], reason=reason)


def platform_boolean_factory(
		condition: bool,
		platform: str,
		versionadded: Optional[str] = None,
		*,
		module: Optional[str] = None,
		) -> Tuple[Callable[..., MarkDecorator], Callable[..., MarkDecorator]]:
	"""
	Factory function to return decorators such as :func:`~.not_pypy` and :func:`~.only_windows`.

	:param condition: Should evaluate to :py:obj:`True` if the test should be skipped.
	:param platform:
	:param versionadded:
	:param module: The module to set the function as belonging to in ``__module__``.
		If :py:obj:`None` ``__module__`` is set to ``'domdf_python_tools.testing'``.

	:return: 2-element tuple of ``not_function``, ``only_function``.

	.. versionadded: 1.5.0

	.. versionchanged: 1.7.1  Added the ``module`` keyword-only argument.
	"""

	default_reason = f"{{}} required on {platform}"
	module = module or platform_boolean_factory.__module__

	def not_function(reason: str = default_reason.format("Not")) -> MarkDecorator:
		return pytest.mark.skipif(condition=condition, reason=reason)

	def only_function(reason: str = default_reason.format("Only")) -> MarkDecorator:
		return pytest.mark.skipif(condition=not condition, reason=reason)

	docstring = dedent(
			"""\
Factory function to return a ``@pytest.mark.skipif`` decorator that will
skip a test {why} the current platform is {platform}.

:param reason: The reason to display when skipping.
"""
			)

	if versionadded:
		docstring += f"\n\n:rtype:\n\n.. versionadded:: {versionadded}"

	not_function.__name__ = not_function.__qualname__ = f"not_{platform.lower()}"
	not_function.__module__ = module
	not_function.__doc__ = docstring.format(why="if", platform=platform)

	only_function.__name__ = only_function.__qualname__ = f"only_{platform.lower()}"
	only_function.__module__ = module
	only_function.__doc__ = docstring.format(why="unless", platform=platform)

	return not_function, only_function


not_windows, only_windows = platform_boolean_factory(
		condition=sys.platform == "win32",
		platform="Windows",
		versionadded="0.9.0",
		)

not_macos, only_macos = platform_boolean_factory(
		condition=sys.platform == "darwin",
		platform="macOS",
		versionadded="1.5.0",
		)

not_docker, only_docker = platform_boolean_factory(condition=is_docker(), platform="Docker", versionadded="1.5.0")
not_docker.__doc__ = cast(str, not_docker.__doc__).replace("the current platform is", "running on")
only_docker.__doc__ = cast(str, only_docker.__doc__).replace("the current platform is", "running on")

not_pypy, only_pypy = platform_boolean_factory(condition=PYPY, platform="PyPy", versionadded="0.9.0")
not_pypy.__doc__ = cast(str, not_pypy.__doc__).replace("current platform", "current Python implementation")
only_pypy.__doc__ = cast(str, only_pypy.__doc__).replace("current platform", "current Python implementation")
