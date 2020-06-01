#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  bases.py
"""
Useful base classes
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
from abc import ABC, abstractmethod
from collections import UserList
from pprint import pformat

# 3rd party
import pydash  # type: ignore


class Dictable(ABC):
	"""
	The basic structure of a class that can be converted into a dictionary
	"""

	@abstractmethod
	def __init__(self, *args, **kwargs):
		pass

	def __str__(self):
		return self.__repr__()

	def __iter__(self):
		for key, value in self.__dict__.items():
			yield key, value

	def __getstate__(self):
		return self.__dict__

	def __setstate__(self, state):
		self.__init__(**state)

	def __copy__(self):
		return self.__class__(**self.__dict__)

	def __deepcopy__(self, memodict={}):
		return self.__copy__()

	@property
	@abstractmethod
	def __dict__(self):
		return dict()

	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return pydash.predicates.is_match(other.__dict__, self.__dict__)

		return NotImplemented


def namedlist(name="NamedList"):
	"""
	A factory function to return a custom list subclass with a name

	:param name:
	:type name:
	:return:
	:rtype:
	"""

	class NamedList(UserList):
		"""
		A list with a name
		"""

		def __repr__(self):
			return f"{super().__repr__()}"

		def __str__(self):
			return f"{self.__class__.__name__}{pformat(list(self))}"

	NamedList.__name__ = name

	return NamedList
