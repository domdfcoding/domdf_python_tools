#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  doctools.py
"""
Utilities for documenting functions, classes and methods
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
from textwrap import dedent
from typing import Any, Callable, Type, TypeVar, Union

F = TypeVar('F', bound=Callable[..., Any])


def deindent_string(string: str) -> str:
	"""
	Removes all indentation from the given string

	:param string: The string to deindent
	:type string: str

	:return: The string without indentation
	:rtype: str
	"""

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
		deindented_target_doc = dedent(target_doc)
		deindented_original_doc = dedent(original_doc)

		target.__doc__ = deindented_target_doc + "\n" + deindented_original_doc

	elif not isinstance(target_doc, str) and isinstance(original_doc, str):
		target.__doc__ = dedent(original_doc)


def make_sphinx_links(input_string, builtins_list=None):
	r"""
	Make proper sphinx links out of double-backticked strings in docstring.

	i.e. \`\`str\`\` becomes \:class\:\`~python:str\`


	Make sure to have `'python': ('https://docs.python.org/3/', None),` in the
	`intersphinx_mapping` dict of your conf.py for sphinx.

	:param input_string: The string to process
	:type input_string: str
	:param builtins_list: A list of builtins to make links for
	:type builtins_list: list of str

	:return: processed string with links
	:rtype: str
	"""

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

	i.e. \`\`str\`\` becomes \:class\:\`~python:str\`

	Make sure to have `'python': ('https://docs.python.org/3/', None),` in the
	`intersphinx_mapping` dict of your conf.py for sphinx.
	"""

	def wrapper(target: F) -> F:
		target.__doc__ = make_sphinx_links(target.__doc__)
		return target

	return wrapper
