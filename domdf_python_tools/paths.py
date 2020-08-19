#!/usr/bin/env python
#
#  paths.py
"""
Functions for paths and files.
"""
#
#  Copyright © 2018-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Parts of the docstrings and the PathPlus class based on the Python 3.8.2 Documentation
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com . All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#
#  copytree based on https://stackoverflow.com/a/12514470/3092681
#      Copyright © 2012 atzz
#      Licensed under CC-BY-SA
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

# stdlib
import os
import pathlib
import shutil
import stat
from typing import IO, Any, Callable, Optional

# this package
from domdf_python_tools.typing import PathLike

__all__ = [
		"append",
		"copytree",
		"delete",
		"maybe_make",
		"parent_path",
		"read",
		"relpath",
		"write",
		"clean_writer",
		"make_executable",
		"PathPlus",
		"PosixPathPlus",
		"WindowsPathPlus",
		]


def append(var: str, filename: PathLike, **kwargs) -> int:
	"""
	Append ``var`` to the file ``filename`` in the current directory.

	.. TODO:: make this the file in the given directory, by default the current directory

	:param var: The value to append to the file
	:param filename: The file to append to
	"""

	with open(os.path.join(os.getcwd(), filename), 'a', **kwargs) as f:
		return f.write(var)


def copytree(
		src: PathLike,
		dst: PathLike,
		symlinks: bool = False,
		ignore: Optional[Callable] = None,
		) -> PathLike:
	"""
	Alternative to :func:`shutil.copytree` to support copying to a directory that already exists.

	Based on https://stackoverflow.com/a/12514470/3092681 by https://stackoverflow.com/users/23252/atzz

	In Python 3.8 and above :func:`shutil.copytree` takes a ``dirs_exist_ok`` argument,
	which has the same result.

	:param src: Source file to copy
	:param dst: Destination to copy file to
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
	"""

	for item in os.listdir(src):
		s = os.path.join(src, item)
		d = os.path.join(dst, item)
		if os.path.isdir(s):
			shutil.copytree(s, d, symlinks, ignore)
		else:
			shutil.copy2(s, d)

	return dst


def delete(filename: PathLike, **kwargs):
	"""
	Delete the file in the current directory.

	.. TODO:: make this the file in the given directory, by default the current directory

	:param filename: The file to delete
	"""

	os.remove(os.path.join(os.getcwd(), filename), **kwargs)


def maybe_make(directory: PathLike, mode: int = 0o777, parents: bool = False, exist_ok: bool = False):
	"""
	Create a directory at the given path, but only if the directory does not already exist.

	.. note::

		This will fail silently if a file with the same name already exists.
		This appears to be due to the behaviour of :func:`os.mkdir`.

	:param directory: Directory to create
	:param mode: Combined with the process’ umask value to determine the file mode and access flags
	:type mode:
	:param parents: If :py:obj:`False` (the default), a missing parent raises a :class:`~python:FileNotFoundError`.
		If :py:obj:`True`, any missing parents of this path are created as needed; they are created with the
		default permissions without taking mode into account (mimicking the POSIX mkdir -p command).
	:no-default parents:
	:type parents: bool, optional
	:param exist_ok: If :py:obj:`False` (the default), a :class:`~python:FileExistsError` is raised if the
		target directory already exists. If :py:obj:`True`, :class:`~python:FileExistsError` exceptions
		will be ignored (same behavior as the POSIX mkdir -p command), but only if the last path
		component is not an existing non-directory file.
	:no-default exist_ok:
	:type exist_ok: bool, optional
	"""

	if not isinstance(directory, pathlib.Path):
		directory = pathlib.Path(directory)

	if not directory.exists():
		directory.mkdir(mode, parents, exist_ok)


def parent_path(path: PathLike) -> pathlib.Path:
	"""
	Returns the path of the parent directory for the given file or directory.

	:param path: Path to find the parent for

	:return: The parent directory
	"""

	if not isinstance(path, pathlib.Path):
		path = pathlib.Path(path)

	return path.parent


def read(filename: PathLike, **kwargs) -> str:
	"""
	Read a file in the current directory (in text mode).

	.. TODO:: make this the file in the given directory, by default the current directory

	:param filename: The file to read from

	:return: The contents of the file
	"""

	with open(os.path.join(os.getcwd(), filename), **kwargs) as f:
		return f.read()


def relpath(path: PathLike, relative_to: Optional[PathLike] = None) -> pathlib.Path:
	"""
	Returns the path for the given file or directory relative to the given
	directory or, if that would require path traversal, returns the absolute path.

	:param path: Path to find the relative path for
	:param relative_to: The directory to find the path relative to.
		Defaults to the current directory.
	:no-default relative_to:

	:return:
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


def write(var: str, filename: PathLike, **kwargs) -> None:
	"""
	Write a variable to file in the current directory.

	.. TODO:: make this the file in the given directory, by default the current directory

	:param var: The value to write to the file
	:param filename: The file to write to
	"""

	with open(os.path.join(os.getcwd(), filename), 'w', **kwargs) as f:
		f.write(var)


def clean_writer(string: str, fp: IO) -> None:
	"""
	Write string to ``fp`` without trailing spaces.

	:param string:
	:type string: str
	:param fp:
	"""

	buffer = []

	for line in string.split('\n'):
		buffer.append(line.rstrip())

	while buffer[-1:] == ['']:
		buffer = buffer[:-1]

	for line in buffer:
		fp.write(line)
		fp.write('\n')


def make_executable(filename: PathLike) -> None:
	"""
	Make the given file executable.

	:param filename: Filename of the file to make executable
	"""

	if not isinstance(filename, pathlib.Path):
		filename = pathlib.Path(filename)

	st = os.stat(str(filename))
	os.chmod(str(filename), st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


class PathPlus(pathlib.Path):
	"""
	Subclass of :mod:`pathlib.Path` with additional methods and a default encoding of UTF-8.

	Path represents a filesystem path but unlike PurePath, also offers
	methods to do system calls on path objects. Depending on your system,
	instantiating a Path will return either a PosixPath or a WindowsPath
	object. You can also instantiate a PosixPath or WindowsPath directly,
	but cannot instantiate a WindowsPath on a POSIX system or vice versa.

	.. versionadded:: 0.3.8
	"""

	def __new__(cls, *args, **kwargs):
		if cls is PathPlus:
			cls = WindowsPathPlus if os.name == 'nt' else PosixPathPlus
		self = cls._from_parts(args, init=False)  # type: ignore
		if not self._flavour.is_supported:
			raise NotImplementedError(f"cannot instantiate {cls.__name__!r} on your system")
		self._init()
		return self

	def make_executable(self):
		"""
		Make the file executable.

		.. versionadded:: 0.3.8
		"""

		make_executable(self)

	def write_clean(
			self,
			string: str,
			encoding: Optional[str] = "UTF-8",
			errors: Optional[str] = None,
			):
		"""
		Open the file in text mode, write to it without trailing spaces, and close the file.

		:param string:
		:param encoding: The encoding to write to the file using.
		:param errors:

		.. versionadded:: 0.3.8
		"""

		with self.open("w", encoding=encoding, errors=errors) as fp:
			clean_writer(string, fp)

	def maybe_make(
			self,
			mode: int = 0o777,
			parents: bool = False,
			exist_ok: bool = False,
			):
		"""
		Create a directory at this path, but only if the directory does not already exist.

		.. note::

			This will fail silently if a file with the same name already exists.
			This appears to be due to the behaviour of :func:`os.mkdir`.

		:param mode: Combined with the process’ umask value to determine the file mode and access flags
		:type mode:
		:param parents: If :py:obj:`False` (the default), a missing parent raises a :class:`~python:FileNotFoundError`.
			If :py:obj:`True`, any missing parents of this path are created as needed; they are created with the
			default permissions without taking mode into account (mimicking the POSIX mkdir -p command).
		:no-default parents:
		:type parents: bool, optional
		:param exist_ok: If :py:obj:`False` (the default), a :class:`~python:FileExistsError` is raised if the
			target directory already exists. If :py:obj:`True`, :class:`~python:FileExistsError` exceptions
			will be ignored (same behavior as the POSIX mkdir -p command), but only if the last path
			component is not an existing non-directory file.
		:no-default exist_ok:
		:type exist_ok: bool, optional

		.. versionadded:: 0.3.8
		"""

		maybe_make(self, mode=mode, parents=parents, exist_ok=exist_ok)

	def append_text(
			self,
			string: str,
			encoding: Optional[str] = "UTF-8",
			errors: Optional[str] = None,
			):
		"""
		Open the file in text mode, append the given string to it, and close the file.

		:param string:
		:type string: str
		:param encoding: The encoding to write to the file using.
		:param errors:

		.. versionadded:: 0.3.8
		"""

		with self.open("a", encoding=encoding, errors=errors) as fp:
			fp.write(string)

	def write_text(
			self,
			data: str,
			encoding: Optional[str] = "UTF-8",
			errors: Optional[str] = None,
			) -> int:
		"""
		Open the file in text mode, write to it, and close the file.

		:param data:
		:type data: str
		:param encoding: The encoding to write to the file using.
		:param errors:

		.. versionadded:: 0.3.8
		"""

		return super().write_text(data, encoding=encoding, errors=errors)

	def read_text(
			self,
			encoding: Optional[str] = "UTF-8",
			errors: Optional[str] = None,
			) -> str:
		"""
		Open the file in text mode, read it, and close the file.

		:param encoding: The encoding to write to the file using.
		:param errors:

		:return: The content of the file.

		.. versionadded:: 0.3.8
		"""

		return super().read_text(encoding=encoding, errors=errors)

	def open(
			self,
			mode: str = "r",
			buffering: int = -1,
			encoding: Optional[str] = "UTF-8",
			errors: Optional[str] = None,
			newline: Optional[str] = None,
			) -> IO[Any]:
		"""
		Open the file pointed by this path and return a file object, as
		the built-in open() function does.

		:param mode: The mode to open the file in.
		:default mode: ``"r"`` (read only)
		:type mode: str
		:param buffering:
		:type buffering: int
		:param encoding:
		:type encoding: str
		:param errors:
		:param newline:

		:return:

		.. versionadded:: 0.3.8
		"""

		if 'b' in mode:
			encoding = None
		return super().open(mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline)


class PosixPathPlus(PathPlus, pathlib.PurePosixPath):
	"""Path subclass for non-Windows systems.

	On a POSIX system, instantiating a PathPlus object should return an instance of this class.

	.. versionadded:: 0.3.8
	"""
	__slots__ = ()


class WindowsPathPlus(PathPlus, pathlib.PureWindowsPath):
	"""Path subclass for Windows systems.

	On a Windows system, instantiating a PathPlus object should return an instance of this class.

	.. versionadded:: 0.3.8
	"""
	__slots__ = ()

	def owner(self):  # pragma: no cover
		raise NotImplementedError("Path.owner() is unsupported on this system")

	def group(self):  # pragma: no cover
		raise NotImplementedError("Path.group() is unsupported on this system")

	def is_mount(self):  # pragma: no cover
		raise NotImplementedError("Path.is_mount() is unsupported on this system")
