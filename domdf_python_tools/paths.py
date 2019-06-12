#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  paths.py
"""Functions for paths and files"""
#
#  Copyright 2018-2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  copytree based on https://stackoverflow.com/a/12514470/3092681
#		Copyright 2012 atzz
#		Licensed under CC-BY-SA
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

def parent_path(path):
	return os.path.abspath(os.path.join(path,os.pardir))

def copytree(src, dst, symlinks=False, ignore=None):
	"""
	
	Because shutil.copytree is borked
	
	:param src:
	:param dst:
	:param symlinks:
	:param ignore:
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

def relpath(path):
	"""
	
	:param path:
	:return:
	"""
	
	if os.path.normpath(os.path.abspath(path)).startswith(os.path.normpath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))):
		return os.path.relpath(os.path.abspath(path))
	else:
		return os.path.abspath(path)

def maybe_make(directory):
	"""
	makes a directory only if it doesn't already exist
	
	:param directory:
	:return:
	"""
	
	if not os.path.exists(directory):
		os.makedirs(directory)