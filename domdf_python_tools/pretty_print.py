#!/usr/bin/env python
# cython: language_level=3
#
#  utils.py
"""
Functions and classes for pretty printing.

.. versionadded:: 0.10.0
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
from io import StringIO
from pprint import PrettyPrinter, _safe_key  # type: ignore
from typing import Any, Callable, Iterator, MutableMapping, Tuple

__all__ = ["FancyPrinter", "simple_repr"]


class FancyPrinter(PrettyPrinter):
	"""
	Subclass of :class:`~.pprint.PrettyPrinter` with different formatting.
	"""

	# TODO: docs
	_dispatch: MutableMapping[Callable, Callable]
	_indent_per_level: int
	_format_items: Callable[[PrettyPrinter, Any, Any, Any, Any, Any, Any], None]
	_dispatch = dict(PrettyPrinter._dispatch)  # type: ignore

	def _make_open(self, char: str, indent: int, obj):
		if self._indent_per_level > 1:
			the_indent = ' ' * (indent + 1)
		else:
			the_indent = ' ' * (indent + self._indent_per_level)

		if len(obj) and not self._compact:  # type: ignore
			return f"{char}\n{the_indent}"
		else:
			return char

	def _make_close(self, char: str, indent: int, obj):
		if len(obj) and not self._compact:  # type: ignore
			return f",\n{' ' * (indent + self._indent_per_level)}{char}"
		else:
			return char

	def _pprint_dict(self, object, stream, indent, allowance, context, level):
		write = stream.write
		write(self._make_open('{', indent, object))

		if self._indent_per_level > 1:
			write((self._indent_per_level - 1) * ' ')

		if len(object):
			self._format_dict_items(  # type: ignore
				object.items(),
				stream,
				indent,
				allowance + 1,
				context,
				level,
				)

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

	def format_attributes(self, obj: Attributes):
		stream = StringIO()
		context = {}

		context[id(obj)] = 1

		stream.write(f"(\n{self._indent_per_level * ' '}")

		if self._indent_per_level > 1:
			stream.write((self._indent_per_level - 1) * ' ')

		if len(obj):
			self._format_attribute_items(list(obj), stream, 0, 0 + 1, context, 1)
		stream.write(f"\n{self._indent_per_level * ' '})")

		del context[id(obj)]
		return stream.getvalue()

	def _format_attribute_items(self, items, stream, indent, allowance, context, level):

		write = stream.write
		indent += self._indent_per_level
		delimnl = ',\n' + ' ' * indent
		last_index = len(items) - 1

		for i, (key, ent) in enumerate(items):
			last = i == last_index
			write(key)
			write('=')
			self._format(  # type: ignore
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
	Adds a simple ``__repr__`` method to the decorated class.

	:param attributes: The attributes to include in the ``__repr__``.
	:param show_module: Whether to show the name of the module in the ``__repr__``.
	:param \*\*kwargs: Keyword arguments passed on to :class:`pprint.PrettyPrinter`.
	"""

	def deco(obj):

		def __repr__(self) -> str:
			if kwargs:
				formatter = ReprPrettyPrinter(**kwargs)
			else:
				formatter = _default_formatter

			class_name = f"{type(self).__module__}.{type(self).__name__}" if show_module else type(self).__name__

			return f"{class_name}{formatter.format_attributes(Attributes(self, *attributes))}"

		__repr__.__doc__ = f"Return a string representation of the :class:`~{obj.__module__}.{obj.__name__}`."
		__repr__.__name__ = "__repr__"
		__repr__.__module__ = obj.__module__
		__repr__.__qualname__ = f"{obj.__module__}.__repr__"
		obj.__repr__ = __repr__

		return obj

	return deco
