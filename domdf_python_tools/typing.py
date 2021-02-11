#!/usr/bin/env python
#
#  typing.py
"""
Common aliases for type hinting.

**Data:**

.. csv-table::
	:widths: 5, 20

	:data:`~.PathLike`, Type hint for objects that represent filesystem paths.
	:data:`~.AnyNumber`, Type hint for numbers.
	:data:`~.WrapperDescriptorType`, The type of methods of some built-in data types and base classes.
	:data:`~.MethodWrapperType`, The type of *bound* methods of some built-in data types and base classes.
	:data:`~.MethodDescriptorType`, The type of methods of some built-in data types.
	:data:`~.ClassMethodDescriptorType`, The type of *unbound* class methods of some built-in data types.

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
import os
import pathlib
import typing
from decimal import Decimal
from json import JSONDecoder, JSONEncoder
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Type, Union

# 3rd party
from typing_extensions import Protocol, runtime_checkable

# this package
import domdf_python_tools

if TYPE_CHECKING or domdf_python_tools.__docs:  # pragma: no cover
	# 3rd party
	from pandas import DataFrame, Series

	Series.__module__ = "pandas"
	DataFrame.__module__ = "pandas"

	JSONDecoder.__module__ = "json"
	JSONEncoder.__module__ = "json"

#: .. versionadded:: 1.0.0
FrameOrSeries = typing.TypeVar("FrameOrSeries", "Series", "DataFrame")

__all__ = [
		"PathLike",
		"PathType",
		"AnyNumber",
		"check_membership",
		"JsonLibrary",
		"WrapperDescriptorType",
		"MethodWrapperType",
		"MethodDescriptorType",
		"ClassMethodDescriptorType",
		"HasHead",
		"String",
		"FrameOrSeries",
		"SupportsIndex",
		]

PathLike = Union[str, pathlib.Path, os.PathLike]
"""
Type hint for objects that represent filesystem paths.

.. seealso:: :py:obj:`domdf_python_tools.typing.PathType`
"""

PathType = typing.TypeVar("PathType", str, pathlib.Path, os.PathLike)
"""
Type variable for objects that represent filesystem paths.

.. versionadded:: 2.2.0

.. seealso:: :py:obj:`domdf_python_tools.typing.PathLike`
"""

AnyNumber = Union[float, int, Decimal]
"""
Type hint for numbers.

.. versionchanged:: 0.4.6

	Moved from :mod:`domdf_python_tools.pagesizes`
"""


def check_membership(obj: Any, type_: Union[Type, object]) -> bool:
	r"""
	Check if the type of ``obj`` is one of the types in a :py:data:`typing.Union`, :class:`typing.Sequence` etc.

	:param obj: The object to check the type of
	:param type\_: A :class:`~typing.Type` that has members,
		such as a :class:`typing.List`, :py:data:`typing.Union` or :py:class:`typing.Sequence`.
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
		Serialize ``obj`` to a JSON formatted :class:`str`.

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


#  Backported from https://github.com/python/cpython/blob/master/Lib/types.py
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.

WrapperDescriptorType = type(object.__init__)
MethodWrapperType = type(object().__str__)
MethodDescriptorType = type(str.join)
ClassMethodDescriptorType = type(dict.__dict__["fromkeys"])


@runtime_checkable
class String(Protocol):
	"""
	:class:`~typing.Protocol` for classes that implement ``__str__``.

	.. versionchanged:: 0.8.0

		Moved from :mod:`domdf_python_tools.stringlist`.
	"""

	def __str__(self) -> str: ...


@runtime_checkable
class HasHead(Protocol):
	"""
	:class:`typing.Protocol` for classes that have a ``head`` method.

	This includes :class:`pandas.DataFrame` and :class:`pandas.Series`.

	.. versionadded:: 0.8.0
	"""  # noqa D400

	def head(self: "HasHead", n: int = 5) -> "HasHead":
		"""
		Return the first n rows.

		:param n: Number of rows to select.

		:return: The first n rows of the caller object.
		"""

	def to_string(self, *args, **kwargs) -> Optional[str]:
		"""
		Render the object to a console-friendly tabular output.
		"""


# class SupportsLessThan(Protocol):
#
# 	def __lt__(self, other: Any) -> bool:
# 		...  # pragma: no cover


class SupportsIndex(Protocol):
	"""
	:class:`typing.Protocol` for classes that support ``__index__``.

	.. versionadded:: 2.0.0
	"""

	def __index__(self) -> int:  # pragma: no cover
		...
