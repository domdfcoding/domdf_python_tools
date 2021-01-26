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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  chunks from https://stackoverflow.com/a/312464/3092681
#  Copyright © 2008 Ned Batchelder
#  Licensed under CC-BY-SA
#

# stdlib
import itertools
import textwrap
from operator import itemgetter
from typing import Any, Callable, Iterable, Iterator, List, Optional, Sequence, Sized, Tuple, Type, TypeVar, Union

# 3rd party
from natsort import natsorted, ns  # type: ignore

# this package
from domdf_python_tools.utils import magnitude

__all__ = [
		"chunks",
		"permutations",
		"split_len",
		"Len",
		"double_chain",
		"flatten",
		"make_tree",
		"natmin",
		"natmax",
		"groupfloats",
		"ranges_from_iterable",
		"extend",
		"extend_with",
		"extend_with_none",
		]

_T = TypeVar("_T")


def chunks(l: Sequence[_T], n: int) -> Iterator[Sequence[_T]]:
	"""
	Yield successive ``n``-sized chunks from ``l``.

	:param l: The objects to yield chunks from.
	:param n: The size of the chunks.

	:rtype:

	.. versionchanged:: 1.4.0 Moved from :mod:`domdf_python_tools.utils`
	"""

	for i in range(0, len(l), n):
		yield l[i:i + n]


def permutations(data: Iterable[_T], n: int = 2) -> List[Tuple[_T, ...]]:
	"""
	Return permutations containing ``n`` items from ``data`` without any reverse duplicates.

	If ``n`` is equal to or greater than the length of the data an empty list of returned.

	:param data:
	:param n:

	:rtype:

	.. versionchanged:: 1.4.0 Moved from :mod:`domdf_python_tools.utils`

	.. seealso:: :func:`itertools.permutations` and :func:`itertools.combinations`
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
	Split ``string`` every ``n`` characters.

	:param string:
	:param n: The number of characters to split after

	:return: The split string

	.. versionchanged:: 1.4.0 Moved from :mod:`domdf_python_tools.utils`
	"""

	return [string[i:i + n] for i in range(0, len(string), n)]


def Len(obj: Sized, start: int = 0, step: int = 1) -> range:
	"""
	Shorthand for ``range(len(obj))``.

	Returns an object that produces a sequence of integers from ``start`` (inclusive)
	to :func:`len(obj) <len>` (exclusive) by ``step``.

	.. versionadded:: 0.4.7

	:param obj: The object to iterate over the length of.
	:param start: The start value of the range.
	:param step: The step of the range.

	:rtype:

	.. versionchanged:: 1.4.0 Moved from :mod:`domdf_python_tools.utils`
	"""

	return range(start, len(obj), step)


def double_chain(iterable: Iterable[Iterable[Iterable[_T]]]) -> Iterator[_T]:
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

	.. versionadded:: 0.4.7

	:param iterable: The iterable to chain.

	:rtype:

	.. versionchanged:: 1.4.0 Moved from :mod:`domdf_python_tools.utils`
	"""

	return itertools.chain.from_iterable(itertools.chain.from_iterable(iterable))


def flatten(iterable: Iterable[_T], primitives: Tuple[Type, ...] = (str, int, float)) -> Iterator[_T]:
	"""
	Flattens a mixed list of primitive types and iterables of those types into a single list,
	regardless of nesting.

	.. versionadded:: 1.4.0

	:param iterable:
	:param primitives: The primitive types to allow.
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

	.. versionadded:: 1.4.0

	:param tree:
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


def natmin(seq: Iterable[_T], key: Optional[Callable[[Any], Any]] = None, alg: int = ns.DEFAULT) -> _T:
	"""
	Returns the minimum value from ``seq`` when sorted naturally.

	.. versionadded:: 1.8.0

	:param seq:
	:param key: A key used to determine how to sort each element of the iterable.
		It is **not** applied recursively.
		The callable should accept a single argument and return a single value.
	:param alg: This option is used to control which algorithm :mod:`natsort` uses when sorting.
	"""

	return natsorted(seq, key=key, alg=alg)[0]


def natmax(seq: Iterable[_T], key: Optional[Callable[[Any], Any]] = None, alg: int = ns.DEFAULT) -> _T:
	"""
	Returns the maximum value from ``seq`` when sorted naturally.

	.. versionadded:: 1.8.0

	:param seq:
	:param key: A key used to determine how to sort each element of the iterable.
		It is **not** applied recursively.
		The callable should accept a single argument and return a single value.
	:param alg: This option is used to control which algorithm :mod:`natsort` uses when sorting.
	"""

	return natsorted(seq, key=key, alg=alg)[-1]


_group = Tuple[float, ...]


def groupfloats(
		iterable: Iterable[float],
		step: float = 1,
		) -> Iterable[_group]:
	"""
	Returns an iterator over the discrete ranges of values in ``iterable``.

	For example:

	.. code-block:: python

		>>> list(groupfloats([170.0, 170.05, 170.1, 170.15, 171.05, 171.1, 171.15, 171.2], step=0.05))
		[(170.0, 170.05, 170.1, 170.15), (171.05, 171.1, 171.15, 171.2)]
		>>> list(groupfloats([1, 2, 3, 4, 5, 7, 8, 9, 10]))
		[(1, 2, 3, 4, 5), (7, 8, 9, 10)]

	.. versionadded:: 2.0.0

	:param iterable:
	:param step: The step between values in ``iterable``.

	:rtype:

	.. seealso::

		:func:`~.ranges_from_iterable`, which returns an iterator over the min and max values for each range.
	"""

	# Based on https://stackoverflow.com/a/4629241
	# By user97370
	# CC BY-SA 4.0

	modifier = 1 / 10**magnitude(step)

	a: float
	b: Iterable[_group]

	def key(pair):
		return (pair[1] * modifier) - ((pair[0] * modifier) * step)

	for a, b in itertools.groupby(enumerate(iterable), key=key):
		yield tuple(map(itemgetter(1), list(b)))


def ranges_from_iterable(iterable: Iterable[float], step: float = 1) -> Iterable[Tuple[float, float]]:
	"""
	Returns an iterator over the minimum and maximum values for each discrete ranges of values in ``iterable``.

	For example:

	.. code-block:: python

		>>> list(ranges_from_iterable([170.0, 170.05, 170.1, 170.15, 171.05, 171.1, 171.15, 171.2], step=0.05))
		[(170.0, 170.15), (171.05, 171.2)]
		>>> list(ranges_from_iterable([1, 2, 3, 4, 5, 7, 8, 9, 10]))
		[(1, 5), (7, 10)]

	:param iterable:
	:param step: The step between values in ``iterable``.
	"""

	for group in groupfloats(iterable, step):
		yield group[0], group[-1]


def extend(sequence: Iterable[_T], minsize: int) -> List[_T]:
	"""
	Extend ``sequence`` by repetition until it is at least as long as ``minsize``.

	.. versionadded:: 2.3.0

	:param sequence:
	:param minsize:

	:rtype:

	.. seealso:: :func:`~.extend_with` and :func:`~.extend_with_none`
	"""

	output = list(sequence)
	cycle = itertools.cycle(output)

	while len(output) < minsize:
		output.append(next(cycle))

	return output


def extend_with(sequence: Iterable[_T], minsize: int, with_: _T) -> List[_T]:
	r"""
	Extend ``sequence`` by adding ``with\_`` to the right hand end until it is at least as long as ``minsize``.

	.. versionadded:: 2.3.0

	:param sequence:
	:param minsize:
	:param with\_:

	:rtype:

	.. seealso:: :func:`~.extend` and :func:`~.extend_with_none`
	"""

	output = list(sequence)

	while len(output) < minsize:
		output.append(with_)

	return output


def extend_with_none(sequence: Iterable[_T], minsize: int) -> Sequence[Optional[_T]]:
	r"""
	Extend ``sequence`` by adding :py:obj:`None` to the right hand end until it is at least as long as ``minsize``.

	.. versionadded:: 2.3.0

	:param sequence:
	:param minsize:

	:rtype:

	.. seealso:: :func:`~.extend` and :func:`~.extend_with`
	"""

	output: Sequence[Optional[_T]] = list(sequence)
	filler: Sequence[Optional[_T]] = [None] * max(0, minsize - len(output))

	return tuple((*output, *filler))
