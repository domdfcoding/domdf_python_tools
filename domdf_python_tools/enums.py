#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  enums.py
"""
Enum subclasses with some extra features
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

# 3rd party
from aenum import Enum, IntEnum  # type: ignore

__all__ = ["IntEnum", "StrEnum"]

# class IntEnum(Enum):
# 	"""
# 	An Enum that can be converted into an integer
# 	"""
#
# 	def __int__(self):
# 		return self.value
#
# 	def __eq__(self, other):
# 		if int(self) == other:
# 			return True
# 		else:
# 			return super().__eq__(other)


class StrEnum(str, Enum):
	"""
	An Enum that can be converted into a string
	"""

	def __str__(self):
		return self.value

	#
	# def __repr__(self):
	# 	return self.value

	# def __eq__(self, other):
	# 	if str(self) == other:
	# 		return True
	# 	else:
	# 		return super().__eq__(other)
