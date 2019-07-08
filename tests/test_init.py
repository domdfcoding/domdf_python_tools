# -*- coding: utf-8 -*-
"""
test_init
~~~~~~~~~~~~~~~

Test functions in __init__.py

"""

import types

from domdf_python_tools import pyversion, str2tuple, tuple2str, chunks, list2str, list2string

def test_pyversion():
	assert isinstance(pyversion, int)

def test_str2tuple():
	assert isinstance(str2tuple("1,2,3"), tuple) # tests without spaces
	assert isinstance(str2tuple("1, 2, 3"), tuple) # tests with spaces
	assert isinstance(str2tuple("1; 2; 3", sep=";"), tuple) # tests with semicolon
	if str2tuple("1,2,3") == (1, 2, 3):
		assert 1
	else:
		assert 0
		
def test_tuple2str():
	assert isinstance(tuple2str(("1","2","3",)), str)
	if tuple2str((1, 2, 3)) == "1,2,3":
		assert 1
	else:
		assert 0
		
	assert isinstance(tuple2str((1,2,3,), sep=";"), str) # tests with semicolon
	if tuple2str((1, 2, 3), sep=";") == "1;2;3":
		assert 1
	else:
		assert 0

def test_chunks():
	assert isinstance(chunks(list(range(100)), 5), types.GeneratorType)
	if list(chunks(list(range(100)), 5))[0] == [0,1,2,3,4]:
		assert 1
	else:
		assert 0


def test_list2str():
	assert isinstance(list2str([1, 2, 3,]), str)
	if list2str([1, 2, 3]) == "1,2,3":
		assert 1
	else:
		assert 0
	
	assert isinstance(list2str([1, 2, 3], sep=";"), str)  # tests with semicolon
	if list2str((1, 2, 3), sep=";") == "1;2;3":
		assert 1
	else:
		assert 0
	
	assert isinstance(list2string([1, 2, 3, ]), str)
	if list2string([1, 2, 3]) == "1,2,3":
		assert 1
	else:
		assert 0
	
	assert isinstance(list2string([1, 2, 3], sep=";"), str)  # tests with semicolon
	if list2string((1, 2, 3), sep=";") == "1;2;3":
		assert 1
	else:
		assert 0


