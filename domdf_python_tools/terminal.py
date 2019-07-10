#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  terminal.py
"""Useful functions for terminal-based programs"""
#
#  Copyright 2014-2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  get_terminal_size, _get_terminal_size_windows, _get_terminal_size_tput and _get_terminal_size_linux
#		from https://gist.github.com/jtriley/1108174
#  		Copyright 2011 jtriley
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
import sys
import shlex
import struct
import platform
import subprocess
from .__init__ import pyversion


def clear():
	"""
	Clear the display
	
	works for Windows and UNIX, but does not clear Python Shell
	
	:return:
	"""
	
	return os.system('cls' if os.name == 'nt' else 'clear')
	

def br():
	"""
	Prints a line break
	"""
	
	print("")

def entry(text_to_print):
	"""
	Version-agnostic input function
	
	# TODO: Deprecation warning
	
	:param text_to_print: Text to print before the input field
	:type text_to_print: str
	
	:return: Text entered
	:rtype: str
	"""
	
	if pyversion == 3:
		return input(text_to_print)
	elif pyversion == 2:
		return raw_input(text_to_print)


def interrupt():
	"""
	Print what to do to abort the script; dynamic depending on OS
	Useful when you have a long-running script that you might want t interrupt part way through
	"""
	
	print('(Press Ctrl-%s to quit at any time.)' % 'C' if os.name == 'nt' else 'D')


def overtype(*objects, sep=' ', end='', file=sys.stdout, flush=False):
	"""
	Print `objects` to the text stream `file`, starting with "\r", separated by `sep` and followed by `end`.
	`sep`, `end`, `file` and `flush`, if present, must be given as keyword arguments

	All non-keyword arguments are converted to strings like ``str()`` does and written to the stream,
	separated by `sep` and followed by `end`.

	If no objects are given, ``overwrite()` will just write "\r".

	Based on the Python print() docs: https://docs.python.org/3/library/functions.html#print

	# This does not currently work in the PyCharm console, at least on Windows

	:param objects:
	:param sep: String to separate the objects with, by default " "
	:type sep: str
	:param end: String to end with, by default nothing
	:type end: str
	:param file: An object with a ``write(string)`` method; default ``sys.stdout``
	:param flush: If true, the stream is forcibly flushed.
	:type flush: bool
	:return:
	"""
	
	object0 = f"\r{objects[0]}"
	objects = (object0, *objects[1:])
	print(*objects, sep=sep, end=end, file=file, flush=flush)


def get_terminal_size():
	"""
	Get width and height of console
	
	Works on linux,os x,windows,cygwin(windows)
	
	Originally retrieved from: http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
	
	:return: tuple_xy
	"""
	
	current_os = platform.system()
	tuple_xy = None
	if current_os == 'Windows':
		tuple_xy = _get_terminal_size_windows()
		if tuple_xy is None:
			tuple_xy = _get_terminal_size_tput()
		# needed for window's python in cygwin's xterm!
	if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
		tuple_xy = _get_terminal_size_linux()
	if tuple_xy is None:
		print("default")
		tuple_xy = (80, 25)      # default value
	return tuple_xy


def _get_terminal_size_windows():
	try:
		from ctypes import windll, create_string_buffer
		# stdin handle is -10
		# stdout handle is -11
		# stderr handle is -12
		h = windll.kernel32.GetStdHandle(-12)
		csbi = create_string_buffer(22)
		res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
		if res:
			(bufx, bufy, curx, cury, wattr,
			 left, top, right, bottom,
			 maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
			sizex = right - left + 1
			sizey = bottom - top + 1
			return sizex, sizey
	except:
		pass


def _get_terminal_size_tput():
	# get terminal width
	# src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
	try:
		cols = int(subprocess.check_call(shlex.split('tput cols')))
		rows = int(subprocess.check_call(shlex.split('tput lines')))
		return (cols, rows)
	except:
		pass


def _get_terminal_size_linux():
	def ioctl_GWINSZ(fd):
		try:
			import fcntl
			import termios
			cr = struct.unpack('hh',
							   fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
			return cr
		except:
			pass
	cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
	if not cr:
		try:
			fd = os.open(os.ctermid(), os.O_RDONLY)
			cr = ioctl_GWINSZ(fd)
			os.close(fd)
		except:
			pass
	if not cr:
		try:
			cr = (os.environ['LINES'], os.environ['COLUMNS'])
		except:
			return None
	return int(cr[1]), int(cr[0])

if __name__ == "__main__":
	sizex, sizey = get_terminal_size()
	print('width =', sizex, 'height =', sizey)
