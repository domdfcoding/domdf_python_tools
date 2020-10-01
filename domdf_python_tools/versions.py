#!/usr/bin/env python
#
#  versions.py
"""
NamedTuple-like class to represent a version number.
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

# stdlib
import re
from typing import Generator, Sequence, Tuple, Union

__all__ = ["Version"]


class Version(Tuple[int, int, int]):
	"""
	NamedTuple-like class to represent a version number.

	:param major: The major version number.
	:type major: :class:`int`
	:param minor: The minor version number.
	:type minor: :class:`int`
	:param patch: The patch version number.
	:type patch: :class:`int`

	.. versionadded:: 0.4.4
	"""

	major: int
	"The major version number."

	minor: int
	"The minor version number."

	patch: int
	"The patch number."

	def __new__(cls, major=0, minor=0, patch=0) -> "Version":
		t: "Version" = super().__new__(cls, (int(major), int(minor), int(patch)))  # type: ignore

		t.__dict__["major"] = int(major)
		t.__dict__["minor"] = int(minor)
		t.__dict__["patch"] = int(patch)

		return t

	def __repr__(self) -> str:
		"""
		Return the representation of the version.
		"""

		field_names = self.__annotations__.keys()
		repr_fmt = '(' + ", ".join(f"{name}=%r" for name in field_names) + ')'
		return self.__class__.__name__ + repr_fmt % self

	def __str__(self) -> str:
		"""
		Return version as a string.
		"""

		return "v" + ".".join(str(x) for x in self)  # pylint: disable=not-an-iterable

	def __float__(self) -> float:
		"""
		Return the major and minor version number as a float.
		"""

		return float(".".join(str(x) for x in self[:2]))

	def __int__(self) -> int:
		"""
		Return the major version number as an integer.
		"""

		return self.major

	def __getnewargs__(self):
		"""
		Return Version as a plain tuple. Used by copy and pickle.
		"""

		return tuple(self)

	def __eq__(self, other) -> bool:
		"""
		Returns whether this version is equal to the other version.

		:type other: str, float, Version
		"""

		other = _prep_for_eq(other)

		if other is NotImplemented:
			return NotImplemented  # pragma: no cover
		else:
			shortest = min(len(self), (len(other)))
			return self[:shortest] == other[:shortest]

	def __gt__(self, other) -> bool:
		"""
		Returns whether this version is greater than the other version.

		:type other: str, float, Version
		"""

		other = _prep_for_eq(other)

		if other is NotImplemented:
			return NotImplemented  # pragma: no cover
		else:
			return tuple(self) > other

	def __lt__(self, other) -> bool:
		"""
		Returns whether this version is less than the other version.

		:type other: str, float, Version
		"""

		other = _prep_for_eq(other)

		if other is NotImplemented:
			return NotImplemented  # pragma: no cover
		else:
			return tuple(self) < other

	def __ge__(self, other) -> bool:
		"""
		Returns whether this version is greater than or equal to the other version.

		:type other: str, float, Version
		"""

		other = _prep_for_eq(other)

		if other is NotImplemented:
			return NotImplemented  # pragma: no cover
		else:
			return tuple(self)[:len(other)] >= other

	def __le__(self, other) -> bool:
		"""
		Returns whether this version is less than or equal to the other version.

		:type other: str, float, Version
		"""

		other = _prep_for_eq(other)

		if other is NotImplemented:
			return NotImplemented  # pragma: no cover
		else:
			return tuple(self)[:len(other)] <= other

	@classmethod
	def from_str(cls, version_string: str) -> "Version":
		"""
		Create a :class:`~.Version` from a :class:`str`.

		:param version_string: The version number.

		:return: The created :class:`~domdf_python_tools.versions.Version`.
		"""

		return cls(*_iter_string(version_string))

	@classmethod
	def from_tuple(cls, version_tuple: Tuple[Union[str, int], ...]) -> "Version":
		"""
		Create a :class:`~.Version` from a :class:`tuple`.

		:param version_tuple: The version number.

		:return: The created :class:`~domdf_python_tools.versions.Version`.

		.. versionchanged:: 0.9.0

			Tuples with more than three elements are truncated.
			Previously a :exc:`TypeError` was raised.
		"""

		return cls(*(int(x) for x in version_tuple[:3]))

	@classmethod
	def from_float(cls, version_float: float) -> "Version":
		"""
		Create a :class:`~.Version` from a :class:`float`.

		:param version_float: The version number.

		:return: The created :class:`~domdf_python_tools.versions.Version`.
		"""

		return cls.from_str(str(version_float))


def _iter_string(version_string: str) -> Generator[int, None, None]:
	"""
	Iterate over the version elements from a string.

	:param version_string: The version as a string.

	:return: Iterable elements of the version.
	"""

	return (int(x) for x in re.split("[.,]", version_string))


def _iter_float(version_float: float) -> Generator[int, None, None]:
	"""
	Iterate over the version elements from a float.

	:param version_float: The version as a float.

	:return: Iterable elements of the version.
	"""

	return _iter_string(str(version_float))


def _prep_for_eq(other: Union[str, float, Version], ) -> Tuple[int, ...]:
	"""
	Prepare 'other' for use in ``__eq__``, ``__le__``, ``__ge__``, ``__gt__``, and ``__lt__``.
	"""

	if isinstance(other, str):
		return tuple(_iter_string(other))
	elif isinstance(other, (Version, Sequence)):
		return tuple((int(x) for x in other))
	elif isinstance(other, (int, float)):
		return tuple(_iter_float(other))
	else:  # pragma: no cover
		return NotImplemented
