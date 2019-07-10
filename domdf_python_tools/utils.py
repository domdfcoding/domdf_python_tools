#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utils.py
"""General Functions"""
#
#  Copyright 2018-2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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


def as_text(value):
	"""
	Convert the given value to a string
	
	:param value: value to convert to a string
	
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

	:param l:
	:param n:
	:return:
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
		if not requirement in modules:
			missing_modules.append(requirement)
	
	if prt:
		if len(missing_modules) == 0:
			print("All modules installed")
		else:
			print("""\rThe following modules are missing.
	Please check the documentation.""")
			print(missing_modules)
		print("")
	
	else:
		return missing_modules


def list2string(the_list, sep=","):
	"""
	Convert a list to a comma separated string

	:param the_list: The list to convert to a string
	:type the_list: list
	:param sep: Separator to use for the string, default ","
	:type sep: str

	:return: Comma separated string
	:rtype: str
	"""
	
	return list2str(the_list, sep)


def list2str(the_list, sep=","):
	"""
	Convert a list to a comma separated string
	
	:param the_list: The list to convert to a string
	:type the_list: list
	:param sep: Separator to use for the string, default ","
	:type sep: str
	
	:return: Comma separated string
	:rtype: str
	"""
	
	return sep.join([str(x) for x in the_list])


def splitLen(string,n):
	"""
	Split a string every x characters
	
	:param string:
	:param n:
	
	:return:
	"""
	
	return [string[i:i+n] for i in range(0,len(string),n)]

