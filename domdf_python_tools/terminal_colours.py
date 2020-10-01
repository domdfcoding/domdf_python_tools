#!/usr/bin/env python
#
#  terminal_colours.py
"""
Functions for adding colours to terminal print statements.

This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
#  Based on colorama
#  https://github.com/tartley/colorama
#  Copyright Jonathan Hartley 2013
#  Distrubuted under the BSD 3-Clause license.
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are met:
#  |
#  |  * Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |  * Redistributions in binary form must reproduce the above copyright notice,
#  |    this list of conditions and the following disclaimer in the documentation
#  |    and/or other materials provided with the distribution.
#  |
#  |  * Neither the name of the copyright holders, nor those of its contributors
#  |    may be used to endorse or promote products derived from this software without
#  |    specific prior written permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  |  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  |  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  |  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  |  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  |  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  |  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  |  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  |  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  Includes modifications to colorama made by Bram Geelen in
#  https://github.com/tartley/colorama/pull/141/files

# stdlib
from abc import ABC
from typing import List

# 3rd party
from colorama import init  # type: ignore
from typing_extensions import Final

__all__ = [
		"CSI",
		"OSC",
		"BEL",
		"code_to_chars",
		"set_title",
		"clear_screen",
		"clear_line",
		"Colour",
		"AnsiCodes",
		"AnsiCursor",
		"AnsiFore",
		"AnsiBack",
		"AnsiStyle",
		"Fore",
		"Back",
		"Style",
		"Cursor",
		]

init()

CSI: Final[str] = "\033["
OSC: Final[str] = "\033]"
BEL: Final[str] = "\a"

fore_stack: List[str] = []
back_stack: List[str] = []
style_stack: List[str] = []


def code_to_chars(code) -> str:
	return CSI + str(code) + 'm'


def set_title(title: str) -> str:
	return OSC + "2;" + title + BEL


def clear_screen(mode: int = 2) -> str:
	return CSI + str(mode) + 'J'


def clear_line(mode: int = 2) -> str:
	return CSI + str(mode) + 'K'


class Colour(str):
	"""
	An ANSI escape sequence representing a colour.

	The colour can be used as a context manager, a string, or a function.

	:param style: Escape sequence representing the style.
	:type style: str
	:param stack: The stack to place the escape sequence on.
	:type stack: str
	:param reset: The escape requence the reset the style.
	:type reset: str
	"""

	style: str
	reset: str
	stack: List[str]

	def __new__(cls, style: str, stack: List[str], reset: str) -> "Colour":
		color = super().__new__(cls, style)  # type: ignore
		color.style = style
		color.stack = stack
		color.reset = reset

		return color

	def __enter__(self) -> None:
		print(self.style, end='')
		self.stack.append(self.style)

	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		if self.style == self.stack[-1]:
			self.stack.pop()
			print(self.stack[-1], end='')

	def __call__(self, text) -> str:
		return f"{self}{text}{self.reset}"


class AnsiCodes(ABC):
	"""
	Abstract base class for ANSI Codes.
	"""

	_stack: List[str]
	_reset: str

	def __init__(self) -> None:
		"""
		The subclasses declare class attributes which are numbers.

		Upon instantiation we define instance attributes, which are the same
		as the class attributes but wrapped with the ANSI escape sequence.
		"""

		for name in dir(self):
			if not name.startswith('_'):
				value = getattr(self, name)
				setattr(self, name, Colour(code_to_chars(value), self._stack, self._reset))


class AnsiCursor:

	def UP(self, n: int = 1) -> str:
		"""

		:param n:
		"""

		return f"{CSI}{str(n)}A"

	def DOWN(self, n: int = 1) -> str:
		"""

		:param n:
		"""

		return f"{CSI}{str(n)}B"

	def FORWARD(self, n: int = 1) -> str:
		"""

		:param n:
		"""

		return f"{CSI}{str(n)}C"

	def BACK(self, n: int = 1) -> str:
		"""

		:param n:
		"""

		return f"{CSI}{str(n)}D"

	def POS(self, x: int = 1, y: int = 1) -> str:
		"""

		:param x:
		:param y:
		"""

		return f"{CSI}{str(y)};{str(x)}H"


class AnsiFore(AnsiCodes):
	"""
	ANSI Colour Codes for foreground colour.

	The colours can be used as a context manager, a string, or a function.

	Valid values are:

	* BLACK
	* RED
	* GREEN
	* YELLOW
	* BLUE
	* MAGENTA
	* CYAN
	* WHITE
	* RESET
	* LIGHTBLACK_EX
	* LIGHTRED_EX
	* LIGHTGREEN_EX
	* LIGHTYELLOW_EX
	* LIGHTBLUE_EX
	* LIGHTMAGENTA_EX
	* LIGHTCYAN_EX
	* LIGHTWHITE_EX
	"""

	_stack = fore_stack
	_reset = "\033[39m"

	BLACK = 30
	RED = 31
	GREEN = 32
	YELLOW = 33
	BLUE = 34
	MAGENTA = 35
	CYAN = 36
	WHITE = 37
	RESET = 39

	# These are fairly well supported, but not part of the standard.
	LIGHTBLACK_EX = 90
	LIGHTRED_EX = 91
	LIGHTGREEN_EX = 92
	LIGHTYELLOW_EX = 93
	LIGHTBLUE_EX = 94
	LIGHTMAGENTA_EX = 95
	LIGHTCYAN_EX = 96
	LIGHTWHITE_EX = 97


class AnsiBack(AnsiCodes):
	"""
	ANSI Colour Codes for background colour.

	The colours can be used as a context manager, a string, or a function.

	Valid values are:

	* BLACK
	* RED
	* GREEN
	* YELLOW
	* BLUE
	* MAGENTA
	* CYAN
	* WHITE
	* RESET
	* LIGHTBLACK_EX
	* LIGHTRED_EX
	* LIGHTGREEN_EX
	* LIGHTYELLOW_EX
	* LIGHTBLUE_EX
	* LIGHTMAGENTA_EX
	* LIGHTCYAN_EX
	* LIGHTWHITE_EX
	"""

	_stack = back_stack
	_reset = "\033[49m"

	BLACK = 40
	RED = 41
	GREEN = 42
	YELLOW = 43
	BLUE = 44
	MAGENTA = 45
	CYAN = 46
	WHITE = 47
	RESET = 49

	# These are fairly well supported, but not part of the standard.
	LIGHTBLACK_EX = 100
	LIGHTRED_EX = 101
	LIGHTGREEN_EX = 102
	LIGHTYELLOW_EX = 103
	LIGHTBLUE_EX = 104
	LIGHTMAGENTA_EX = 105
	LIGHTCYAN_EX = 106
	LIGHTWHITE_EX = 107


class AnsiStyle(AnsiCodes):
	"""
	ANSI Colour Codes for text style.

	Valid values are:

	* BRIGHT
	* DIM
	* NORMAL

	Additionally, ``AnsiStyle.RESET_ALL`` can be used to reset the
	foreground and background colours as well as the text style.
	"""

	_stack = style_stack
	_reset = "\033[22m"

	BRIGHT = 1
	DIM = 2
	NORMAL = 22
	RESET_ALL = 0


Fore = AnsiFore()
Back = AnsiBack()
Style = AnsiStyle()
Cursor = AnsiCursor()

fore_stack.append(Fore.RESET)
back_stack.append(Back.RESET)
style_stack.append(Style.NORMAL)
