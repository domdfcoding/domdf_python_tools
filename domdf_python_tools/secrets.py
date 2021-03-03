#  !/usr/bin/env python
#
#  secrets.py
"""
Functions for working with secrets, such as API tokens.

.. versionadded:: 0.4.6
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# this package
from domdf_python_tools.doctools import prettify_docstrings

__all__ = ["Secret"]


@prettify_docstrings
class Secret(str):
	"""
	Subclass of :py:class:`str` that guards against accidentally printing a secret to the terminal.

	The actual value of the secret is accessed via the ``.value`` attribute.

	The protection should be maintained even when the secret is in a list, tuple, set or dict,
	but you should still refrain from printing objects containing the secret.

	The secret overrides the :meth:`~.__eq__` method of :class:`str`, so:

		.. code-block:: python

			>>> Secret("Barry as FLUFL") == "Barry as FLUFL"
			True

	.. versionadded:: 0.4.6
	"""

	__slots__ = ("value", )

	value: str  #: The actual value of the secret.

	def __new__(cls, value) -> "Secret":  # noqa D102
		obj: Secret = super().__new__(cls, "<SECRET>")
		obj.value = str(value)
		return obj

	def __eq__(self, other) -> bool:
		return self.value == other

	def __hash__(self):
		return hash(self.value)
