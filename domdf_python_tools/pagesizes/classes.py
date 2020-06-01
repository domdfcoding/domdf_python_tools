#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  classes.py
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on reportlab.lib.pagesizes and reportlab.lib.units
#    www.reportlab.co.uk
#    Copyright ReportLab Europe Ltd. 2000-2017
#    Copyright (c) 2000-2018, ReportLab Inc.
#    All rights reserved.
#    Licensed under the BSD License
#
#  Includes data from en.wikipedia.org.
#  Licensed under the Creative Commons Attribution-ShareAlike License
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
from collections import namedtuple
from collections.abc import Sequence
from typing import List, Tuple

from ._types import AnyNumber
from .units import cicero, cm, didot, inch, mm, new_cicero, new_didot, pica, pt, scaled_point, um
from .utils import _rounders, convert_from

__all__ = [
		"BaseSize",
		"Size_mm",
		"Size_inch",
		"Size_cm",
		"Size_um",
		"Size_pica",
		"Size_didot",
		"Size_cicero",
		"Size_new_didot",
		"Size_new_cicero",
		"Size_scaled_point",
		"PageSize",
		]


class BaseSize(namedtuple("__BaseSize", "width, height")):
	__slots__: List[str] = []
	_unit: float = pt

	def __new__(cls, width: AnyNumber, height: AnyNumber):
		return super().__new__(cls, float(width), float(height))

	def __str__(self):
		return f"{self.__class__.__name__}(width={_rounders(self.width, '0')}, height={_rounders(self.height, '0')})"

	@classmethod
	def from_size(cls, size: Tuple[AnyNumber, AnyNumber]):
		"""

		:param size:
		:type size: Sequence

		:return:
		:rtype:
		"""

		return cls(*size)

	def landscape(self) -> "BaseSize":
		"""
		Returns the pagesize in landscape orientation

		:return: The pagesize in the landscape orientation
		:rtype: BaseSize
		"""

		if self.is_portrait():
			return self.__class__(self.height, self.width)
		else:
			return self

	def is_landscape(self) -> bool:
		"""
		Returns whether the pagesize is in the landscape orientation

		:return:
		:rtype: bool
		"""

		return self.width >= self.height

	def portrait(self) -> "BaseSize":
		"""
		Returns the pagesize in portrait orientation

		:return: The pagesize in the portrait orientation
		:rtype: BaseSize
		"""

		if self.is_landscape():
			return self.__class__(self.height, self.width)
		else:
			return self

	def is_portrait(self) -> bool:
		"""
		Returns whether the pagesize is in the portrait orientation

		:return:
		:rtype: bool
		"""

		return self.width < self.height

	def is_square(self) -> bool:
		"""
		Returns whether the given pagesize is square

		:return:
		:rtype:
		"""

		return self.width == self.height

	@classmethod
	def from_pt(cls, size: "PageSize"):
		"""

		:param size:
		:type size: PageSize

		:return:
		:rtype:
		"""

		assert isinstance(size, PageSize)

		return cls(size.width / cls._unit, size.height / cls._unit)

	def to_pt(self) -> "PageSize":
		"""

		:return:
		:rtype: PageSize
		"""

		return PageSize(self.width * self._unit, self.height * self._unit)


# TODO: conversion to Point for the __eq__ function in the below


class Size_mm(BaseSize):
	_unit = mm


class Size_inch(BaseSize):
	_unit = inch


class Size_cm(BaseSize):
	_unit = cm


class Size_um(BaseSize):
	_unit = um


class Size_pica(BaseSize):
	_unit = pica


class Size_didot(BaseSize):
	_unit = didot


class Size_cicero(BaseSize):
	_unit = cicero


class Size_new_didot(BaseSize):
	_unit = new_didot


class Size_new_cicero(BaseSize):
	_unit = new_cicero


class Size_scaled_point(BaseSize):
	_unit = scaled_point


class PageSize(BaseSize):
	__slots__: List[str] = []

	def __new__(cls, width, height, unit=pt):
		width, height = convert_from((width, height), unit)
		return super().__new__(cls, width, height)

	@property
	def inch(self):
		return Size_inch.from_pt(self)

	@property
	def cm(self):
		return Size_cm.from_pt(self)

	@property
	def mm(self):
		return Size_mm.from_pt(self)

	@property
	def um(self):
		return Size_um.from_pt(self)

	@property
	def pc(self):
		return Size_pica.from_pt(self)

	pica = pc

	@property
	def dd(self):
		return Size_didot.from_pt(self)

	didot = dd

	@property
	def cc(self):
		return Size_cicero.from_pt(self)

	cicero = cc

	@property
	def nd(self):
		return Size_new_didot.from_pt(self)

	new_didot = nd

	@property
	def nc(self):
		return Size_new_cicero.from_pt(self)

	new_cicero = nc

	@property
	def sp(self):
		return Size_scaled_point.from_pt(self)

	scaled_point = sp
