#!/usr/bin/env python
#
#  iterative.py
"""
Functions for iteration, looping etc.

.. versionadded:: 1.4.0
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
#  chunks from https://stackoverflow.com/a/312464/3092681
# 		Copyright © 2008 Ned Batchelder
# 		Licensed under CC-BY-SA
#

# stdlib
import itertools
import textwrap
from typing import Any, Generator, Iterable, Iterator, List, Sequence, Tuple, Type, Union

__all__ = [
		"chunks",
		"permutations",
		"split_len",
		"Len",
		"double_chain",
		"flatten",
		"make_tree",
		]


def chunks(l: Sequence[Any], n: int) -> Generator[Any, None, None]:
	"""
	Yield successive n-sized chunks from l.

	:param l: The objects to yield chunks from
	:param n: The size of the chunks

	.. versionchanged:: 1.4.0 Moved from :mod:`domdf_python_tools.utils`
	"""

	for i in range(0, len(l), n):
		yield l[i:i + n]


def permutations(data: Iterable[Any], n: int = 2) -> List[Tuple[Any, ...]]:
	"""
	Return permutations containing ``n`` items from ``data`` without any reverse duplicates.

	If ``n`` is equal to or greater than the length of the data an empty list of returned.

	:param data:
	:param n:

	.. versionchanged:: 1.4.0 Moved from :mod:`domdf_python_tools.utils`
	"""

	if n == 0:
		raise ValueError("'n' cannot be 0")

	perms = []
	for i in itertools.permutations(data, n):
		if i[::-1] not in perms:
			perms.append(i)

	return perms


def split_len(string: str, n: int) -> List[str]:
	"""
	Split a string every ``n`` characters.

	:param string: The string to split
	:param n: The number of characters to split after

	:return: The split string

	.. versionchanged:: 1.4.0 Moved from :mod:`domdf_python_tools.utils`
	"""

	return [string[i:i + n] for i in range(0, len(string), n)]


def Len(obj: Any, start: int = 0, step: int = 1) -> range:
	"""
	Shorthand for ``range(len(obj))``.

	Returns an object that produces a sequence of integers from start (inclusive)
	to len(obj) (exclusive) by step.

	:param obj: The object to iterate over the length of.
	:param start: The start value of the range.
	:param step: The step of the range.

	.. versionadded:: 0.4.7

	.. versionchanged:: 1.4.0 Moved from :mod:`domdf_python_tools.utils`
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

	:rtype:

	.. versionadded:: 0.4.7

	.. versionchanged:: 1.4.0 Moved from :mod:`domdf_python_tools.utils`
	"""

	yield from itertools.chain.from_iterable(itertools.chain.from_iterable(iterable))


def flatten(iterable: Iterable, primitives: Tuple[Type, ...] = (str, int, float)):
	"""
	Flattens a mixed list of primitive types and iterables of those types into a single list,
	regardless of nesting.

	:param iterable:
	:param primitives: The primitive types to allow.

	.. versionadded:: 1.4.0
	"""  # noqa: D400

	for item in iterable:
		if isinstance(item, primitives):
			yield item
		elif isinstance(item, Iterable):
			yield from flatten(item)
		else:
			raise NotImplementedError


Branch = Union[Sequence[str], Sequence[Union[Sequence[str], Sequence]]]


def make_tree(tree: Branch) -> Iterator[str]:
	"""
	Returns the string representation of a mixed list of strings and lists of strings,
	similar to :manpage:`tree(1)`.

	:param tree:

	.. versionadded:: 1.4.0
	"""  # noqa: D400

	last_string = 0
	for idx, entry in enumerate(tree):
		if isinstance(entry, str):
			last_string = idx

	for idx, entry in enumerate(tree[:-1]):
		if isinstance(entry, str):
			if idx > last_string:
				yield f"│   {entry}"
			elif idx == last_string:
				yield f"└── {entry}"
			else:
				yield f"├── {entry}"

		elif isinstance(entry, Iterable):
			for line in make_tree(entry):
				if idx - 1 == last_string:
					yield textwrap.indent(line, "└── ")
				else:
					yield textwrap.indent(line, "│   ")

	if tree:
		if isinstance(tree[-1], str):
			yield f"└── {tree[-1]}"
		elif isinstance(tree[-1], Iterable):
			for line in make_tree(tree[-1]):
				yield textwrap.indent(line, "    ")
