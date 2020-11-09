#!/usr/bin/env python
#
#  import_tools.py
"""
Functions for importing classes.
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
#  Based on https://github.com/asottile/git-code-debt/blob/master/git_code_debt/util/discovery.py
#  Copyright (c) 2014 Anthony Sottile
#  Licensed under the MIT License
#  |  Permission is hereby granted, free of charge, to any person obtaining a copy
#  |  of this software and associated documentation files (the "Software"), to deal
#  |  in the Software without restriction, including without limitation the rights
#  |  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  |  copies of the Software, and to permit persons to whom the Software is
#  |  furnished to do so, subject to the following conditions:
#  |
#  |  The above copyright notice and this permission notice shall be included in
#  |  all copies or substantial portions of the Software.
#  |
#  |  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  |  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  |  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  |  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  |  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  |  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  |  THE SOFTWARE.
#

# stdlib
import inspect
import pkgutil
from types import ModuleType
from typing import Any, Callable, List, Optional, Type, overload

# 3rd party
from typing_extensions import Literal

# this package
from domdf_python_tools.compat import importlib_metadata

__all__ = ["discover", "discover_entry_points"]


@overload
def discover(
		package: ModuleType,
		match_func: Optional[Callable[[Any], bool]] = ...,
		exclude_side_effects: Literal[True] = ...,
		) -> List[Type[Any]]:
	...  # pragma: no cover


@overload
def discover(
		package: ModuleType,
		match_func: Optional[Callable[[Any], bool]] = ...,
		exclude_side_effects: Literal[False] = ...,
		) -> List[Any]:
	...  # pragma: no cover


def discover(
		package: ModuleType,
		match_func: Optional[Callable[[Any], bool]] = None,
		exclude_side_effects: bool = True,
		) -> List[Any]:
	"""
	Returns a list of objects in the given module,
	optionally filtered by ``match_func``.

	:param package: A Python package
	:param match_func: Function taking an object and returning :py:obj:`True` if the object is to be included in the output.
	:default match_func: :py:obj:`None`, which includes all objects.
	:param exclude_side_effects: Don't include objects that are only there because of an import side effect.

	:return: List of matching objects.

	.. versionchanged:: 1.0.0

		Added the ``exclude_side_effects`` parameter.
	"""  # noqa D400

	matching_objects = []

	for _, module_name, _ in pkgutil.walk_packages(
		# https://github.com/python/mypy/issues/1422
		# Stalled PRs: https://github.com/python/mypy/pull/3527
		#              https://github.com/python/mypy/pull/5212
		package.__path__,  # type: ignore
		prefix=package.__name__ + '.',
		):
		module = __import__(module_name, fromlist=["__trash"], level=0)

		# Check all the functions in that module
		for _, imported_objects in inspect.getmembers(module, match_func):

			if exclude_side_effects:
				if not hasattr(imported_objects, "__module__"):
					continue
				if imported_objects.__module__ != module.__name__:
					continue

			matching_objects.append(imported_objects)

	return matching_objects


#
# def import_module(filename: str):
# 	"""
# 	Import the module with the given filename.
# 	:param filename:
# 	:return:
# 	"""
#
# 	spec = importlib.util.spec_from_file_location("typing", filename)
# 	mod = importlib.util.module_from_spec(spec)
# 	spec.loader.exec_module(mod)
# 	sys.modules[mod.__name__] = mod
# 	return mod


def discover_entry_points(
		group_name: str,
		match_func: Optional[Callable[[Any], bool]] = None,
		) -> List[Any]:
	"""
	Returns a list of entry points in the given category, optionally filtered by ``match_func``.

	:param group_name: The entry point group name, e.g. ``'entry_points'``.
	:param match_func: Function taking an object and returning :py:obj:`True`
		if the object is to be included in the output.
	:default match_func: :py:obj:`None`, which includes all objects.

	:return: List of matching objects.

	.. versionadded:: 1.1.0
	"""

	matching_objects = []

	for entry_point in importlib_metadata.entry_points().get(group_name, ()):
		entry_point = entry_point.load()

		if match_func is not None and not match_func(entry_point):
			continue

		matching_objects.append(entry_point)

	return matching_objects
