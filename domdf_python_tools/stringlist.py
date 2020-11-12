#!/usr/bin/env python
#
#  stringlist.py
"""
A list of strings that represent lines in a multiline string.

.. versionchanged:: 1.0.0

	:class:`~domdf_python_tools.typing.String` should now be imported from :mod:`domdf_python_tools.typing`.
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
from contextlib import contextmanager
from typing import Any, Iterable, Iterator, List, Tuple, TypeVar, Union, cast, overload

# this package
from domdf_python_tools.doctools import prettify_docstrings
from domdf_python_tools.typing import String
from domdf_python_tools.utils import convert_indents

__all__ = ["Indent", "StringList", "DelimitedList"]

_S = TypeVar("_S")


@prettify_docstrings
class Indent:
	"""
	Represents an indent, having a symbol/type and a size.

	:param size: The indent size.
	:param type: The indent character.
	"""

	def __init__(self, size: int = 0, type: str = '\t'):  # noqa A002  # pylint: disable=redefined-builtin
		self.size = int(size)
		self.type = str(type)

	def __iter__(self) -> Iterator[Union[str, Any]]:
		"""
		Returns the size and type of the :class:`~domdf_python_tools.stringlist.Indent`.
		"""

		yield self.size
		yield self.type

	@property
	def size(self) -> int:
		"""
		The indent size.
		"""

		return self._size

	@size.setter
	def size(self, size: int) -> None:
		self._size = int(size)

	@property  # noqa: A002,A003
	def type(self) -> str:  # noqa: A002,A003  # pylint: disable=redefined-builtin
		"""
		The indent character.
		"""

		return self._type

	@type.setter  # noqa: A002,A003  # pylint: disable=redefined-builtin
	def type(self, type: str) -> None:  # noqa A002  # pylint: disable=redefined-builtin
		if not str(type):
			raise ValueError("'type' cannot an empty string.")

		self._type = str(type)

	def __str__(self) -> str:
		"""
		Returns the :class:`~domdf_python_tools.stringlist.Indent` as a string.
		"""

		return self.type * self.size

	def __repr__(self) -> str:
		"""
		Returns the string representation of the :class:`~domdf_python_tools.stringlist.Indent`.
		"""

		return f"{type(self).__name__}(size={self.size}, type={self.type!r})"

	def __eq__(self, other):
		if isinstance(other, Indent):
			return other.size == self.size and other.type == self.type
		elif isinstance(other, str):
			return str(self) == other
		elif isinstance(other, tuple):
			return tuple(self) == other
		else:
			return NotImplemented


class StringList(List[str]):
	"""
	A list of strings that represent lines in a multiline string.

	:param iterable: Content to populate the StringList with.
	:param convert_indents: Whether indents at the start of lines should be converted.
	"""

	#: The indent to insert at the beginning of new lines.
	indent: Indent

	convert_indents: bool
	"""
	Whether indents at the start of lines should be converted.

	Only applies to lines added after this is enabled/disabled.

	Can only be used when the indent is ``'\\t'`` or ``'␣'``.
	"""

	def __init__(self, iterable: Iterable[String] = (), convert_indents: bool = False) -> None:
		if isinstance(iterable, str):
			iterable = iterable.split('\n')

		self.indent = Indent()
		self.convert_indents = convert_indents
		super().__init__([self._make_line(str(x)) for x in iterable])

	def _make_line(self, line: str) -> str:
		if not str(self.indent_type).strip(" \t") and self.convert_indents:
			if self.indent_type == '\t':
				line = convert_indents(line, tab_width=1, from_="    ", to='\t')
			else:  # pragma: no cover
				line = convert_indents(line, tab_width=1, from_='\t', to=self.indent_type)

		return f"{self.indent}{line}".rstrip()

	def append(self, line: String) -> None:
		"""
		Append a line to the end of the :class:`~domdf_python_tools.stringlist.StringList`.

		:param line:
		"""

		for inner_line in str(line).split('\n'):
			super().append(self._make_line(inner_line))

	def extend(self, iterable: Iterable[String]) -> None:
		"""
		Extend the :class:`~domdf_python_tools.stringlist.StringList` with lines from ``iterable``.

		:param iterable: An iterable of string-like objects to add to the end of the
			:class:`~domdf_python_tools.stringlist.StringList`.
		"""

		for line in iterable:
			self.append(line)

	def copy(self) -> "StringList":
		"""
		Returns a shallow copy of the :class:`~domdf_python_tools.stringlist.StringList`.

		Equivalent to ``a[:]``.
		"""

		return self.__class__(super().copy())

	def count_blanklines(self) -> int:
		"""
		Returns a count of the blank lines in the :class:`~domdf_python_tools.stringlist.StringList`.

		.. versionadded:: 0.7.1
		"""

		return self.count('')

	def insert(self, index: int, line: String) -> None:
		"""
		Insert a line into the :class:`~domdf_python_tools.stringlist.StringList` at the given position.

		:param index:
		:param line:
		"""

		lines: List[str]

		if index < 0 or index > len(self):
			lines = str(line).split('\n')
		else:
			lines = cast(list, reversed(str(line).split('\n')))

		for inner_line in lines:
			super().insert(index, self._make_line(inner_line))

	@overload
	def __setitem__(self, index: int, line: String) -> None:
		...  # pragma: no cover

	@overload
	def __setitem__(self, index: slice, line: Iterable[String]) -> None:
		...  # pragma: no cover

	def __setitem__(self, index: Union[int, slice], line: Union[String, Iterable[String]]):
		"""
		Replaces the given line with new content.

		If the new content consists of multiple lines subsequent content in the
		:class:`~domdf_python_tools.stringlist.StringList` will be shifted down.

		:param index:
		:param line:
		"""

		if isinstance(index, int):
			if self and index < len(self):
				self.pop(index)
			if index < 0:
				index = len(self) + index + 1
			self.insert(index, line)

		elif isinstance(index, slice):
			for line, index in zip(
				reversed(line),  # type: ignore
				reversed(range(index.start or 0, index.stop + 1, index.step or 1)),
				):
				self[index] = line

	@overload
	def __getitem__(self, index: int) -> str:
		...  # pragma: no cover

	@overload
	def __getitem__(self, index: slice) -> List[str]:
		...  # pragma: no cover

	def __getitem__(self, index: Union[int, slice]) -> Union[str, List[str]]:
		"""
		Returns the line with the given index.

		:param index:
		"""

		return super().__getitem__(index)

	def blankline(self, ensure_single: bool = False):
		"""
		Append a blank line to the end of the :class:`~domdf_python_tools.stringlist.StringList`.

		:param ensure_single: Ensure only a single blank line exists after the previous line of text.
		"""

		if ensure_single:
			while self and not self[-1]:
				self.pop(-1)

		self.append('')

	def set_indent_size(self, size: int = 0):
		"""
		Sets the size of the indent to insert at the beginning of new lines.

		:param size: The indent size to use for new lines.
		"""

		self.indent.size = int(size)

	def set_indent_type(self, indent_type: str = '\t'):
		"""
		Sets the type of the indent to insert at the beginning of new lines.

		:param indent_type: The type of indent to use for new lines.
		"""

		self.indent.type = str(indent_type)

	def set_indent(self, indent: Union[String, Indent], size: int = 0):
		"""
		Sets the indent to insert at the beginning of new lines.

		:param indent: The :class:`~.Indent` to use for new lines, or the indent type.
		:param size: If ``indent`` is an indent type, the indent size to use for new lines.
		"""

		if isinstance(indent, Indent):
			if size:
				raise TypeError("'size' argument cannot be used when providing an 'Indent' object.")

			self.indent = indent
		else:
			self.indent = Indent(int(size), str(indent))

	@property
	def indent_size(self) -> int:
		"""
		The current indent size.
		"""

		return int(self.indent.size)

	@indent_size.setter
	def indent_size(self, size: int) -> None:
		"""
		Sets the indent size.
		"""

		self.indent.size = int(size)

	@property
	def indent_type(self) -> str:
		"""
		The current indent type.
		"""

		return str(self.indent.type)

	@indent_type.setter
	def indent_type(self, type: str) -> None:  # noqa: A002  # pylint: disable=redefined-builtin
		"""
		Sets the indent type.
		"""

		self.indent.type = str(type)

	def __str__(self) -> str:
		"""
		Returns the :class:`~domdf_python_tools.stringlist.StringList` as a string.
		"""

		return '\n'.join(self)

	def __eq__(self, other) -> bool:
		"""
		Returns whether the other object is equal to this :class:`~domdf_python_tools.stringlist.StringList`.
		"""

		if isinstance(other, str):
			return str(self) == other
		else:
			return super().__eq__(other)

	@contextmanager
	def with_indent(self, indent: Union[String, Indent], size: int = 0):
		"""
		Context manager to temporarily use a different indent.

		.. code-block:: python

			>>> sl = StringList()
			>>> with sl.with_indent("    ", 1):
			...     sl.append("Hello World")

		:param indent: The :class:`~.Indent` to use within the ``with`` block, or the indent type.
		:param size: If ``indent`` is an indent type, the indent size to use within the ``with`` block.
		"""

		original_indent: Tuple[int, str] = tuple(self.indent)  # type: ignore

		try:
			self.set_indent(indent, size)
			yield
		finally:
			self.indent = Indent(*original_indent)

	@contextmanager
	def with_indent_size(self, size: int = 0):
		"""
		Context manager to temporarily use a different indent size.

		.. code-block:: python

			>>> sl = StringList()
			>>> with sl.with_indent_size(1):
			...     sl.append("Hello World")

		:param size: The indent size to use within the ``with`` block.
		"""

		original_indent_size = self.indent_size

		try:
			self.indent_size = size
			yield
		finally:
			self.indent_size = original_indent_size

	@contextmanager
	def with_indent_type(self, indent_type: str = '\t'):
		"""
		Context manager to temporarily use a different indent type.

		.. code-block:: python

			>>> sl = StringList()
			>>> with sl.with_indent_type("    "):
			...     sl.append("Hello World")

		:param indent_type: The type of indent to use within the ``with`` block.
		"""

		original_indent_type = self.indent_type

		try:
			self.indent_type = indent_type
			yield
		finally:
			self.indent_type = original_indent_type


class DelimitedList(List[_S]):
	"""
	Subclass of :class:`list` that supports custom delimiters in format strings.

	**Example:**

	.. code-block::

		>>> l = DelimitedList([1, 2, 3, 4, 5])
		>>> format(l, ", ")
		'1, 2, 3, 4, 5'
		>>> f"Numbers: {l:, }"
		'Numbers: 1, 2, 3, 4, 5'

	.. versionadded:: 1.1.0
	"""

	def __format__(self, format_spec: str) -> str:
		return format_spec.join([str(x) for x in self])
