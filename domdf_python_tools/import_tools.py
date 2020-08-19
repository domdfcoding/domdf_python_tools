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
from typing import Any, Callable, List, Optional, Type

__all__ = ["discover"]


def discover(
		package: ModuleType,
		match_func: Optional[Callable[[Any], bool]] = None,
		) -> List[Type[Any]]:
	"""
	Returns a list of objects in the directory matched by match_func

	:param package: A Python package
	:param match_func: Function taking an object and returning true if the object is to be included in the output.
	:default match_func: :py:obj:`None`, which includes all objects.

	:return: List of matching objects.
	"""

	matched_classes = list()

	for _, module_name, _ in pkgutil.walk_packages(
		# https://github.com/python/mypy/issues/1422
		# Stalled PRs: https://github.com/python/mypy/pull/3527
		#              https://github.com/python/mypy/pull/5212
		package.__path__,  # type: ignore
		prefix=package.__name__ + '.',
		):
		module = __import__(module_name, fromlist=['__trash'], level=0)

		# Check all the functions in that module
		for _, imported_objects in inspect.getmembers(module, match_func):
			if not hasattr(imported_objects, "__module__"):
				continue

			# Don't include things that are only there due to a side effect of importing
			if imported_objects.__module__ != module.__name__:
				continue

			matched_classes.append(imported_objects)

	return matched_classes
