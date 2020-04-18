# -*- coding: utf-8 -*-
"""
test_utils
~~~~~~~~~~~~~~~

Test functions in utils.py

"""

import types
import pathlib
import decimal

import pytest

from domdf_python_tools.utils import str2tuple, tuple2str, chunks, list2str, list2string, bdict, pyversion
from domdf_python_tools import utils


def test_pyversion():
	assert isinstance(pyversion, int)


def test_str2tuple():
	assert isinstance(str2tuple("1,2,3"), tuple)  # tests without spaces
	assert isinstance(str2tuple("1, 2, 3"), tuple)  # tests with spaces
	assert isinstance(str2tuple("1; 2; 3", sep=";"), tuple)  # tests with semicolon
	assert str2tuple("1,2,3") == (1, 2, 3)


def test_tuple2str():
	assert isinstance(tuple2str(("1", "2", "3",)), str)
	assert tuple2str((1, 2, 3)) == "1,2,3"
	
	assert isinstance(tuple2str((1, 2, 3,), sep=";"), str)  # tests with semicolon
	assert tuple2str((1, 2, 3), sep=";") == "1;2;3"


def test_chunks():
	assert isinstance(chunks(list(range(100)), 5), types.GeneratorType)
	assert list(chunks(list(range(100)), 5))[0] == [0, 1, 2, 3, 4]


def test_list2str():
	assert isinstance(list2str([1, 2, 3, ]), str)
	assert list2str([1, 2, 3]) == "1,2,3"
	
	assert isinstance(list2str([1, 2, 3], sep=";"), str)  # tests with semicolon
	assert list2str((1, 2, 3), sep=";") == "1;2;3"
	
	assert isinstance(list2string([1, 2, 3, ]), str)
	assert list2string([1, 2, 3]) == "1,2,3"
	
	assert isinstance(list2string([1, 2, 3], sep=";"), str)  # tests with semicolon
	assert list2string((1, 2, 3), sep=";") == "1;2;3"


def test_bdict():
	new_dict = bdict(Alice=27, Bob=30, Dom=23)
	
	assert new_dict[23] == "Dom"
	assert new_dict["Alice"] == 27
	
	# test deleting key
	del new_dict["Alice"]
	with pytest.raises(KeyError):
		new_dict["Alice"]
		
	# test booleans
	new_dict["True"] = True
	assert new_dict["True"] is True
	new_dict["False"] = False
	assert new_dict["False"] is False
	new_dict["None"] = None
	assert new_dict["None"] is None


def test_bdict_from_dict():
	original_dict = {"Alice": 27, "Bob": 30, "Dom": 23}
	
	new_dict = bdict(original_dict)
	
	assert new_dict[23] == "Dom"
	assert new_dict["Alice"] == 27


def test_bdict_booleans():
	original_dict = {"True": True, "False": False, "None": None}
	
	new_dict = bdict(original_dict)
	
	assert new_dict[True] == "True"
	assert new_dict["True"]
	
	original_dict = {True: True, False: False, None: None}
	
	new_dict = bdict(original_dict)
	
	assert new_dict[True]


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


def test_bdict_bool():
	new_dict = bdict(N=None, T=True, F=False)
	
	print(new_dict)
	
	assert None in new_dict
	assert True in new_dict
	assert True in new_dict
	
	assert isinstance(new_dict["T"], bool) and new_dict["T"]
	assert isinstance(new_dict["F"], bool) and not new_dict["F"]
	
	assert new_dict[True] == "T"
	assert new_dict[False] == "F"
	assert new_dict[None] == "N"
	
	assert "_None" in new_dict
	assert new_dict["_None"] == "N"
	
	# Test for pyMHDAC
	new_dict_2 = bdict(Unspecified=0, _None=1, GC=2, LC=3, CE=4)
	
	assert None in new_dict_2
	
	assert new_dict_2[None] == 1


def test_as_text():
	assert utils.as_text(12345) == "12345"
	assert utils.as_text(123.45) == "123.45"
	assert utils.as_text([123.45]) == "[123.45]"
	assert utils.as_text({123.45}) == "{123.45}"
	assert utils.as_text((123.45,)) == "(123.45,)"
	assert utils.as_text(None) == ""
	assert utils.as_text(pathlib.Path(".")) == "."
	assert utils.as_text(decimal.Decimal("1234")) == "1234"


def test_split_len():
	assert utils.split_len("Spam Spam Spam Spam Spam Spam Spam Spam ", 5) == ["Spam "]*8


def test_permutations():
	data = ["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"]
	
	assert utils.permutations(data, 1) == [(x,) for x in data]
	assert utils.permutations(data, 2) == [
			('egg and bacon', 'egg sausage and bacon'),
			('egg and bacon', 'egg and spam'),
			('egg and bacon', 'egg bacon and spam'),
			('egg sausage and bacon', 'egg and spam'),
			('egg sausage and bacon', 'egg bacon and spam'),
			('egg and spam', 'egg bacon and spam')]
	assert utils.permutations(data, 3) == [
			('egg and bacon', 'egg sausage and bacon', 'egg and spam'),
			('egg and bacon', 'egg sausage and bacon', 'egg bacon and spam'),
			('egg and bacon', 'egg and spam', 'egg sausage and bacon'),
			('egg and bacon', 'egg and spam', 'egg bacon and spam'),
			('egg and bacon', 'egg bacon and spam', 'egg sausage and bacon'),
			('egg and bacon', 'egg bacon and spam', 'egg and spam'),
			('egg sausage and bacon', 'egg and bacon', 'egg and spam'),
			('egg sausage and bacon', 'egg and bacon', 'egg bacon and spam'),
			('egg sausage and bacon', 'egg and spam', 'egg bacon and spam'),
			('egg sausage and bacon', 'egg bacon and spam', 'egg and spam'),
			('egg and spam', 'egg and bacon', 'egg bacon and spam'),
			('egg and spam', 'egg sausage and bacon', 'egg bacon and spam')]
	assert utils.permutations(data, 4) == [
			('egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam'),
			('egg and bacon',  'egg sausage and bacon', 'egg bacon and spam', 'egg and spam'),
			('egg and bacon', 'egg and spam', 'egg sausage and bacon', 'egg bacon and spam'),
			('egg and bacon', 'egg and spam', 'egg bacon and spam', 'egg sausage and bacon'),
			('egg and bacon', 'egg bacon and spam', 'egg sausage and bacon', 'egg and spam'),
			('egg and bacon', 'egg bacon and spam', 'egg and spam', 'egg sausage and bacon'),
			('egg sausage and bacon', 'egg and bacon', 'egg and spam', 'egg bacon and spam'),
			('egg sausage and bacon', 'egg and bacon', 'egg bacon and spam', 'egg and spam'),
			('egg sausage and bacon', 'egg and spam', 'egg and bacon', 'egg bacon and spam'),
			('egg sausage and bacon', 'egg bacon and spam', 'egg and bacon', 'egg and spam'),
			('egg and spam', 'egg and bacon', 'egg sausage and bacon', 'egg bacon and spam'),
			('egg and spam', 'egg sausage and bacon', 'egg and bacon', 'egg bacon and spam')]
	assert utils.permutations(data, 5) == []
	assert utils.permutations(data, 6) == []
	assert utils.permutations(data, 10) == []
	assert utils.permutations(data, 30) == []
	assert utils.permutations(data, 100) == []
	
	with pytest.raises(ValueError):
		utils.permutations(data, 0)
