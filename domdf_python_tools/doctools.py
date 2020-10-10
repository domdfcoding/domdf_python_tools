#  !/usr/bin/env python
#
#  doctools.py
"""
Utilities for documenting functions, classes and methods.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#  Based on https://softwareengineering.stackexchange.com/a/386758
#  Copyright © amon (https://softwareengineering.stackexchange.com/users/60357/amon)
#  Licensed under CC BY-SA 4.0
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
import builtins
import platform
from inspect import cleandoc
from types import MethodType
from typing import Any, Callable, Dict, Optional, Sequence, Type, TypeVar, Union

# this package
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.typing import MethodDescriptorType, MethodWrapperType, WrapperDescriptorType

__all__ = [
		"F",
		"deindent_string",
		"document_object_from_another",
		"append_doctring_from_another",
		"make_sphinx_links",
		"is_documented_by",
		"append_docstring_from",
		"sphinxify_docstring",
		"prettify_docstrings",
		]

F = TypeVar('F', bound=Callable[..., Any])
PYPY = platform.python_implementation() == "PyPy"


def deindent_string(string: Optional[str]) -> str:
	"""
	Removes all indentation from the given string.

	:param string: The string to deindent

	:return: The string without indentation
	"""

	if not string:
		# Short circuit if empty string or None
		return ''

	split_string = string.split("\n")
	deindented_string = [line.lstrip("\t ") for line in split_string]
	return "\n".join(deindented_string)


# Functions that do the work
def document_object_from_another(target: Union[Type, Callable], original: Union[Type, Callable]):
	"""
	Sets the docstring of the ``target`` function to that of the ``original`` function.

	This may be useful for subclasses or wrappers that use the same arguments.

	:param target: The object to set the docstring for
	:param original: The object to copy the docstring from
	"""

	target.__doc__ = original.__doc__


def append_doctring_from_another(target: Union[Type, Callable], original: Union[Type, Callable]):
	"""
	Sets the docstring of the ``target`` function to that of the ``original`` function.

	This may be useful for subclasses or wrappers that use the same arguments.

	Any indentation in either docstring is removed to
	ensure consistent indentation between the two docstrings.
	Bear this in mind if additional indentation is used in the docstring.

	:param target: The object to append the docstring to
	:param original: The object to copy the docstring from
	"""

	target_doc = target.__doc__
	original_doc = original.__doc__

	if isinstance(original_doc, str) and isinstance(target_doc, str):
		docstring = StringList(cleandoc(target_doc))
		docstring.blankline(ensure_single=True)
		docstring.append(cleandoc(original_doc))
		docstring.blankline(ensure_single=True)
		target.__doc__ = str(docstring)

	elif not isinstance(target_doc, str) and isinstance(original_doc, str):
		docstring = StringList(cleandoc(original_doc))
		docstring.blankline(ensure_single=True)
		target.__doc__ = str(docstring)


def make_sphinx_links(input_string: str, builtins_list: Optional[Sequence[str]] = None) -> str:
	r"""
	Make proper sphinx links out of double-backticked strings in docstring.

	i.e.

	.. code-block:: rest

		``str``

	becomes

	.. code-block:: rest

		:class:`~python:str`

	Make sure to have ``'python': ('https://docs.python.org/3/', None),`` in the
	``intersphinx_mapping`` dict of your ``conf.py`` file for Sphinx.

	:param input_string: The string to process.
	:param builtins_list: A list of builtins to make links for.
	:default builtins_list: dir(:py:obj:`builtins`)

	:return: Processed string with links.
	"""  # noqa SXL001

	if builtins_list is None:
		builtins_list = dir(builtins)

	working_string = f"{input_string}"

	for builtin in {x for x in builtins_list if not x.startswith("__") and x != "None"}:
		working_string = working_string.replace(f"``{builtin}``", f":class:`~python:{builtin}`")

	return working_string


# Decorators that call the above functions
def is_documented_by(original: F) -> Callable:
	"""
	Decorator to set the docstring of the ``target`` function to that of the ``original`` function.

	This may be useful for subclasses or wrappers that use the same arguments.
	"""

	def wrapper(target: F) -> F:
		document_object_from_another(target, original)
		return target

	return wrapper


def append_docstring_from(original: F) -> Callable:
	"""
	Decorator to appends the docstring from the ``original`` function to the ``target`` function.

	This may be useful for subclasses or wrappers that use the same arguments.

	Any indentation in either docstring is removed to
	ensure consistent indentation between the two docstrings.
	Bear this in mind if additional indentation is used in the docstring.
	"""

	def wrapper(target: F) -> F:
		append_doctring_from_another(target, original)
		return target

	return wrapper


def sphinxify_docstring() -> Callable:
	r"""
	Decorator to make proper sphinx links out of double-backticked strings in the docstring.

	i.e.

	.. code-block:: rest

		``str``

	becomes

	.. code-block:: rest

		:class:`~python:str`

	Make sure to have ``'python': ('https://docs.python.org/3/', None),`` in the
	``intersphinx_mapping`` dict of your ``conf.py`` file for Sphinx.
	"""  # noqa SXL001

	def wrapper(target: F) -> F:
		target_doc = target.__doc__

		if target_doc:
			target.__doc__ = make_sphinx_links(target_doc)

		return target

	return wrapper


# Check against object
base_new_docstrings = {
		"__delattr__": "Implement :func:`delattr(self, name) <delattr>`.",
		"__dir__": "Default :func:`dir` implementation.",
		"__eq__": "Return ``self == other``.",  # __format__
		"__getattribute__": "Return :func:`getattr(self, name) <getattr>`.",
		"__ge__": "Return ``self >= other``.",
		"__gt__": "Return ``self > other``.",
		"__hash__": "Return :func:`hash(self) <hash>`.",
		# __init_subclass__
		# __init__  # not usually shown in sphinx
		"__lt__": "Return ``self < other``.",
		"__le__": "Return ``self <= other``.",  # __new__
		"__ne__": "Return ``self != other``.",
		# __reduce_ex__
		# __reduce__
		# __repr__ is defined within the function
		"__setattr__": "Implement :func:`setattr(self, name) <setattr>`.",
		"__sizeof__": "Returns the size of the object in memory, in bytes.",
		"__str__": "Return :class:`str(self) <str>`.",  # __subclasshook__
		}

# Check against dict
container_docstrings = {
		"__contains__": "Return ``key in self``.",
		"__getitem__": "Return ``self[key]``.",
		"__setitem__": "Set ``self[key]`` to ``value``.",
		"__delitem__": "Delete ``self[key]``.",
		}

# Check against int
operator_docstrings = {
		"__and__": "Return ``self & value``.",
		"__add__": "Return ``self + value``.",
		"__abs__": "Return :func:`abs(self) <abs>`.",
		"__divmod__": "Return :func:`divmod(self, value) <divmod>`.",
		"__floordiv__": "Return ``self // value``.",
		"__invert__": "Return ``~ self``.",
		"__lshift__": "Return ``self << value``.",
		"__mod__": "Return ``self % value``.",
		"__mul__": "Return ``self * value``.",
		"__neg__": "Return ``- self``.",
		"__or__": "Return ``self | value``.",
		"__pos__": "Return ``+ self``.",
		"__pow__": "Return :func:`pow(self, value, mod) <pow>`.",
		"__radd__": "Return ``value + self``.",
		"__rand__": "Return ``value & self``.",
		"__rdivmod__": "Return :func:`divmod(value, self) <divmod>`.",
		"__rfloordiv__": "Return ``value // self``.",
		"__rlshift__": "Return ``value << self``.",
		"__rmod__": "Return ``value % self``.",
		"__rmul__": "Return ``value * self``.",
		"__ror__": "Return ``value | self``.",
		"__rpow__": "Return :func:`pow(value, self, mod) <pow>`.",
		"__rrshift__": "Return ``self >> value``.",
		"__rshift__": "Return ``self >> value``.",
		"__rsub__": "Return ``value - self``.",
		"__rtruediv__": "Return ``value / self``.",
		"__rxor__": "Return ``value ^ self``.",
		"__sub__": "Return ``value - self``.",
		"__truediv__": "Return ``self / value``.",
		"__xor__": "Return ``self ^ value``.",
		}

# Check against int
base_int_docstrings = {
		# "__bool__": "Return ``self != 0`.",  # TODO
		# __ceil__
		"__float__": "Return :func:`float(self) <float>`.",  # __floor__
		"__int__": "Return :func:`int(self) <int>`.",  # __round__
		}

new_return_types = {
		"__eq__": bool,
		"__ge__": bool,
		"__gt__": bool,
		"__lt__": bool,
		"__le__": bool,
		"__ne__": bool,
		"__repr__": str,
		"__str__": str,
		"__int__": int,
		"__float__": float,
		"__bool__": bool,
		}


def _do_prettify(obj: Type, base: Type, new_docstrings: Dict[str, str]):
	"""
	Perform the actual prettification for :func`~.prettify_docstrings`.

	:param obj:
	:param base:
	:param new_docstrings:

	:rtype:

	.. versionadded:: 0.8.0
	"""

	for attr_name in new_docstrings:

		if not hasattr(obj, attr_name):
			continue

		attribute = getattr(obj, attr_name)

		if not PYPY and isinstance(
				attribute,
				(WrapperDescriptorType, MethodDescriptorType, MethodWrapperType, MethodType),
				):
			continue
		elif PYPY and isinstance(attribute, MethodType):
			continue  # pragma: no cover (!PyPy)

		if attribute is None:
			continue

		base_docstring: Optional[str] = None
		if hasattr(base, attr_name):
			base_docstring = getattr(base, attr_name).__doc__

		doc: Optional[str] = attribute.__doc__
		if doc in {None, base_docstring}:
			attribute.__doc__ = new_docstrings[attr_name]


def prettify_docstrings(obj: Type) -> Type:
	"""
	Prettify the default :class:`object` docstrings for use in Sphinx documentation.

	:param obj: The object to prettify the method docstrings for.

	:return: The object

	.. versionadded:: 0.8.0
	"""

	repr_docstring = f"Return a string representation of the :class:`~{obj.__module__}.{obj.__name__}`."
	new_docstrings = {**base_new_docstrings, "__repr__": repr_docstring}

	_do_prettify(obj, object, new_docstrings)
	_do_prettify(obj, dict, container_docstrings)
	_do_prettify(obj, int, operator_docstrings)
	_do_prettify(obj, int, base_int_docstrings)

	for attribute in new_return_types:
		if hasattr(obj, attribute):
			annotations: Dict = getattr(getattr(obj, attribute), "__annotations__", {})

			if "return" not in annotations or annotations["return"] is Any:
				annotations["return"] = new_return_types[attribute]

			try:
				getattr(obj, attribute).__annotations__ = annotations
			except AttributeError:  # pragma: no cover
				pass

	if issubclass(obj, tuple) and obj.__repr__.__doc__ == "Return a nicely formatted representation string":
		obj.__repr__.__doc__ = repr_docstring

	return obj
