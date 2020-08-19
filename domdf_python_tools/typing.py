#!/usr/bin/env python
#
#  typing.py
"""
Common aliases for type hinting
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
import os
import pathlib
from decimal import Decimal
from typing import Any, Type, Union

__all__ = ["PathLike", "AnyNumber", "check_membership"]


#: Type hint for objects that represent filesystem paths.
PathLike = Union[str, pathlib.Path, os.PathLike]

AnyNumber = Union[float, int, Decimal]
"""
Type hint for numbers.

.. versionchanged:: 0.4.6

	Moved from :mod:`domdf_python_tools.pagesizes`
"""


def check_membership(obj: Any, type_: Union[Type, object]) -> bool:
	"""
	Check if the type of ``obj`` is one of the types in a :py:data:`typing.Union`, :typing.sequence:``Sequence`` etc.

	:param obj: The object to check the type of
	:param type_: A :class:`~typing.Type` that has members, such as a List, Union or Sequence.

	:return:
	:rtype:
	"""

	return isinstance(obj, type_.__args__)  # type: ignore
