#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  utils.py
"""
Tools for working with pagesizes
"""
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
import re
from decimal import ROUND_HALF_UP, Decimal
from numbers import Number
from typing import List, Sequence, Tuple, Union

from ._types import AnyNumber
from .units import cc, cm, dd, inch, mm, nc, nd, pc, pica, sp, um

# from .units import Unit

__all__ = ["convert_from", "parse_measurement"]


def _rounders(val_to_round: Union[str, int, float, Decimal], round_format: str) -> Decimal:
	return Decimal(Decimal(val_to_round).quantize(Decimal(str(round_format)), rounding=ROUND_HALF_UP))


def convert_from(value: Union[Sequence[AnyNumber], AnyNumber],
					from_: AnyNumber) -> Union[float, Tuple[float, ...]]:
	"""
	Convert ``value`` to point from the unit specified in ``from_``

	:param value:
	:param from_: The unit to convert from, specified as a number of points

	:return:
	:rtype:
	"""

	if isinstance(value, Sequence):
		return _sequence_convert_from(value, from_)
	else:
		return _sequence_convert_from((value, ), from_)[0]


def _sequence_convert_from(seq: Sequence[AnyNumber], from_: AnyNumber) -> Tuple[float, ...]:
	from_ = float(from_)

	return tuple(float(x) * from_ for x in seq)


def parse_measurement(measurement):
	# TODO: docstring
	match = re.findall(r"(\d*\.?\d+) *([A-Za-z]*)", measurement)[0]
	print(match)
	print(len(match))
	if len(match) < 2:
		raise ValueError("Unable to parse measurement")
	else:
		val = Decimal(str(match[0]))
		unit = match[1]
		if unit == "mm":
			return convert_from(val, mm)
		elif unit == "cm":
			return convert_from(val, cm)
		elif unit in {"um", "μm", "µm"}:
			return convert_from(val, um)
		elif unit == "pt":
			return val
		elif unit == "inch":
			return convert_from(val, inch)
		elif unit == "in":
			return convert_from(val, inch)
		elif unit == "pc":
			return convert_from(val, pc)
		elif unit == "dd":
			return convert_from(val, dd)
		elif unit == "cc":
			return convert_from(val, cc)
		elif unit == "nd":
			return convert_from(val, nd)
		elif unit == "nc":
			return convert_from(val, nc)
		elif unit == "sp":
			return convert_from(val, sp)
		raise ValueError("Unknown unit")


def to_length(s):
	"""
	Convert a string to a length

	:param s:
	:type s:
	:return:
	:rtype:

	# TODO: combine with parse_measurement
	"""

	try:
		if s[-2:] == 'cm':
			return float(s[:-2]) * cm
		if s[-2:] == 'in':
			return float(s[:-2]) * inch
		if s[-2:] == 'pt':
			return float(s[:-2])
		if s[-1:] == 'i':
			return float(s[:-1]) * inch
		if s[-2:] == 'mm':
			return float(s[:-2]) * mm
		if s[-4:] == 'pica':
			return float(s[:-4]) * pica
		return float(s)
	except:
		raise ValueError(f"Can't convert_to '{s}' to length")
