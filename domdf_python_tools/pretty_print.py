#!/usr/bin/env python
# cython: language_level=3
#
#  utils.py
"""
Functions and classes for pretty printing.

.. versionadded:: 1.0.0
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
#  Based on CPython.
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#

# stdlib
import re
from io import StringIO
from pprint import PrettyPrinter, _recursion, _safe_key, _safe_tuple  # type: ignore
from typing import Any, Callable, Iterator, MutableMapping, Optional, Tuple

# this package
from domdf_python_tools.stringlist import StringList

__all__ = ["FancyPrinter", "pformat_tabs", "Attributes", "ReprPrettyPrinter", "simple_repr"]


class FancyPrinter(PrettyPrinter):
	# TODO: docs
	_dispatch: MutableMapping[Callable, Callable]
	_indent_per_level: int
	_format_items: Callable[[Any, Any, Any, Any, Any, Any], None]
	_dispatch = dict(PrettyPrinter._dispatch)  # type: ignore

	def _make_open(self, char: str, indent: int, obj):
		if self._indent_per_level > 1:
			the_indent = ' ' * (indent + 1)
		else:
			the_indent = ' ' * (indent + self._indent_per_level)

		if len(obj) and not self._compact:
			return f"{char}\n{the_indent}"
		else:
			return char

	def _make_close(self, char: str, indent: int, obj):
		if len(obj) and not self._compact:
			return f",\n{' ' * (indent + self._indent_per_level)}{char}"
		else:
			return char

	def _pprint_dict(self, object, stream, indent, allowance, context, level):
		write = stream.write
		write(self._make_open('{', indent, object))

		if self._indent_per_level > 1:
			write((self._indent_per_level - 1) * ' ')

		if len(object):
			self._format_dict_items(object.items(), stream, indent, allowance + 1, context, level)

		write(self._make_close('}', indent, object))

	_dispatch[dict.__repr__] = _pprint_dict

	def _pprint_list(self, object, stream, indent, allowance, context, level):
		stream.write(self._make_open('[', indent, object))
		self._format_items(object, stream, indent, allowance + 1, context, level)
		stream.write(self._make_close(']', indent, object))

	_dispatch[list.__repr__] = _pprint_list

	def _pprint_tuple(self, object, stream, indent, allowance, context, level):
		stream.write(self._make_open('(', indent, object))
		endchar = ",)" if len(object) == 1 else self._make_close(')', indent, object)
		self._format_items(object, stream, indent, allowance + len(endchar), context, level)
		stream.write(endchar)

	_dispatch[tuple.__repr__] = _pprint_tuple

	def _pprint_set(self, object, stream, indent, allowance, context, level):
		if not len(object):
			stream.write(repr(object))
			return
		typ = object.__class__
		if typ is set:
			stream.write(self._make_open('{', indent, object))
			endchar = self._make_close('}', indent, object)
		else:
			stream.write(typ.__name__ + f"({{\n{' ' * (indent + self._indent_per_level + len(typ.__name__) + 1)}")
			endchar = f",\n{' ' * (indent + self._indent_per_level + len(typ.__name__) + 1)}}})"
			indent += len(typ.__name__) + 1
		object = sorted(object, key=_safe_key)
		self._format_items(object, stream, indent, allowance + len(endchar), context, level)
		stream.write(endchar)

	_dispatch[set.__repr__] = _pprint_set
	_dispatch[frozenset.__repr__] = _pprint_set


def pformat_tabs(
		object: object,
		width: int = 80,
		depth: Optional[int] = None,
		*,
		compact: bool = False,
		) -> str:
	"""
	Format a Python object into a pretty-printed representation.
	Indentation is set at one tab.

	:param object:
	:param width:
	:param depth:
	:param compact:
	"""

	prettyprinter = FancyPrinter(indent=4, width=width, depth=depth, compact=compact)

	buf = StringList()
	for line in prettyprinter.pformat(object).splitlines():
		buf.append(re.sub("^ {4}", r"\t", line))

	return str(buf)


class Attributes:

	def __init__(self, obj: object, *attributes: str):
		self.obj = obj
		self.attributes = attributes

	def __iter__(self) -> Iterator[Tuple[str, Any]]:
		for attr in self.attributes:
			yield attr, getattr(self.obj, attr)

	def __len__(self) -> int:
		return len(self.attributes)

	def __repr__(self):
		return f"Attributes{self.attributes}"


class ReprPrettyPrinter(FancyPrinter):

	_dispatch = dict(FancyPrinter._dispatch)  # type: ignore

	def pformat(self, object):
		stream = StringIO()
		context = {}

		objid = id(object)
		if objid in context:
			stream.write(_recursion(object))
			self._recursive = True
			self._readable = False
			return

		p = self._dispatch.get(type(object).__repr__, None)

		context[objid] = 1
		p(self, object, stream, 0, 0, context, 1)
		del context[objid]
		return stream.getvalue()

	def _pprint_attributes(self, object, stream, indent, allowance, context, level):

		stream.write(f"(\n{self._indent_per_level * ' '}")

		if self._indent_per_level > 1:
			stream.write((self._indent_per_level - 1) * ' ')

		if len(object):
			self._format_attribute_items(list(object), stream, indent, allowance + 1, context, level)
		stream.write(f"\n{self._indent_per_level * ' '})")

	_dispatch[Attributes.__repr__] = _pprint_attributes

	def _format_attribute_items(self, items, stream, indent, allowance, context, level):

		write = stream.write
		indent += self._indent_per_level
		delimnl = ',\n' + ' ' * indent
		last_index = len(items) - 1

		for i, (key, ent) in enumerate(items):
			last = i == last_index
			write(key)
			write('=')
			self._format(
					ent,
					stream,
					indent + len(key) + 2,
					allowance if last else 1,
					context,
					level,
					)

			if not last:
				write(delimnl)


_default_formatter = ReprPrettyPrinter()


def simple_repr(*attributes: str, show_module: bool = False, **kwargs):
	r"""
	Adds a simple ``__repr__` method to the decorated class.

	:param attributes: The attributes to include in the ``__repr__``.
	:param show_module: Whether to show the name of the module in the ``__repr__``.
	:param \*\*kwargs: Keyword arguments passed on to :class:`pprint.PrettyPrinter`.
		Has no effect if `multiline` is :py:obj:`False`.
	"""

	def deco(obj):

		def __repr__(self) -> str:
			if kwargs:
				formatter = ReprPrettyPrinter(**kwargs)
			else:
				formatter = _default_formatter

			class_name = f"{type(self).__module__}.{type(self).__name__}" if show_module else type(self).__name__

			return f"{class_name}{formatter.pformat(Attributes(self, *attributes))}"

		__repr__.__doc__ = f"Return a string representation of the :class:`~{obj.__module__}.{obj.__name__}`."
		__repr__.__name__ = "__repr__"
		__repr__.__module__ = obj.__module__
		__repr__.__qualname____ = f"{obj.__module__}.__repr__"
		obj.__repr__ = __repr__

		return obj

	return deco
