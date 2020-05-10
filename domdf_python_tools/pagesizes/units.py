#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  units.py
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


from decimal import Decimal

__all__ = [
		"pt", "inch", "cm", "mm", "um", "pc", "pica",
		"dd", "didot", "cc", "cicero", "nd", "new_didot",
		"nc", "new_cicero", "sp", "scaled_point",
		]


class Unit(Decimal):

	def __mul__(self, other):
		if isinstance(other, float):
			other = Decimal(str(other))

		return self.__class__(super().__mul__(other))

	__rmul__ = __mul__


# Units
pt = 1
inch = Unit("72.0")
cm = inch / Unit("2.54")
mm = cm * Unit("0.1")
um = mm * Unit("0.01")
pc = pica = Unit("12.0")
dd = didot = Unit("1.07")
cc = cicero = dd * 12
nd = new_didot = Unit("1.067")
nc = new_cicero = nd * 12
sp = scaled_point = 1 / 65536
