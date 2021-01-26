#!/usr/bin/env python
# cython: language_level=3
#
#  utils.py
"""
General utility functions.

.. versionchanged:: 1.0.0

	* Removed ``tuple2str`` and ``list2string``.
	  Use :func:`domdf_python_tools.utils.list2str` instead.
	* Removed ``as_text`` and ``word_join``.
	  Import from :mod:`domdf_python_tools.words` instead.
	* Removed ``splitLen``.
	  Use :func:`domdf_python_tools.iterative.split_len` instead.

.. versionchanged:: 2.0.0

	:func:`~domdf_python_tools.iterative.chunks`,
	:func:`~domdf_python_tools.iterative.permutations`,
	:func:`~domdf_python_tools.iterative.split_len`,
	:func:`~domdf_python_tools.iterative.Len`, and
	:func:`~domdf_python_tools.iterative.double_chain`
	moved to :func:`domdf_python_tools.iterative`.

.. versionchanged:: 2.3.0

	Removed :func:`domdf_python_tools.utils.deprecated`.
	Use the new `deprecation-alias <https://pypi.org/project/deprecation-alias/>`_ package instead.

"""
#
#  Copyright © 2018-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#  as_text from https://stackoverflow.com/a/40935194
# 		Copyright © 2016 User3759685
# 		Available under the MIT License
#
#  strtobool based on the "distutils" module from CPython.
#  Some docstrings based on the Python documentation.
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#

# stdlib
import inspect
import json
import sys
from math import log10
from pprint import pformat
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

# this package
import domdf_python_tools.words
from domdf_python_tools.typing import HasHead, String

if TYPE_CHECKING or domdf_python_tools.__docs:  # pragma: no cover
	# 3rd party
	from pandas import DataFrame, Series  # type: ignore

	Series.__module__ = "pandas"
	DataFrame.__module__ = "pandas"

__all__ = [
		"pyversion",
		"SPACE_PLACEHOLDER",
		"cmp",
		"list2str",
		"printr",
		"printt",
		"stderr_writer",
		"printe",
		"str2tuple",
		"strtobool",
		"enquote_value",
		"posargs2kwargs",
		"convert_indents",
		"etc",
		"head",
		"magnitude",
		"trim_precision",
		"double_repr_string",
		]

#: The current major python version.
pyversion: int = int(sys.version_info.major)  # Python Version

#: The ``␣`` character.
SPACE_PLACEHOLDER = '␣'


def cmp(x, y) -> int:
	"""
	Implementation of ``cmp`` for Python 3.

	Compare the two objects x and y and return an integer according to the outcome.

	The return value is negative if ``x < y``, zero if ``x == y`` and strictly positive if ``x > y``.
	"""

	return int((x > y) - (x < y))


def list2str(the_list: Iterable[Any], sep: str = ',') -> str:
	"""
	Convert an iterable, such as a list, to a comma separated string.

	:param the_list: The iterable to convert to a string.
	:param sep: Separator to use for the string.

	:return: Comma separated string
	"""

	return sep.join([str(x) for x in the_list])


def printr(obj: Any, *args, **kwargs) -> None:
	"""
	Print the repr() of an object.
	"""

	print(repr(obj), *args, **kwargs)


def printt(obj: Any, *args, **kwargs) -> None:
	"""
	Print the type of an object.
	"""

	print(type(obj), *args, **kwargs)


def stderr_writer(*args, **kwargs) -> None:
	"""
	Write to stderr, flushing stdout beforehand and stderr afterwards.
	"""

	sys.stdout.flush()
	kwargs["file"] = sys.stderr
	print(*args, **kwargs)
	sys.stderr.flush()


printe = stderr_writer


def str2tuple(input_string: str, sep: str = ',') -> Tuple[int, ...]:
	"""
	Convert a comma-separated string of integers into a tuple.

	.. important::

		The input string must represent a comma-separated series of integers.

	.. TODO:: Allow custom types, not just :class:`int` (making :class:`int` the default)

	:param input_string: The string to be converted into a tuple
	:param sep: The separator in the string.
	"""

	return tuple(int(x) for x in input_string.split(sep))


def strtobool(val: Union[str, int]) -> bool:
	"""
	Convert a string representation of truth to :py:obj:`True` or :py:obj:`False`.

	If val is an integer then its boolean representation is returned. If val is a boolean it is returned as-is.

	:py:obj:`True` values are ``'y'``, ``'yes'``, ``'t'``, ``'true'``, ``'on'``, ``'1'``, and ``1``.

	:py:obj:`False` values are ``'n'``, ``'no'``, ``'f'``, ``'false'``, ``'off'``, ``'0'``, and ``0``.

	:raises: :py:exc:`ValueError` if ``val`` is anything else.
	"""

	if isinstance(val, int):
		return bool(val)

	val = val.lower()
	if val in {'y', "yes", 't', "true", "on", '1'}:
		return True
	elif val in {'n', "no", 'f', "false", "off", '0'}:
		return False
	else:
		raise ValueError(f"invalid truth value {val!r}")


def enquote_value(value: Any) -> Union[str, bool, float]:
	"""
	Adds single quotes (``'``) to the given value, suitable for use in a templating system such as Jinja2.

	:class:`Floats <float>`, :class:`integers <int>`, :class:`booleans <bool>`, :py:obj:`None`,
	and the strings ``'True'``, ``'False'`` and ``'None'`` are returned as-is.

	:param value: The value to enquote
	"""

	if value in {"True", "False", "None", True, False, None}:
		return value
	elif isinstance(value, (int, float)):
		return value
	elif isinstance(value, str):
		return repr(value)
	else:
		return f"'{value}'"


def posargs2kwargs(
		args: Iterable[Any],
		posarg_names: Union[Iterable[str], Callable],
		kwargs: Optional[Dict[str, Any]] = None,
		) -> Dict[str, Any]:
	"""
	Convert the positional args in ``args`` to kwargs, based on the relative order of ``args`` and ``posarg_names``.

	.. important:: Python 3.8's Positional-Only Parameters (:pep:`570`) are not supported.

	.. versionadded:: 0.4.10

	:param args: List of positional arguments provided to a function.
	:param posarg_names: Either a list of positional argument names for the function, or the function object.
	:param kwargs: Optional mapping of keyword argument names to values.
		The arguments will be added to this dictionary if provided.
	:default kwargs: ``{}``

	:return: Dictionary mapping argument names to values.
	"""

	if kwargs is None:
		kwargs = {}

	if callable(posarg_names):
		posarg_names = inspect.getfullargspec(posarg_names).args

	kwargs.update(zip(posarg_names, args))

	# TODO: positional only arguments

	return kwargs


def convert_indents(text: str, tab_width: int = 4, from_: str = '\t', to: str = ' ') -> str:
	r"""
	Convert indentation at the start of lines in ``text`` from tabs to spaces.

	:param text: The text to convert indents in.
	:param tab_width: The number of spaces per tab.
	:param from\_: The indent to convert from.
	:param to: The indent to convert to.
	"""

	output = []
	tab = to * tab_width
	from_size = len(from_)

	for line in text.splitlines():
		indent_count = 0

		while line.startswith(from_):
			indent_count += 1
			line = line[from_size:]

		output.append(f"{tab * indent_count}{line}")

	return '\n'.join(output)


class _Etcetera(str):

	def __new__(cls):
		return str.__new__(cls, "...")  # type: ignore

	def __repr__(self) -> str:
		return str(self)


etc = _Etcetera()
"""
Object that provides an ellipsis string

.. versionadded:: 0.8.0
"""


def head(obj: Union[Tuple, List, "DataFrame", "Series", String, HasHead], n: int = 10) -> Optional[str]:
	"""
	Returns the head of the given object.

	.. versionadded:: 0.8.0

	:param obj:
	:param n: Show the first ``n`` items of ``obj``.

	.. seealso:: :func:`textwrap.shorten`, which truncates a string to fit within a given number of characters.
	"""

	if isinstance(obj, tuple) and hasattr(obj, "_fields"):
		# Likely a namedtuple
		if len(obj) <= n:
			return repr(obj)
		else:
			head_of_namedtuple = {k: v for k, v in zip(obj._fields[:n], obj[:n])}  # type: ignore
			repr_fmt = '(' + ", ".join(f"{k}={v!r}" for k, v in head_of_namedtuple.items()) + f", {etc})"
			return obj.__class__.__name__ + repr_fmt

	elif isinstance(obj, (list, tuple)):
		if len(obj) > n:
			return pformat(obj.__class__((*obj[:n], etc)))
		else:
			return pformat(obj)

	elif isinstance(obj, HasHead):
		return obj.head(n).to_string()

	elif len(obj) <= n:  # type: ignore
		return str(obj)

	else:
		return str(obj[:n]) + etc  # type: ignore


def magnitude(x: float) -> int:
	"""
	Returns the magnitude of the given value.

	* For negative numbers the absolute magnitude is returned.
	* For decimal numbers below ``1`` the magnitude will be negative.

	.. versionadded:: 2.0.0

	:param x: Numerical value to find the magnitude of.
	"""

	if x > 0.0:
		return int(log10(x))
	elif x < 0.0:
		return int(log10(abs(x)))
	else:
		return 0


def trim_precision(value: float, precision: int = 4) -> float:
	"""
	Trim the precision of the given floating point value.

	For example, if you have the value `170.10000000000002` but really only care about it being
	``\u2248 179.1``:

	.. code-block:: python

		>>> trim_precision(170.10000000000002, 2)
		170.1
		>>> type(trim_precision(170.10000000000002, 2))
		<class 'float'>

	.. versionadded:: 2.0.0

	:param value:
	:param precision: The number of decimal places to leave in the output.
	"""

	return float(format(value, f"0.{precision}f"))


def double_repr_string(string: str):
	"""
	Like :func:`repr(str) <repr>`, but tries to use double quotes instead.

	.. versionadded:: 2.5.0
	"""

	# figure out which quote to use; double is preferred
	if '"' in string and "'" not in string:
		return repr(string)
	else:
		return json.dumps(string, ensure_ascii=False)
