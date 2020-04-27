#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  doctools.py
"""
List of common pagesizes and some tools for working with them
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


from collections import Sequence
import re


"""This module defines a few common page sizes in points (1/72 inch).
To be expanded to include things like label sizes, envelope windows
etc."""
__version__ = '3.3.0'

'''
Defines inch, cm, mm etc as multiples of a point

You can now in user-friendly units by doing::

	from reportlab.lib.units import inch
	r = Rect(0, 0, 3 * inch, 6 * inch)

'''

inch = 72.0
cm = inch / 2.54
mm = cm * 0.1
um = mm * 0.01
pc = pica = 12.0
dd = didot = 1.07
cc = cicero = dd*12
nd = new_didot = 1.067
nc = new_cicero = nd*12
sp = scaled_point = 1/65536


# ISO 216 standard paper sizes; see eg https://en.wikipedia.org/wiki/ISO_216
# also http://www.printernational.org/iso-paper-sizes.php
_4A0 = (1682 * mm, 2378 * mm)
_2A0 = (1189 * mm, 1682 * mm)
A0 = (841 * mm, 1189 * mm)
A1 = (594 * mm, 841 * mm)
A2 = (420 * mm, 594 * mm)
A3 = (297 * mm, 420 * mm)
A4 = (210 * mm, 297 * mm)
A5 = (148 * mm, 210 * mm)
A6 = (105 * mm, 148 * mm)
A7 = (74 * mm, 105 * mm)
A8 = (52 * mm, 74 * mm)
A9 = (37 * mm, 52 * mm)
A10 = (26 * mm, 37 * mm)

# _W, _H = (21 * cm, 29.7 * cm)
# A6 = (_W * .5, _H * .5)
# A5 = (_H * .5, _W)
# A4 = (_W, _H)
# A3 = (_H, _W * 2)
# A2 = (_W * 2, _H * 2)
# A1 = (_H * 2, _W * 4)
# A0 = (_W * 4, _H * 4)

B0 = (1000 * mm, 1414 * mm)
B1 = (707 * mm, 1000 * mm)
B2 = (500 * mm, 707 * mm)
B3 = (353 * mm, 500 * mm)
B4 = (250 * mm, 353 * mm)
B5 = (176 * mm, 250 * mm)
B6 = (125 * mm, 176 * mm)
B7 = (88 * mm, 125 * mm)
B8 = (62 * mm, 88 * mm)
B9 = (44 * mm, 62 * mm)
B10 = (31 * mm, 44 * mm)

# _BW, _BH = (25 * cm, 35.3 * cm)
# B6 = (_BW * .5, _BH * .5)
# B5 = (_BH * .5, _BW)
# B4 = (_BW, _BH)
# B3 = (_BH * 2, _BW)
# B2 = (_BW * 2, _BH * 2)
# B1 = (_BH * 4, _BW * 2)
# B0 = (_BW * 4, _BH * 4)

C0 = (917 * mm, 1297 * mm)
C1 = (648 * mm, 917 * mm)
C2 = (458 * mm, 648 * mm)
C3 = (324 * mm, 458 * mm)
C4 = (229 * mm, 324 * mm)
C5 = (162 * mm, 229 * mm)
C6 = (114 * mm, 162 * mm)
C7 = (81 * mm, 114 * mm)
C8 = (57 * mm, 81 * mm)
C9 = (40 * mm, 57 * mm)
C10 = (28 * mm, 40 * mm)

A2EXTRA = (445 * mm, 619 * mm)
A3EXTRA = (322 * mm, 445 * mm)
A3SUPER = (305 * mm, 508 * mm)
SUPERA3 = (305 * mm, 487 * mm)
A4EXTRA = (235 * mm, 322 * mm)
A4SUPER = (229 * mm, 322 * mm)
SUPERA4 = (227 * mm, 356 * mm)
A4LONG = (210 * mm, 348 * mm)
A5EXTRA = (173 * mm, 235 * mm)
SOB5EXTRA = (202 * mm, 276 * mm)

# American paper sizes
LETTER = (8.5 * inch, 11 * inch)
LEGAL = (8.5 * inch, 14 * inch)
TABLOID = ELEVENSEVENTEEN = (11 * inch, 17 * inch)

# From https://en.wikipedia.org/wiki/Paper_size
JUNIOR_LEGAL = (5 * inch, 8 * inch)
HALF_LETTER = (5.5 * inch, 8 * inch)
GOV_LETTER = (8 * inch, 10.5 * inch)
GOV_LEGAL = (8.5 * inch, 13 * inch)
LEDGER = (17 * inch, 11 * inch)
EMPEROR = (48*inch, 72*inch)
QUAD_ROYAL = (40*inch, 50*inch)
QUAD_DEMY = (35*inch, 40*inch)
ANTIQUARIAN = (31*inch, 53*inch)
GRAND_EAGLE = (28.75*inch, 42*inch)
DOUBLE_ELEPHANT = (26.75*inch, 40*inch)
ATLAS = (26*inch, 34*inch)
DOUBLE_ROYAL = (25*inch, 40*inch)
COLOMBIER = (23.5*inch, 34.5*inch)
DOUBLE_DEMY_US = (22.5*inch, 35.5*inch)
DOUBLE_DEMY = DOUBLE_DEMY_UK = (22.5*inch, 35*inch)
IMPERIAL = (22*inch, 30*inch)
DOUBLE_LARGE_POST = (21*inch, 33*inch)
ELEPHANT = (23*inch, 28*inch)
PRINCESS = (22.5*inch, 28*inch)
CARTRIDGE = (21*inch, 26*inch)
ROYAL = (20*inch, 25*inch)
SHEET = HALF_POST = (19.5*inch, 23.5*inch)
DOUBLE_POST = (19*inch, 30.5*inch)
SUPER_ROYAL = (19*inch, 27*inch)
BROADSHEET = (18*inch, 24*inch)
MEDIUM_US = (17.5*inch, 23*inch)
MEDIUM_UK = (18*inch, 23*inch)
DEMY = (17.5*inch, 22.5*inch)
COPY_DRAUGHT = (16*inch, 20*inch)
LARGE_POST_US = (15.5*inch, 20*inch)
LARGE_POST_UK = (16.5*inch, 21*inch)
POST_US = (15.5*inch, 19.35*inch)
POST_UK = (15.5*inch, 19.5*inch)
CROWN = (15*inch, 20*inch)
PINCHED_POST = (14.75*inch, 18.5*inch)
FOOLSCAP_US = (13.5*inch, 17*inch)
FOOLSCAP_UK = (13*inch, 18*inch)
SMALL_FOOLSCAP = (13.35*inch, 16.5*inch)
BRIEF = (13.5*inch, 16*inch)
POTT = (12.5*inch, 15*inch)
QUARTO_US = (9*inch, 11*inch)
EXECUTIVE = MONARCH = (7.35*inch, 10.5*inch)
FOLIO = FOOLSCAP_FOLIO = (8*inch, 13*inch)
QUARTO = QUARTO_UK = (8*inch, 10*inch)
# IMPERIAL = (7*inch, 9*inch)  there are two of these?
KINGS = (6.5*inch, 8*inch)
DUKES = (5.5*inch, 7*inch)

# https://en.wikipedia.org/wiki/ISO/IEC_7810
ID_1 = (85.60*mm, 53.98*mm)  # Most banking cards and ID cards
ID_2 = (105*mm, 74*mm)  # French and other ID cards; Visas
ID_3 = (125*mm, 88*mm)  # US government ID cards
ID_000 = (25*mm, 15*mm)  # SIM cards


# functions to mess with pagesizes
def landscape(pagesize):
	"""
	Returns the given pagesize in landscape orientation
	
	:param pagesize:
	:type pagesize:
	
	:return:
	:rtype:
	"""
	
	a, b = pagesize
	if a < b:
		return b, a
	else:
		return a, b


def portrait(pagesize):
	"""
	Returns the given pagesize in portrait orientation
	
	:param pagesize:
	:type pagesize:
	
	:return:
	:rtype:
	"""
	
	a, b = pagesize
	if a >= b:
		return b, a
	else:
		return a, b


def _w_h_from_size(size=None, width=None, height=None):
	if size:
		width, height = size
	else:
		if not width or not height:
			raise ValueError("Either `size` or `width` AND `height` must be provided.")
	
	return width, height

def is_portrait(size=None, *, width=None, height=None):
	width, height = _w_h_from_size(size, width, height)
	return width <= height
	
	
def is_landscape(size=None, *, width=None, height=None):
	width, height = _w_h_from_size(size, width, height)
	return width >= height
	
	
def is_square(size=None, *, width=None, height=None):
	width, height = _w_h_from_size(size, width, height)
	return width == height
	

def to_mm(val):
	"""
	Convert from pt to mm
	
	:type val: float
	:rtype: float
	"""
	
	return _convert(val, mm)


def to_cm(val):
	"""
	Convert from pt to cm
	
	:type val: float
	:rtype: float
	"""
	
	return _convert(val, cm)


def to_inch(val):
	"""
	Convert from pt to inch
	
	:type val: float
	:rtype: float
	"""
	
	return _convert(val, inch)


def to_pica(val):
	"""
	Convert from pt to pica
	
	:type val: float
	:rtype: float
	"""
	
	return _convert(val, pica)


def _convert(val, to):
	if isinstance(val, Sequence):
		return _sequence_convert(val, to)
	else:
		return val / to


def _sequence_convert(seq, to):
	return type(seq)([x / to for x in seq])


def parse_measurement(measurement):
	match = re.findall(r"\d*\.?\d+", measurement)
	if len(match) < 2:
		raise ValueError("Unable to parse measurement")
	else:
		val, unit, *_ = match
		if unit == "mm":
			return val*mm
		elif unit == "cm":
			return val*cm
		# TODO: um
		elif unit == "pt":
			return val
		elif unit == "inch":
			return val*inch
		elif unit == "pc":
			return val*pc
		elif unit == "dd":
			return val*dd
		elif unit == "cc":
			return val*cc
		elif unit == "nd":
			return val*nd
		elif unit == "nc":
			return val*nc
		elif unit == "sp":
			return val*sp
		raise ValueError("Unknown unit")


def toLength(s):
	"""
	Convert a string to a length

	:param s:
	:type s:
	:return:
	:rtype:
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
		raise ValueError(f"Can't convert '{s}' to length")
