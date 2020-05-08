#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  sizes.py
"""
List of common pagesizes in point/pt
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


from .classes import Size_inch, Size_mm


# ISO 216 standard paper sizes; see eg https://en.wikipedia.org/wiki/ISO_216
# also http://www.printernational.org/iso-paper-sizes.php
_4A0 = Size_mm(1682, 2378).to_pt()
_2A0 = Size_mm(1189, 1682).to_pt()
A0 = Size_mm(841, 1189).to_pt()
A1 = Size_mm(594, 841).to_pt()
A2 = Size_mm(420, 594).to_pt()
A3 = Size_mm(297, 420).to_pt()
A4 = Size_mm(210, 297).to_pt()
A5 = Size_mm(148, 210).to_pt()
A6 = Size_mm(105, 148).to_pt()
A7 = Size_mm(74, 105).to_pt()
A8 = Size_mm(52, 74).to_pt()
A9 = Size_mm(37, 52).to_pt()
A10 = Size_mm(26, 37).to_pt()

# _W, _H = (21 * cm, 29.7 * cm)
# A6 = (_W * .5, _H * .5)
# A5 = (_H * .5, _W)
# A4 = (_W, _H)
# A3 = (_H, _W * 2)
# A2 = (_W * 2, _H * 2)
# A1 = (_H * 2, _W * 4)
# A0 = (_W * 4, _H * 4)

B0 = Size_mm(1000, 1414)
B1 = Size_mm(707, 1000)
B2 = Size_mm(500, 707)
B3 = Size_mm(353, 500)
B4 = Size_mm(250, 353)
B5 = Size_mm(176, 250)
B6 = Size_mm(125, 176)
B7 = Size_mm(88, 125)
B8 = Size_mm(62, 88)
B9 = Size_mm(44, 62)
B10 = Size_mm(31, 44)

# _BW, _BH = (25 * cm, 35.3 * cm)
# B6 = (_BW * .5, _BH * .5)
# B5 = (_BH * .5, _BW)
# B4 = (_BW, _BH)
# B3 = (_BH * 2, _BW)
# B2 = (_BW * 2, _BH * 2)
# B1 = (_BH * 4, _BW * 2)
# B0 = (_BW * 4, _BH * 4)

C0 = Size_mm(917, 1297)
C1 = Size_mm(648, 917)
C2 = Size_mm(458, 648)
C3 = Size_mm(324, 458)
C4 = Size_mm(229, 324)
C5 = Size_mm(162, 229)
C6 = Size_mm(114, 162)
C7 = Size_mm(81, 114)
C8 = Size_mm(57, 81)
C9 = Size_mm(40, 57)
C10 = Size_mm(28, 40)

A2EXTRA = Size_mm(445, 619)
A3EXTRA = Size_mm(322, 445)
A3SUPER = Size_mm(305, 508)
SUPERA3 = Size_mm(305, 487)
A4EXTRA = Size_mm(235, 322)
A4SUPER = Size_mm(229, 322)
SUPERA4 = Size_mm(227, 356)
A4LONG = Size_mm(210, 348)
A5EXTRA = Size_mm(173, 235)
SOB5EXTRA = Size_mm(202, 276)

# American paper sizes
LETTER = Size_inch(8.5, 11).to_pt()
LEGAL = Size_inch(8.5, 14).to_pt()
TABLOID = ELEVENSEVENTEEN = Size_inch(11, 17).to_pt()

# From https://en.wikipedia.org/wiki/Paper_size
JUNIOR_LEGAL = Size_inch(5, 8).to_pt()
HALF_LETTER = Size_inch(5.5, 8).to_pt()
GOV_LETTER = Size_inch(8, 10.5).to_pt()
GOV_LEGAL = Size_inch(8.5, 13).to_pt()
LEDGER = Size_inch(17, 11).to_pt()
EMPEROR = Size_inch(48, 72).to_pt()
QUAD_ROYAL = Size_inch(40, 50).to_pt()
QUAD_DEMY = Size_inch(35, 40).to_pt()
ANTIQUARIAN = Size_inch(31, 53).to_pt()
GRAND_EAGLE = Size_inch(28.75, 42).to_pt()
DOUBLE_ELEPHANT = Size_inch(26.75, 40).to_pt()
ATLAS = Size_inch(26, 34).to_pt()
DOUBLE_ROYAL = Size_inch(25, 40).to_pt()
COLOMBIER = Size_inch(23.5, 34.5).to_pt()
DOUBLE_DEMY_US = Size_inch(22.5, 35.5).to_pt()
DOUBLE_DEMY = DOUBLE_DEMY_UK = Size_inch(22.5, 35).to_pt()
IMPERIAL = Size_inch(22, 30).to_pt()
DOUBLE_LARGE_POST = Size_inch(21, 33).to_pt()
ELEPHANT = Size_inch(23, 28).to_pt()
PRINCESS = Size_inch(22.5, 28).to_pt()
CARTRIDGE = Size_inch(21, 26).to_pt()
ROYAL = Size_inch(20, 25).to_pt()
SHEET = HALF_POST = Size_inch(19.5, 23.5).to_pt()
DOUBLE_POST = Size_inch(19, 30.5).to_pt()
SUPER_ROYAL = Size_inch(19, 27).to_pt()
BROADSHEET = Size_inch(18, 24).to_pt()
MEDIUM_US = Size_inch(17.5, 23).to_pt()
MEDIUM_UK = Size_inch(18, 23).to_pt()
DEMY = Size_inch(17.5, 22.5).to_pt()
COPY_DRAUGHT = Size_inch(16, 20).to_pt()
LARGE_POST_US = Size_inch(15.5, 20).to_pt()
LARGE_POST_UK = Size_inch(16.5, 21).to_pt()
POST_US = Size_inch(15.5, 19.35).to_pt()
POST_UK = Size_inch(15.5, 19.5).to_pt()
CROWN = Size_inch(15, 20).to_pt()
PINCHED_POST = Size_inch(14.75, 18.5).to_pt()
FOOLSCAP_US = Size_inch(13.5, 17).to_pt()
FOOLSCAP_UK = Size_inch(13, 18).to_pt()
SMALL_FOOLSCAP = Size_inch(13.35, 16.5).to_pt()
BRIEF = Size_inch(13.5, 16).to_pt()
POTT = Size_inch(12.5, 15).to_pt()
QUARTO_US = Size_inch(9, 11).to_pt()
EXECUTIVE = MONARCH = Size_inch(7.35, 10.5).to_pt()
FOLIO = FOOLSCAP_FOLIO = Size_inch(8, 13).to_pt()
QUARTO = QUARTO_UK = Size_inch(8, 10).to_pt()
# IMPERIAL = Size_inch(7*inch, 9*inch).to_pt()  there are two of these?
KINGS = Size_inch(6.5, 8).to_pt()
DUKES = Size_inch(5.5, 7).to_pt()

# https://en.wikipedia.org/wiki/ISO/IEC_7810
ID_1 = Size_mm(85.60, 53.98).to_pt()  # Most banking cards and ID cards
ID_2 = Size_mm(105, 74).to_pt()  # French and other ID cards; Visas
ID_3 = Size_mm(125, 88).to_pt()  # US government ID cards
ID_000 = Size_mm(25, 15).to_pt()  # SIM cards