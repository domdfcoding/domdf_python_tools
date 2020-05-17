#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utils.py
"""
General Functions
"""
#
#  Copyright © 2018-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#

import sys
from collections.abc import Sequence
from domdf_python_tools.doctools import is_documented_by

pyversion = int(sys.version[0])  # Python Version


def as_text(value):
	"""
	Convert the given value to a string

	:param value: value to convert to a string
	:type value: any

	:rtype: str
	"""

	if value is None:
		return ""

	return str(value)


def str2tuple(input_string, sep=","):
	"""
	Convert a comma-separated string of integers into a tuple

	:param input_string: The string to be converted into a tuple
	:type input_string: str
	:param sep: The separator in the string, default ","
	:type sep: str

	:rtype: tuple
	"""

	return tuple(int(x) for x in input_string.split(sep))


def tuple2str(input_tuple, sep=","):
	"""
	Convert a tuple into a comma-separated string

	:param input_tuple: The tuple to be joined into a string
	:type input_tuple: tuple
	:param sep: The separator in the string, default ","
	:type sep: str

	:rtype: str
	"""

	return sep.join([str(x) for x in input_tuple])


def chunks(l, n):
	"""
	Yield successive n-sized chunks from l.

	:param l: The objects to yield chunks from
	:type l: Sequence
	:param n: The size of the chunks
	:type n: int
	"""

	for i in range(0, len(l), n):
		yield l[i:i + n]


def check_dependencies(dependencies, prt=True):
	"""

	:param dependencies:
	:param prt:

	:return:
	"""

	from pkgutil import iter_modules

	modules = set(x[1] for x in iter_modules())

	missing_modules = []
	for requirement in dependencies:
		if requirement not in modules:
			missing_modules.append(requirement)

	if prt:
		if len(missing_modules) == 0:
			print("All modules installed")
		else:
			print("The following modules are missing.")
			print(missing_modules)
			print("Please check the documentation.")
		print("")

	else:
		return missing_modules


def list2str(the_list, sep=","):
	"""
	Convert a list to a comma separated string

	:param the_list: The list to convert to a string
	:type the_list: list, tuple
	:param sep: Separator to use for the string, default ","
	:type sep: str

	:return: Comma separated string
	:rtype: str
	"""

	return sep.join([str(x) for x in the_list])


list2string = list2str


def split_len(string, n):
	"""
	Split a string every x characters

	:param string: The string to split
	:type string: str
	:param n:
	:type n: int

	:return: The split string
	:rtype: list
	"""

	return [string[i:i + n] for i in range(0, len(string), n)]


splitLen = split_len


def permutations(data, n=2):
	"""
	Return permutations containing `n` items from `data` without any reverse duplicates.
	If ``n`` is equal to or greater than the length of the data an empty list of returned

	:type data: list or string
	:type n: int

	:rtype: [tuple]
	"""

	import itertools

	if n == 0:
		raise ValueError("`n` cannot be 0")

	perms = []
	for i in itertools.permutations(data, n):
		if i[::-1] not in perms:
			perms.append(i)
	return perms


def cmp(x, y):
	"""
	Implementation of cmp for Python 3

	Compare the two objects x and y and return an integer according to the outcome.
	The return value is negative if x < y, zero if x == y and strictly positive if x > y.

	:rtype: int
	"""

	return int((x > y) - (x < y))


def printr(item, *args, **kwargs):
	"""
	Print the repr() of an object
	"""

	return print(repr(item), *args, **kwargs)


def printt(item, *args, **kwargs):
	"""
	Print the type of an object
	"""

	return print(type(item), *args, **kwargs)
