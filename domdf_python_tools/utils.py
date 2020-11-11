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
	  Use :func:`domdf_python_tools.utils.split_len` instead.

.. versionchanged:: 1.4.0

	:func:`~domdf_python_tools.iterative.chunks`,
	:func:`~domdf_python_tools.iterative.permutations`,
	:func:`~domdf_python_tools.iterative.split_len`,
	:func:`~domdf_python_tools.iterative.Len`, and
	:func:`~domdf_python_tools.iterative.double_chain`
	moved to :func:`domdf_python_tools.iterative`.

	They can still be imported from here until version 2.0.0, but that use is deprecated.
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
#  strtobool based on the "distutils" module from CPython.
#  Some docstrings based on the Python documentation.
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#
#  deprecated based on https://github.com/briancurtin/deprecation
#  Modified to only change the docstring of the wrapper and not the original function.
#  |  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  |  not use this file except in compliance with the License. You may obtain
#  |  a copy of the License at
#  |
#  |      http://www.apache.org/licenses/LICENSE-2.0
#  |
#  |  Unless required by applicable law or agreed to in writing, software
#  |  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  |  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  |  License for the specific language governing permissions and limitations
#  |  under the License.
#

# stdlib
import difflib
import functools
import inspect
import sys
import textwrap
import typing
import warnings
from datetime import date
from pprint import pformat
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

# 3rd party
import deprecation  # type: ignore
from packaging import version

# this package
import domdf_python_tools.words
from domdf_python_tools import __version__, iterative
from domdf_python_tools.terminal_colours import Colour, Fore
from domdf_python_tools.typing import HasHead, String

if typing.TYPE_CHECKING or domdf_python_tools.__docs:  # pragma: no cover
	# 3rd party
	from pandas import DataFrame, Series  # type: ignore

	Series.__module__ = "pandas"
	DataFrame.__module__ = "pandas"

__all__ = [
		"pyversion",
		"SPACE_PLACEHOLDER",
		"check_dependencies",
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
		"coloured_diff",
		"deprecated",
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

	:param obj:
	:param n: Show the first ``n`` items of ``obj``.

	.. versionadded:: 0.8.0

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


def deprecated(
		deprecated_in: Optional[str] = None,
		removed_in: Optional[str] = None,
		current_version: Optional[str] = None,
		details: str = '',
		name: Optional[str] = None
		):
	r"""Decorate a function to signify its deprecation.

	This function wraps a method that will soon be removed and does two things:

	* The docstring of the method will be modified to include a notice
	  about deprecation, e.g., "Deprecated since 0.9.11. Use foo instead."
	* Raises a :class:`~deprecation.DeprecatedWarning`
	  via the :mod:`warnings` module, which is a subclass of the built-in
	  :class:`DeprecationWarning`. Note that built-in
	  :class:`DeprecationWarning`\s are ignored by default, so for users
	  to be informed of said warnings they will need to enable them -- see
	  the :mod:`warnings` module documentation for more details.

	:param deprecated_in: The version at which the decorated method is considered
		deprecated. This will usually be the next version to be released when
		the decorator is added. The default is :py:obj:`None`, which effectively
		means immediate deprecation. If this is not specified, then the
		``removed_in`` and ``current_version`` arguments are ignored.
	:no-default deprecated_in:

	:param removed_in: The version or :class:`datetime.date` when the decorated
		method will be removed. The default is :py:obj:`None`, specifying that
		the function is not currently planned to be removed.

		.. note::

			This parameter cannot be set to a value if ``deprecated_in=None``.

	:no-default removed_in:

	:param current_version: The source of version information for the currently
		running code. This will usually be a ``__version__`` attribute in your
		library. The default is :py:obj:`None`. When ``current_version=None``
		the automation to determine if the wrapped function is actually in
		a period of deprecation or time for removal does not work, causing a
		:class:`~deprecation.DeprecatedWarning` to be raised in all cases.
	:no-default current_version:

	:param details: Extra details to be added to the method docstring and
		warning. For example, the details may point users to a replacement
		method, such as "Use the foo_bar method instead".

	:param name: The name of the deprecated function, if an alias is being
		deprecated. Default is to the name of the decorated function.
	:no-default name:
	"""

	# You can't just jump to removal. It's weird, unfair, and also makes
	# building up the docstring weird.
	if deprecated_in is None and removed_in is not None:
		raise TypeError("Cannot set removed_in to a value without also setting deprecated_in")

	# Only warn when it's appropriate. There may be cases when it makes sense
	# to add this decorator before a formal deprecation period begins.
	# In CPython, PendingDeprecatedWarning gets used in that period,
	# so perhaps mimick that at some point.
	is_deprecated = False
	is_unsupported = False

	# StrictVersion won't take a None or a "", so make whatever goes to it
	# is at least *something*. Compare versions only if removed_in is not
	# of type datetime.date
	if isinstance(removed_in, date):
		if date.today() >= removed_in:
			is_unsupported = True
		else:
			is_deprecated = True
	elif current_version:
		current_version = version.parse(current_version)  # type: ignore

		if removed_in is not None and current_version >= version.parse(removed_in):  # type: ignore
			is_unsupported = True
		elif deprecated_in is not None and current_version >= version.parse(deprecated_in):  # type: ignore
			is_deprecated = True
	else:
		# If we can't actually calculate that we're in a period of
		# deprecation...well, they used the decorator, so it's deprecated.
		# This will cover the case of someone just using
		# @deprecated("1.0") without the other advantages.
		is_deprecated = True

	should_warn = any([is_deprecated, is_unsupported])

	def _function_wrapper(function):
		# Everything *should* have a docstring, but just in case...
		existing_docstring = function.__doc__ or ''

		# split docstring at first occurrence of newline
		string_list = existing_docstring.split('\n', 1)

		if should_warn:
			# The various parts of this decorator being optional makes for
			# a number of ways the deprecation notice could go. The following
			# makes for a nicely constructed sentence with or without any
			# of the parts.

			parts = {"deprecated_in": '', "removed_in": '', "details": ''}

			if deprecated_in:
				parts["deprecated_in"] = f" {deprecated_in}"
			if removed_in:
				# If removed_in is a date, use "removed on"
				# If removed_in is a version, use "removed in"
				if isinstance(removed_in, date):
					parts["removed_in"] = f"\n   This will be removed on {removed_in}."
				else:
					parts["removed_in"] = f"\n   This will be removed in {removed_in}."
			if details:
				parts["details"] = f" {details}"

			deprecation_note = (".. deprecated::{deprecated_in}{removed_in}{details}".format_map(parts))

			# default location for insertion of deprecation note
			loc = 1

			if len(string_list) > 1:
				# With a multi-line docstring, when we modify
				# existing_docstring to add our deprecation_note,
				# if we're not careful we'll interfere with the
				# indentation levels of the contents below the
				# first line, or as PEP 257 calls it, the summary
				# line. Since the summary line can start on the
				# same line as the """, dedenting the whole thing
				# won't help. Split the summary and contents up,
				# dedent the contents independently, then join
				# summary, dedent'ed contents, and our
				# deprecation_note.

				# in-place dedent docstring content
				string_list[1] = textwrap.dedent(string_list[1])

				# we need another newline
				string_list.insert(loc, '\n')

				# change the message_location if we add to end of docstring
				# do this always if not "top"
				if deprecation.message_location != "top":
					loc = 3

			# insert deprecation note and dual newline
			string_list.insert(loc, deprecation_note)
			string_list.insert(loc, "\n\n")

		@functools.wraps(function)
		def _inner(*args, **kwargs):
			if should_warn:
				if is_unsupported:
					cls = deprecation.UnsupportedWarning
				else:
					cls = deprecation.DeprecatedWarning

				the_warning = cls(name or function.__name__, deprecated_in, removed_in, details)
				warnings.warn(the_warning, category=DeprecationWarning, stacklevel=2)

			return function(*args, **kwargs)

		_inner.__doc__ = ''.join(string_list)

		return _inner

	return _function_wrapper


chunks = deprecated(
		deprecated_in="1.4.0",
		removed_in="2.0.0",
		current_version=__version__,
		details="Import from 'domdf_python_tools.iterative' instead.",
		)(
				iterative.chunks
				)
permutations = deprecated(
		deprecated_in="1.4.0",
		removed_in="2.0.0",
		current_version=__version__,
		details="Import from 'domdf_python_tools.iterative' instead.",
		)(
				iterative.permutations
				)
split_len = deprecated(
		deprecated_in="1.4.0",
		removed_in="2.0.0",
		current_version=__version__,
		details="Import from 'domdf_python_tools.iterative' instead.",
		)(
				iterative.split_len
				)
Len = deprecated(
		deprecated_in="1.4.0",
		removed_in="2.0.0",
		current_version=__version__,
		details="Import from 'domdf_python_tools.iterative' instead.",
		)(
				iterative.Len
				)
double_chain = deprecated(
		deprecated_in="1.4.0",
		removed_in="2.0.0",
		current_version=__version__,
		details="Import from 'domdf_python_tools.iterative' instead.",
		)(
				iterative.double_chain
				)


@deprecated(
		deprecated_in="1.4.0",
		removed_in="2.0.0",
		current_version=__version__,
		details="Import from :mod:`shippinglabel.requirements` instead.",
		)
def check_dependencies(dependencies: Iterable[str], prt: bool = True) -> List[str]:
	"""
	Check whether one or more dependencies are available to be imported.

	:param dependencies: The list of dependencies to check the availability of.
	:param prt: Whether the status should be printed to the terminal.

	:return: A list of any missing modules.
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
			print("The following modules are missing:")
			print(missing_modules)
			print("Please check the documentation.")
		print('')

	return missing_modules


@deprecated(
		deprecated_in="1.4.0",
		removed_in="2.0.0",
		current_version=__version__,
		details="Import from :mod:`consolekit.utils` (v0.3.0 or later) instead.",
		)
def coloured_diff(
		a: typing.Sequence[str],
		b: typing.Sequence[str],
		fromfile: str = '',
		tofile: str = '',
		fromfiledate: str = '',
		tofiledate: str = '',
		n: int = 3,
		lineterm: str = '\n',
		removed_colour: Colour = Fore.RED,
		added_colour: Colour = Fore.GREEN,
		) -> str:
	r"""
	Compare two sequences of lines; generate the delta as a unified diff.

	Unified diffs are a compact way of showing line changes and a few
	lines of context. The number of context lines is set by ``n`` which
	defaults to three.

	By default, the diff control lines (those with ``---``, ``+++``, or ``@@``)
	are created with a trailing newline. This is helpful so that inputs
	created from ``file.readlines()`` result in diffs that are suitable for
	``file.writelines()`` since both the inputs and outputs have trailing
	newlines.

	For inputs that do not have trailing newlines, set the lineterm
	argument to ``''`` so that the output will be uniformly newline free.

	The unidiff format normally has a header for filenames and modification
	times. Any or all of these may be specified using strings for
	``fromfile``, ``tofile``, ``fromfiledate``, and ``tofiledate``.
	The modification times are normally expressed in the ISO 8601 format.

	**Example:**

	>>> for line in coloured_diff('one two three four'.split(),
	...             'zero one tree four'.split(), 'Original', 'Current',
	...             '2005-01-26 23:30:50', '2010-04-02 10:20:52',
	...             lineterm=''):
	...     print(line)                 # doctest: +NORMALIZE_WHITESPACE
	--- Original        2005-01-26 23:30:50
	+++ Current         2010-04-02 10:20:52
	@@ -1,4 +1,4 @@
	+zero
	one
	-two
	-three
	+tree
	four

	:param a:
	:param b:
	:param fromfile:
	:param tofile:
	:param fromfiledate:
	:param tofiledate:
	:param n:
	:param lineterm:
	:param removed_colour: The :class:`~domdf_python_tools.terminal_colours.Colour` to use for lines that were removed.
	:param added_colour: The :class:`~domdf_python_tools.terminal_colours.Colour` to use for lines that were added.
	"""

	# this package
	from domdf_python_tools.stringlist import StringList

	buf = StringList()
	diff = difflib.unified_diff(a, b, fromfile, tofile, fromfiledate, tofiledate, n, lineterm)

	for line in diff:
		if line.startswith('+'):
			buf.append(added_colour(line))
		elif line.startswith('-'):
			buf.append(removed_colour(line))
		else:
			buf.append(line)

	buf.blankline(ensure_single=True)

	return str(buf)
