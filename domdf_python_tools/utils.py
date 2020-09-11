#!/usr/bin/env python
# cython: language_level=3
#
#  utils.py
"""
General utility functions

.. versionchanged:: 0.8.0

	``tuple2str`` and ``list2string`` are deprecated and will be removed in 1.0.0.
	Use :func:`domdf_python_tools.utils.list2str` instead.
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  check_dependencies based on https://stackoverflow.com/a/29044693/3092681
#  		Copyright © 2015 TehTechGuy
# 		Licensed under CC-BY-SA
#
#  as_text from https://stackoverflow.com/a/40935194
# 		Copyright © 2016 User3759685
# 		Available under the MIT License
#
#  chunks from https://stackoverflow.com/a/312464/3092681
# 		Copytight © 2008 Ned Batchelder
# 		Licensed under CC-BY-SA
#
#  strtobool based on the "distutils" module from CPython
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#

# stdlib
import inspect
import itertools
import sys
from pprint import pformat
from typing import TYPE_CHECKING, Any, Callable, Dict, Generator, Iterable, List, Optional, Sequence, Tuple, Union

# 3rd party
import deprecation  # type: ignore
from typing_extensions import Protocol, runtime_checkable

# this package
import domdf_python_tools.words
from domdf_python_tools import __version__

if TYPE_CHECKING:
	# 3rd party
	from pandas import DataFrame, Series  # type: ignore
	from pandas._typing import FrameOrSeries  # type: ignore

__all__ = [
		"pyversion",
		"SPACE_PLACEHOLDER",
		"check_dependencies",
		"chunks",
		"cmp",
		"list2str",
		"permutations",
		"printr",
		"printt",
		"stderr_writer",
		"printe",
		"split_len",
		"splitLen",
		"str2tuple",
		"strtobool",
		"enquote_value",
		"Len",
		"double_chain",
		"posargs2kwargs",
		"convert_indents",
		"etc",
		"head",
		"HasHead",
		"String",
		]

#: The current major python version.
pyversion: int = int(sys.version_info.major)  # Python Version

#: The ``␣`` character.
SPACE_PLACEHOLDER = '␣'


@runtime_checkable
class String(Protocol):
	"""
	Protocol for classes that implement ``__str__``.
	"""

	def __str__(self) -> str:
		...  # pragma: no cover


def check_dependencies(dependencies: Iterable[str], prt: bool = True) -> List[str]:
	"""
	Check whether one or more dependencies are available to be imported.

	:param dependencies: The list of dependencies to check the availability of.
	:param prt: Whether the status should be printed to the terminal. Default :py:obj:`True`.

	:return: A list of any missing modules
	"""

	# stdlib
	from pkgutil import iter_modules

	modules = {x[1] for x in iter_modules()}
	missing_modules = []

	for requirement in dependencies:
		if requirement not in modules:
			missing_modules.append(requirement)

	if prt:
		if len(missing_modules) == 0:
			print("All modules installed")
		else:
			print("The following modules are missing.")
			print(missing_modules)
			print("Please check the documentation.")
		print('')

	return missing_modules


def chunks(l: Sequence[Any], n: int) -> Generator[Any, None, None]:
	"""
	Yield successive n-sized chunks from l.

	:param l: The objects to yield chunks from
	:param n: The size of the chunks
	"""

	for i in range(0, len(l), n):
		yield l[i:i + n]


def cmp(x, y) -> int:
	"""
	Implementation of cmp for Python 3.

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


# Will be removed in 1.0.0
tuple2str = list2string = list2str


def permutations(data: Iterable[Any], n: int = 2) -> List[Tuple[Any, ...]]:
	"""
	Return permutations containing ``n`` items from ``data`` without any reverse duplicates.

	If ``n`` is equal to or greater than the length of the data an empty list of returned.

	:param data:
	:param n:
	"""

	if n == 0:
		raise ValueError("'n' cannot be 0")

	perms = []
	for i in itertools.permutations(data, n):
		if i[::-1] not in perms:
			perms.append(i)

	return perms


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


def split_len(string: str, n: int) -> List[str]:
	"""
	Split a string every ``n`` characters.

	:param string: The string to split
	:param n: The number of characters to split after

	:return: The split string
	"""

	return [string[i:i + n] for i in range(0, len(string), n)]


splitLen = split_len


def str2tuple(input_string: str, sep: str = ',') -> Tuple[int, ...]:
	"""
	Convert a comma-separated string of integers into a tuple.

	.. important::

		The input string must represent a comma-separated series of integers.

	.. TODO:: Allow custom types, not just ``int`` (making ``int`` the default)

	:param input_string: The string to be converted into a tuple
	:param sep: The separator in the string. Default `,`
	"""

	return tuple(int(x) for x in input_string.split(sep))


def strtobool(val: Union[str, bool]) -> bool:
	"""
	Convert a string representation of truth to :py:obj:`True` or :py:obj:`False`.

	If val is an integer then its boolean representation is returned. If val is a boolean it is returned as-is.

	:py:obj:`True` values are ``'y'``, ``'yes'``, ``'t'``, ``'true'``, ``'on'``, ``'1'``, and ``1``.

	:py:obj:`False` values are ``'n'``, ``'no'``, ``'f'``, ``'false'``, ``'off'``, ``'0'``, and ``0``.

	:raises: :py:exc:`ValueError` if 'val' is anything else.
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


def Len(obj: Any, start: int = 0, step: int = 1) -> range:
	"""
	Shorthand for ``range(len(obj))``.

	Returns an object that produces a sequence of integers from start (inclusive)
	to len(obj) (exclusive) by step.

	:param obj: The object to iterate over the length of.
	:param start: The start value of the range.
	:param step: The step of the range.

	.. versionadded:: 0.4.7
	"""

	return range(start, len(obj), step)


def double_chain(iterable: Iterable[Iterable]):
	"""
	Flatten a list of lists of lists into a single list.

	Literally just:

	.. code-block:: python

		chain.from_iterable(chain.from_iterable(iterable))

	Converts

	.. code-block:: python

		[[(1, 2), (3, 4)], [(5, 6), (7, 8)]]

	to

	.. code-block:: python

		[1, 2, 3, 4, 5, 6, 7, 8]


	:param iterable: The iterable to chain.
	:return:

	.. versionadded:: 0.4.7
	"""

	yield from itertools.chain.from_iterable(itertools.chain.from_iterable(iterable))


def posargs2kwargs(
		args: Iterable[Any],
		posarg_names: Union[Iterable[str], Callable],
		kwargs: Optional[Dict[str, Any]] = None,
		) -> Dict[str, Any]:
	"""
	Convert the positional args in ``args`` to kwargs, based on the relative order of ``args`` and ``posarg_names``.

	:param args: List of positional arguments provided to a function.
	:param posarg_names: Either a list of positional argument names for the function, or the function object.
	:param kwargs: Optional mapping of keyword argument names to values.
		The arguments will be added to this dictionary if provided.
	:default kwargs: ``{}``

	:return: Dictionary mapping argument names to values.

	.. versionadded:: 0.4.10
	"""

	if kwargs is None:
		kwargs = {}

	if callable(posarg_names):
		posarg_names = inspect.getfullargspec(posarg_names).args

	kwargs.update(zip(posarg_names, args))

	return kwargs


def convert_indents(text: str, tab_width: int = 4, from_: str = "\t", to: str = " ") -> str:
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

	return "\n".join(output)


as_text = deprecation.deprecated(
		deprecated_in="0.8.0",
		removed_in="1.0.0",
		current_version=__version__,
		details="Import from 'domdf_python_tools.words' instead.",
		)(
				domdf_python_tools.words.as_text
				)

word_join = deprecation.deprecated(
		deprecated_in="0.8.0",
		removed_in="1.0.0",
		current_version=__version__,
		details="Import from 'domdf_python_tools.words' instead.",
		)(
				domdf_python_tools.words.word_join
				)


@runtime_checkable
class HasHead(Protocol):
	"""
	:class:`typing.Protocol` for classes that have a ``head``.

	This includes :class:`pandas.DataFrame` and :class:`pandas.Series`.
	"""

	def head(self: "FrameOrSeries", n: int = 5) -> "FrameOrSeries":
		...  # pragma: no cover

	def to_string(self, *args, **kwargs) -> Optional[str]:
		...  # pragma: no cover


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


def head(obj: Union[Tuple, List, "DataFrame", "Series", "String"], n: int = 10) -> str:
	"""
	Returns the head of the given object.

	:param obj:
	:param n: Show the first ``n`` items of ``obj``.

	.. versionadded:: 0.8.0
	"""

	if isinstance(obj, tuple) and hasattr(obj, "_fields"):
		if len(obj) <= n:
			return repr(obj)
		else:
			# Likely a namedtuple
			head_of_namedtuple = {k: v for k, v in zip(obj._fields[:n], obj[:n])}  # type: ignore
			repr_fmt = '(' + ', '.join(f'{k}={v!r}' for k, v in head_of_namedtuple.items()) + f', {etc})'
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
