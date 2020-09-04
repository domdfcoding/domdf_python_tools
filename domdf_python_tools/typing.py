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
from json import JSONDecoder, JSONEncoder
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

# 3rd party
from typing_extensions import Protocol

__all__ = ["PathLike", "AnyNumber", "check_membership", "JsonLibrary"]

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
	Check if the type of ``obj`` is one of the types in a :py:data:`typing.Union`, :typing.sequence:`Sequence` etc.

	:param obj: The object to check the type of
	:param type_: A :class:`~typing.Type` that has members, such as a List, Union or Sequence.

	:return:
	:rtype:
	"""

	return isinstance(obj, type_.__args__)  # type: ignore


class JsonLibrary(Protocol):
	"""
	Type hint for functions that take a JSON serialisation-deserialisation library as an argument.

	The library implement at least the following methods:
	"""

	@staticmethod
	def dumps(
			obj: Any,
			*,
			skipkeys: bool = ...,
			ensure_ascii: bool = ...,
			check_circular: bool = ...,
			allow_nan: bool = ...,
			cls: Optional[Type[JSONEncoder]] = ...,
			indent: Union[None, int, str] = ...,
			separators: Optional[Tuple[str, str]] = ...,
			default: Optional[Callable[[Any], Any]] = ...,
			sort_keys: bool = ...,
			**kwds: Any,
			) -> str:
		"""
		Serialize ``obj`` to a JSON formatted ``str``.

		:param obj:
		:param skipkeys:
		:param ensure_ascii:
		:param check_circular:
		:param allow_nan:
		:param cls:
		:param indent:
		:param separators:
		:param default:
		:param sort_keys:
		:param kwds:
		"""

	@staticmethod
	def loads(
			s: Union[str, bytes],
			*,
			cls: Optional[Type[JSONDecoder]] = ...,
			object_hook: Optional[Callable[[Dict[Any, Any]], Any]] = ...,
			parse_float: Optional[Callable[[str], Any]] = ...,
			parse_int: Optional[Callable[[str], Any]] = ...,
			parse_constant: Optional[Callable[[str], Any]] = ...,
			object_pairs_hook: Optional[Callable[[List[Tuple[Any, Any]]], Any]] = ...,
			**kwds: Any,
			) -> Any:
		"""
		Deserialize ``s`` to a Python object.

		:param s:
		:param cls:
		:param object_hook:
		:param parse_float:
		:param parse_int:
		:param parse_constant:
		:param object_pairs_hook:
		:param kwds:
		"""
