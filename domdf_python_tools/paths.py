#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  paths.py
"""Functions for paths and files"""
#
#  Copyright 2018-2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  check_dependencies based on https://stackoverflow.com/a/29044693/3092681
#  		Copyright 2015 TehTechGuy
#		Licensed under CC-BY-SA
#
#  as_text from https://stackoverflow.com/a/40935194
#		Copyright 2016 User3759685
#		Available under the MIT License
#
#  chunks from https://stackoverflow.com/a/312464/3092681
#		Copytight 2008 Ned Batchelder
#		Licensed under CC-BY-SA
#
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

import os

def copytree(src, dst, symlinks=False, ignore=None):
	"""
	Because shutil.copytree is borked

	Some of this docstring from https://docs.python.org/3/library/shutil.html

	:param src: Source file to copy
	:type src: str
	:param dst: Destination to copy file to
	:type dst: str
	:param symlinks: Whether to represent symbolic links in the source as symbolic links in the destination
		If false or omitted, the contents and metadata of the linked files are copied to the new tree.
		When symlinks is false, if the file pointed by the symlink doesn’t exist, an exception will be added in the list of errors raised in an Error exception at the end of the copy process. You can set the optional ignore_dangling_symlinks flag to true if you want to silence this exception. Notice that this option has no effect on platforms that don’t support os.symlink().
	:type symlinks: bool
	:param ignore: A callable that will receive as its arguments the source directory, and a list of its contents.
		The ignore callable will be called once for each directory that is copied.
		The callable must return a sequence of directory and file names relative to the current directory (i.e. a subset of the items in its second argument); these names will then be ignored in the copy process. ignore_patterns() can be used to create such a callable that ignores names based on glob-style patterns.

	:return:
	"""
	
	import shutil
	
	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			return shutil.copytree(s, d, symlinks, ignore)
		else:
			return shutil.copy2(s, d)

def maybe_make(directory):
	"""
	Makes a directory only if it doesn't already exist

	:param directory: Directory to create
	:type directory: str
	
	"""
	
	if not os.path.exists(directory):
		os.makedirs(directory)

def parent_path(path):
	"""
	Returns the path of the parent directory for the given file or directory
	
	:param path: Path to find the parent for
	:type path: str
	
	:return:
	"""
	
	return os.path.abspath(os.path.join(path,os.pardir))

def relpath(path, relative_to=None):
	"""
	Returns the path for the given file or directory relative to the given directory
	
	:param path: Path to find the relative path for
	:type path: str
	:param relative_to: The directory to find the path relative to. Defaults to the current working directory (i.e. os.getcwd())
	:type relative_to: str
	
	:return:
	"""
	
	if relative_to is None:
		relative_to = os.getcwd()
	
	#if os.path.normpath(os.path.abspath(path)).startswith(os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))):
	if os.path.normpath(os.path.abspath(path)).startswith(os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(relative_to))))):
		return os.path.relpath(os.path.abspath(path))
	else:
		return os.path.abspath(path)



def delete(filename):
	"""
	Delete the file in the current directory
	
	# TODO: make this the file in the given directory, by default the current directory
	
	:param filename:
	
	:return:
	"""
	
	os.remove(os.path.join(os.getcwd(), filename))


def write(var, filename):
	"""
	Write a variable to file in the current directory
	
	# TODO: make this the file in the given directory, by default the current directory
	
	:param var:
	:param filename:
	
	:return:
	"""
	
	with open(os.path.join(os.getcwd(), filename), 'w') as f:
		f.write(var)


def read(filename):
	"""
	Read a file in the current directory; Untested
	
	# TODO: make this the file in the given directory, by default the current directory
	
	:param filename:
	
	:return:
	"""
	
	with open(os.path.join(os.getcwd(), filename)) as f:
		return f.read()


def append(var, filename):
	"""
	Append `var` to the file `filename` in the current directory; Untested
	
	# TODO: make this the file in the given directory, by default the current directory
	
	:param var:
	:param filename:
	
	:return:
	"""
	
	with open(os.path.join(os.getcwd(), filename), 'a') as f:
		f.write(var)

