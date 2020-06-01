#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  paths.py
"""
Functions for paths and files
"""
#
#  Copyright © 2018-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  check_dependencies based on https://stackoverflow.com/a/29044693/3092681
#  		Copyright © 2015 TehTechGuy
# 		Licensed under CC-BY-SA
#
#  as_text from https://stackoverflow.com/a/40935194
# 		Copyright © 2016 User3759685
# 		Available under the MIT License
#
#  chunks from https://stackoverflow.com/a/312464/3092681
# 		Copytight © 2008 Ned Batchelder
# 		Licensed under CC-BY-SA
#
#  Parts of the docstrings based on the Python 3.8.2 Documentation
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com . All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives . All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum . All rights reserved.
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

# stdlib
import os
import pathlib
import shutil
from typing import AnyStr, Callable, Union


def append(var: str, filename: Union[str, pathlib.Path, os.PathLike]):
	"""
	Append ``var`` to the file ``filename`` in the current directory.

	.. warning::

		This is currently untested

	TODO: make this the file in the given directory, by default the current directory

	:param var: The value to append to the file
	:param filename: The file to append to
	:type filename: str or pathlib.Path or os.PathLike
	"""

	with open(os.path.join(os.getcwd(), filename), 'a') as f:
		f.write(var)


def copytree(
		src: Union[str, pathlib.Path, os.PathLike],
		dst: Union[str, pathlib.Path, os.PathLike],
		symlinks: bool = False,
		ignore: Callable = None,
		):
	"""
	Alternative to :func:`shutil.copytree` to work in some situations where it doesn't.

	:param src: Source file to copy
	:type src: str or pathlib.Path or os.PathLike
	:param dst: Destination to copy file to
	:type dst: str or pathlib.Path or os.PathLike
	:param symlinks: Whether to represent symbolic links in the source as symbolic
		links in the destination. If false or omitted, the contents and metadata
		of the linked files are copied to the new tree. When symlinks is false,
		if the file pointed by the symlink doesn't exist, an exception will be
		added in the list of errors raised in an Error exception at the end of
		the copy process. You can set the optional ignore_dangling_symlinks
		flag to true if you want to silence this exception. Notice that this
		option has no effect on platforms that don’t support :class:`python:os.symlink`.
	:type symlinks: bool, optional
	:param ignore: A callable that will receive as its arguments the source
		directory, and a list of its contents. The ignore callable will be
		called once for each directory that is copied. The callable must return
		a sequence of directory and file names relative to the current
		directory (i.e. a subset of the items in its second argument); these
		names will then be ignored in the copy process.
		:class:`python:shutil.ignore_patterns` can be used to create such a callable
		that ignores names based on
		glob-style patterns.
	:type ignore: ~typing.Callable, optional
	"""

	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)


def delete(filename: Union[str, pathlib.Path, os.PathLike]):
	"""
	Delete the file in the current directory.

	.. warning::

		This is currently untested

	TODO: make this the file in the given directory, by default the current directory

	:param filename: The file to delete
	:type filename: str or pathlib.Path or os.PathLike
	"""

	os.remove(os.path.join(os.getcwd(), filename))


def maybe_make(
		directory: Union[str, pathlib.Path, os.PathLike],
		mode=0o777,
		parents: bool = False,
		exist_ok: bool = False
		):
	"""
	Create a directory at this given path, but only if the directory does not already exist.

	:param directory: Directory to create
	:type directory: str or pathlib.Path or os.PathLike
	:param mode: Combined with the process’ umask value to determine the file mode and access flags
	:type mode:
	:param parents: If ``False`` (the default), a missing parent raises a :class:`~python:FileNotFoundError`.
		If ``True``, any missing parents of this path are created as needed; they are created with the
		default permissions without taking mode into account (mimicking the POSIX mkdir -p command).
	:type parents: bool, optional
	:param exist_ok: If ``False`` (the default), a :class:`~python:FileExistsError` is raised if the
		target directory already exists. If ``True``, :class:`~python:FileExistsError` exceptions
		will be ignored (same behavior as the POSIX mkdir -p command), but only if the last path
		component is not an existing non-directory file.
	:type exist_ok: bool, optional
	"""

	if not isinstance(directory, pathlib.Path):
		directory = pathlib.Path(directory)

	if not directory.exists():
		directory.mkdir(mode, parents, exist_ok)


def parent_path(path: Union[str, pathlib.Path, os.PathLike]) -> pathlib.Path:
	"""
	Returns the path of the parent directory for the given file or directory

	:param path: Path to find the parent for
	:type path: str or pathlib.Path or os.PathLike

	:return: The parent directory
	:rtype: pathlib.Path
	"""

	if not isinstance(path, pathlib.Path):
		path = pathlib.Path(path)

	return path.parent


def read(filename: Union[str, pathlib.Path, os.PathLike]) -> str:
	"""
	Read a file in the current directory (in text mode)

	.. warning::

		This is currently untested

	TODO: make this the file in the given directory, by default the current directory

	:param filename: The file to read from
	:type filename: str or pathlib.Path or os.PathLike

	:return: The contents of the file
	:rtype: str
	"""

	# TODO: docstring

	with open(os.path.join(os.getcwd(), filename)) as f:
		return f.read()


def relpath(
		path: Union[str, pathlib.Path, os.PathLike],
		relative_to: Union[str, pathlib.Path, os.PathLike] = None
		) -> pathlib.Path:
	"""
	Returns the path for the given file or directory relative to the given
	directory or, if that would require path traversal, returns the absolute path.

	:param path: Path to find the relative path for
	:type path: str or pathlib.Path or os.PathLike
	:param relative_to: The directory to find the path relative to.
		Defaults to the current directory
	:type relative_to: str or pathlib.Path or os.PathLike, optional

	:rtype: pathlib.Path
	"""

	if not isinstance(path, pathlib.Path):
		path = pathlib.Path(path)

	abs_path = path.absolute()

	if relative_to is None:
		relative_to = pathlib.Path().absolute()

	if not isinstance(relative_to, pathlib.Path):
		relative_to = pathlib.Path(relative_to)

	relative_to = relative_to.absolute()

	try:
		return abs_path.relative_to(relative_to)
	except ValueError:
		return abs_path


relpath2 = relpath


def write(var: str, filename: Union[str, pathlib.Path, os.PathLike]):
	"""
	Write a variable to file in the current directory

	TODO: make this the file in the given directory, by default the current directory

	:param var: The value to write to the file
	:param filename: The file to write to
	:type filename: str or pathlib.Path or os.PathLike
	"""

	with open(os.path.join(os.getcwd(), filename), 'w') as f:
		f.write(var)
