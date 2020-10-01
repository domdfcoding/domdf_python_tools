#  !/usr/bin/env python
#
#  utils.py
"""
Tools for working with pagesizes.
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
from typing import Sequence, Tuple, Union, overload

# this package
from domdf_python_tools.typing import AnyNumber

# this package
from .units import Unit, cm, inch, mm, pc, pt, um

# from .units import Unit

__all__ = ["convert_from", "parse_measurement"]


@overload
def convert_from(value: Sequence[AnyNumber], from_: AnyNumber) -> Tuple[float, ...]:
	...  # pragma: no cover


@overload
def convert_from(value: AnyNumber, from_: AnyNumber) -> float:
	...  # pragma: no cover


def convert_from(
		value: Union[Sequence[AnyNumber], AnyNumber],
		from_: AnyNumber,
		) -> Union[float, Tuple[float, ...]]:
	r"""
	Convert ``value`` to point from the unit specified in ``from_``.

	:param value:
	:param from\_: The unit to convert from, specified as a number of points.
	"""

	if isinstance(value, Sequence):
		return _sequence_convert_from(value, from_)
	else:
		return _sequence_convert_from((value, ), from_)[0]


def _sequence_convert_from(seq: Sequence[AnyNumber], from_: AnyNumber) -> Tuple[float, ...]:
	if isinstance(from_, Unit):
		from_ = from_._in_pt
	else:
		from_ = float(from_)

	return tuple(float(x) * from_ for x in seq)


_measurement_re = re.compile(r"(\d*\.?\d+) *([A-Za-zμµ\"']*)")


def parse_measurement(measurement: str) -> Union[float, Tuple[float, ...]]:
	"""
	Parse the given measurement.

	:param measurement:
	"""

	# TODO: docstring
	all_matches = _measurement_re.findall(measurement)

	if len(all_matches) > 1:
		raise ValueError("Too many measurements")
	elif len(all_matches) == 0:
		raise ValueError("Unable to parse measurement")

	val, unit = all_matches[0]

	if '' in {val, unit}:
		raise ValueError("Unable to parse measurement")

	val = float(val)

	if unit == "mm":
		return val * mm
	elif unit == "cm":
		return val * cm
	elif unit in {"um", "μm", "µm"}:  # second is mu, third is micro
		return val * um
	elif unit == "pt":
		return val * pt
	elif unit in {"inch", "in", '"'}:
		return val * inch
	elif unit in ("pc", "pica"):
		return val * pc

	raise ValueError("Unknown unit")
