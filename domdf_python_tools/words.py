#!/usr/bin/env python
#
#  words.py
"""
Functions for working with (English) words.

..versionadded:: 0.4.5
"""
# stdlib
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
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  List of 10000 English words from https://github.com/first20hours/google-10000-english/
#  Derived from the Google Web Trillion Word Corpus,
#      as described by Thorsten Brants and Alex Franz,
#      and distributed by the Linguistic Data Consortium.
#
#  Subsets of this corpus distributed by Peter Novig.
#  Corpus editing and cleanup by Josh Kaufman.
#
import functools
import random
from typing import List

# 3rd party
import importlib_resources

# this package
import domdf_python_tools
from domdf_python_tools.paths import PathPlus


__all__ = ["get_words_list", "get_random_word"]


@functools.lru_cache()
def get_words_list(min_length: int = 0, max_length: int = -1) -> List[str]:
	"""
	Returns the list of words, optionally only including those
	whose length is between ``min_length`` and ``max_length``.

	:param min_length: The minimum length of the words to return
	:param max_length: The maximum length of the words to return. A value of ``-1`` indicates no upper limit.
	:no-default max_length:

	:return: The list of words meeting the above specifiers.

	..versionadded:: 0.4.5
	"""

	with importlib_resources.path(domdf_python_tools, "google-10000-english-no-swears.txt") as words_file_:
		words_file = PathPlus(words_file_)

	words_list: List[str] = words_file.read_text().splitlines()

	if min_length > 0 or max_length != -1:
		if max_length == -1:
			words_list = [word for word in words_list if min_length <= len(word)]
		else:
			words_list = [word for word in words_list if min_length <= len(word) <= max_length]

	return words_list


def get_random_word(min_length: int = 0, max_length: int = -1) -> str:
	"""
	Returns a random word, optionally only one whose length
	is between ``min_length`` and ``max_length``.

	:param min_length: The minimum length of the words to return
	:param max_length: The maximum length of the words to return. A value of ``-1`` indicates no upper limit.
	:no-default max_length:

	:return: A random word meeting the above specifiers.

	..versionadded:: 0.4.5
	"""

	words_list = get_words_list(min_length=min_length, max_length=max_length)

	return random.choice(words_list)
