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
	:type the_list: list, tuple
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
	:type the_list: list, tuple
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


def permutations(data, n=2):
	"""
	Return permutations containing `n` items from `data` without any reverse duplicates
	
	:type data: list or string
	:type n: int
	
	:rtype: list of tuples
	"""
	
	import itertools
	perms = []
	for i in itertools.permutations(data, n):
		"""from https://stackoverflow.com/questions/10201977/how-to-reverse-tuples-in-python"""
		if i[::-1] not in perms:
			perms.append(i)
	return perms


class bdict(dict):
	"""
	Returns a new dictionary initialized from an optional positional argument
		and a possibly empty set of keyword arguments.
	
	Each key:value pair is entered into the dictionary in both directions,
		so you can perform lookups with either the key or the value.
	
	If no positional argument is given, an empty dictionary is created.
	If a positional argument is given and it is a mapping object, a dictionary
		is created with the same key-value pairs as the mapping object.
	Otherwise, the positional argument must be an iterable object.
		Each item in the iterable must itself be an iterable with exactly two
		objects. The first object of each item becomes a key in the new
		dictionary, and the second object the corresponding value.
	
	If keyword arguments are given, the keyword arguments and their values are
	added to the dictionary created from the positional argument.
	
	If an attempt is made to add a key or value that already exists in the
		dictionary a ValueError will be raised
	
	Keys or values of "None", "True" and "False" will be stored internally as
		"_None" "_True" and "_False" respectively
	
	Based on https://stackoverflow.com/a/1063393 by https://stackoverflow.com/users/9493/brian
	"""
	
	def __init__(self, *args, **kwargs):
		super().__init__(self)
		if len(args) == 1:
			for key, value in dict(*args).items():
				self.__setitem__(key, value)
		if len(args) == 0:
			for key, value in kwargs.items():
				self.__setitem__(key, value)

	def __setitem__(self, key, val):
		if key in self or val in self:
			if key in self and self[key] != val:
				raise ValueError(f"The key '{key}' is already present in the dictionary")
			if val in self and self[val] != key:
				raise ValueError(f"The key '{val}' is already present in the dictionary")
		
		if key is None:
			key = "_None"
		if val is None:
			val = "_None"
		
		if isinstance(key, bool):
			if key:
				key = "_True"
			else:
				key = "_False"
		
		if isinstance(val, bool):
			if val:
				val = "_True"
			else:
				val = "_False"
		
		dict.__setitem__(self, key, val)
		dict.__setitem__(self, val, key)
	
	def __delitem__(self, key):
		dict.__delitem__(self, self[key])
		dict.__delitem__(self, key)
	
	def __getitem__(self, key):
		if key is None:
			key = "_None"
		
		if isinstance(key, bool):
			if key:
				key = "_True"
			else:
				key = "_False"
		
		val = dict.__getitem__(self, key)

		if val == "_None":
			return None
		elif val == "_True":
			return True
		elif val == "_False":
			return False
		else:
			return val
	
	def __contains__(self, key):
		print("Contains")
		if key is None:
			key = "_None"
		
		if isinstance(key, bool):
			if key:
				key = "_True"
			else:
				key = "_False"
		
		return dict.__contains__(self, key)
