#  !/usr/bin/env python
#
#  bases.py
"""
Useful base classes.
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
from abc import abstractmethod
from collections import UserList
from pprint import pformat
from typing import Any, Dict, Iterable, Tuple, Type

# 3rd party
import pydash  # type: ignore

__all__ = ["Dictable", "NamedList", "namedlist"]


class Dictable(Iterable):
	"""
	The basic structure of a class that can be converted into a dictionary.
	"""

	@abstractmethod
	def __init__(self, *args, **kwargs):
		pass

	def __str__(self) -> str:
		return self.__repr__()

	def __iter__(self) -> Iterable[Tuple[str, Any]]:  # type: ignore[override]
		yield from self.__dict__.items()

	def __getstate__(self) -> Dict[str, Any]:
		return self.__dict__

	def __setstate__(self, state):
		self.__init__(**state)  # type: ignore

	def __copy__(self):
		return self.__class__(**self.__dict__)

	def __deepcopy__(self, memodict={}):
		return self.__copy__()

	@property
	@abstractmethod
	def __dict__(self):
		return dict()  # pragma: no cover (abc)

	def __eq__(self, other) -> bool:
		if isinstance(other, self.__class__):
			return pydash.predicates.is_match(other.__dict__, self.__dict__)

		return NotImplemented


class NamedList(UserList):
	"""
	A list with a name.

	The name of the list is taken from the name of the subclass.
	"""

	def __repr__(self) -> str:
		return f"{super().__repr__()}"

	def __str__(self) -> str:
		return f"{self.__class__.__name__}{pformat(list(self))}"


def namedlist(name: str = "NamedList") -> Type[NamedList]:
	"""
	A factory function to return a custom list subclass with a name.

	:param name: The name of the list.
	"""

	class cls(NamedList):
		pass

	cls.__name__ = name

	return cls
