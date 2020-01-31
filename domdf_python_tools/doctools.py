#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  doctools.py
"""
Utilities for documenting functions, classes and methods
"""
#
#  Based on https://softwareengineering.stackexchange.com/a/386758
#  Copyright (c) amon (https://softwareengineering.stackexchange.com/users/60357/amon)
#  Licensed under CC BY-SA 4.0
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


def is_documented_by(original):
	def wrapper(target):
		target.__doc__ = original.__doc__
		return target
	return wrapper


def append_docstring_from(original):
	def wrapper(target):
		target.__doc__ = target.__doc__ + "\n" + original.__doc__
		return target
	return wrapper
