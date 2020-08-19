#!/usr/bin/env python
#
#  terminal.py
"""
Useful functions for terminal-based programs
"""
#
#  Copyright © 2014-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  get_terminal_size, _get_terminal_size_windows, _get_terminal_size_tput and _get_terminal_size_posix
# 		from https://gist.github.com/jtriley/1108174
#  		Copyright © 2011 jtriley
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
#  "Echo" based on ChemPy (https://github.com/bjodah/chempy)
#  |  Copyright (c) 2015-2018, Björn Dahlgren
#  |  All rights reserved.
#  |
#  |  Redistribution and use in source and binary forms, with or without modification,
#  |  are permitted provided that the following conditions are met:
#  |
#  |    Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |    Redistributions in binary form must reproduce the above copyright notice, this
#  |    list of conditions and the following disclaimer in the documentation and/or
#  |    other materials provided with the distribution.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
#  |  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  |  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  |  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
#  |  ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  |  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  |  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
import inspect
import os
import platform
import pprint
import shlex
import struct
import subprocess
import textwrap
from typing import Any, Optional, Tuple

__all__ = [
		"clear",
		"br",
		"interrupt",
		"overtype",
		"get_terminal_size",
		"Echo",
		]


def clear() -> None:
	"""
	Clears the display.

	Works for Windows and POSIX, but does not clear the Python Interpreter or PyCharm's Console.
	"""

	if os.name == "nt":  # pragma: no cover (!Windows)
		os.system("cls")  # nosec: B607,B605
	else:  # pragma: no cover (!Linux)
		print("\033c", end='')


def br() -> None:
	"""
	Prints a line break
	"""

	print('')


def interrupt() -> None:
	"""
	Print the key combination needed to abort the script; dynamic depending on OS.

	Useful when you have a long-running script that you might want to
	interrupt part way through.
	"""

	print(f"(Press Ctrl-{'C' if os.name == 'nt' else 'D'} to quit at any time.)")


def overtype(*objects, sep: str = ' ', end: str = '', file=None, flush: bool = False) -> None:
	"""
	Print ``objects`` to the text stream ``file``, starting with ``"\\r"``, separated by ``sep``
	and followed by ``end``.

	``sep``, ``end``, ``file`` and ``flush``, if present, must be given as keyword arguments

	All non-keyword arguments are converted to strings like :class:`str` does and written to the stream,
	separated by `sep` and followed by `end`.

	If no objects are given, :func:`~domdf_python_tools.terminal.overtype` will just write ``"\\r"``.

	.. TODO:: This does not currently work in the PyCharm console, at least on Windows

	:param objects: A list of strings or string-like objects to write to the terminal.
	:param sep: String to separate the objects with.
	:type sep: str
	:param end: String to end with.
	:type end: str
	:param file: An object with a ``write(string)`` method.
	:default file: ``sys.stdout``
	:type file:
	:param flush: If true, the stream is forcibly flushed.
	:type flush: bool
	"""

	object0 = f"\r{objects[0]}"
	objects = (object0, *objects[1:])
	print(*objects, sep=sep, end=end, file=file, flush=flush)


def get_terminal_size() -> Tuple[int, int]:  # pragma: no cover
	"""
	Get width and height of console.

	Works on Linux, macOS, Windows, and Cygwin.

	Based on http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python

	:return: tuple_xy
	"""

	current_os = platform.system()
	tuple_xy = None

	if current_os == "Windows":
		tuple_xy = _get_terminal_size_windows()
		if tuple_xy is None:
			tuple_xy = _get_terminal_size_tput()
		# needed for window's python in cygwin's xterm!

	if current_os in {"Linux", "Darwin"} or current_os.startswith("CYGWIN"):
		tuple_xy = _get_terminal_size_posix()

	if tuple_xy is None:
		print("default")
		tuple_xy = (80, 25)  # default value

	return tuple_xy


def _get_terminal_size_windows() -> Optional[Tuple[int, int]]:  # pragma: no cover
	try:

		# stdlib
		from ctypes import create_string_buffer, windll  # type: ignore

		# stdin handle is -10
		# stdout handle is -11
		# stderr handle is -12
		h = windll.kernel32.GetStdHandle(-12)
		csbi = create_string_buffer(22)
		res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)

		if res:
			(buf_x, buf_y, cur_x, cur_y, wattr, left, top, right, bottom, maxx,
				maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
			size_x = right - left + 1
			size_y = bottom - top + 1

			return size_x, size_y
	except Exception:
		pass

	return None


def _get_terminal_size_tput() -> Optional[Tuple[int, int]]:  # pragma: no cover
	# get terminal width
	# src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
	try:
		cols = int(subprocess.check_call(shlex.split("tput cols")))
		rows = int(subprocess.check_call(shlex.split("tput lines")))
		return cols, rows
	except Exception:
		return None


def _get_terminal_size_posix() -> Optional[Tuple[int, int]]:  # pragma: no cover

	# stdlib
	import fcntl
	import termios

	def ioctl_GWINSZ(fd: int) -> Optional[Tuple[Any, ...]]:
		try:
			cr = struct.unpack("hh", fcntl.ioctl(fd, termios.TIOCGWINSZ, b"1234"))
			return cr
		except Exception:
			pass

		return None

	cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)

	if not cr:
		try:
			fd = os.open(os.ctermid(), os.O_RDONLY)  # type: ignore
			cr = ioctl_GWINSZ(fd)
			os.close(fd)
		except Exception:
			pass

	if not cr:
		try:
			cr = (os.environ["LINES"], os.environ["COLUMNS"])
		except Exception:
			return None

	return int(cr[1]), int(cr[0])


class Echo:
	"""
	Context manager for echoing variable assignments (in CPython).

	:param indent: The indentation of the dictionary of variable assignments.
	:type indent: str, optional
	"""

	def __init__(self, indent: str = "  "):
		self.indent = indent

		frame = inspect.currentframe()
		if frame is None:  # pragma: no cover
			raise ValueError("Unable to obtain the frame of the caller.")
		else:
			self.parent_frame = inspect.currentframe().f_back  # type: ignore  # TODO

	def __enter__(self):
		self.locals_on_entry = self.parent_frame.f_locals.copy()  # type: ignore

	def __exit__(self, exc_t, exc_v, tb):
		new_locals = {
				k: v
				for k,
				v in self.parent_frame.f_locals.items()  # type: ignore
				if k not in self.locals_on_entry
				}

		print(textwrap.indent(pprint.pformat(new_locals), self.indent))


if __name__ == "__main__":  # pragma: no cover
	size_x, size_y = get_terminal_size()
	print("width =", size_x, "height =", size_y)
