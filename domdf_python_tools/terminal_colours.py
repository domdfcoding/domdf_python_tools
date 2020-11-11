#!/usr/bin/env python
#
#  terminal_colours.py
"""
Functions for adding colours to terminal print statements.

This module generates ANSI character codes to printing colors to terminals.
See: http://en.wikipedia.org/wiki/ANSI_escape_code

.. deprecated:: Use :mod:`consolekit.terminal_colours` instead.
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
#  Distributed under the BSD 3-Clause license.
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
#
#  _ansi_re and strip_ansi based on https://github.com/pallets/click
#  Copyright 2014 Pallets
#  Distributed under the BSD 3-Clause license.
#


from consolekit.terminal_colours import (
	CSI,
	OSC,
	BEL,
	code_to_chars,
	set_title,
	clear_line,
	Colour,
	AnsiCodes,
	AnsiCursor,
	AnsiFore,
	AnsiBack,
	AnsiStyle,
	Fore,
	Back,
	Style,
	Cursor,
	strip_ansi,
	fore_stack,
	back_stack,
	style_stack,
	)

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
		"strip_ansi",
		]


def clear_screen(mode: int = 2) -> str:
	return CSI + str(mode) + 'J'
