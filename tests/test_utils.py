# -*- coding: utf-8 -*-
"""
test_utils
~~~~~~~~~~~~~~~

Test functions in utils.py

"""

import types

import pytest

from domdf_python_tools.utils import str2tuple, tuple2str, chunks, list2str, list2string, bdict


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


def test_bdict():
	new_dict = bdict(Alice=27, Bob=30, Dom=23)
	
	assert new_dict[23] == "Dom"
	assert new_dict["Alice"] == 27
	
	
def test_bdict_from_dict():
	
	original_dict = {"Alice": 27, "Bob": 30, "Dom": 23}
	
	new_dict = bdict(original_dict)
	
	assert new_dict[23] == "Dom"
	assert new_dict["Alice"] == 27
	
	
def test_bdict_from_zip():
	
	new_dict = bdict(zip(["Alice", "Bob", "Dom"], [27, 30, 23]))
	
	assert new_dict[23] == "Dom"
	assert new_dict["Alice"] == 27


def test_bdict_from_list():
	new_dict = bdict([("Alice", 27), ("Bob", 30), ("Dom", 23)])
	
	assert new_dict[23] == "Dom"
	assert new_dict["Alice"] == 27


def test_bdict_errors():
	new_dict = bdict([("Key1", "Value1"), ("Key2", "Value2"), ("Key3", "Value3")])
	
	with pytest.raises(ValueError):
		new_dict["Key1"] = 1234
	with pytest.raises(ValueError):
		new_dict["Value1"] = 1234
	new_dict["Key1"] = "Value1"
	new_dict["Value1"] = "Key1"
