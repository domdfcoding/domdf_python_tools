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

from domdf_python_tools.utils import str2tuple, tuple2str, chunks, list2str, list2string, pyversion
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

#
#
# def test_bdict_errors():
# 	new_dict = bdict([("Key1", "Value1"), ("Key2", "Value2"), ("Key3", "Value3")])
#
# 	with pytest.raises(ValueError):
# 		new_dict["Key1"] = 1234
# 	with pytest.raises(ValueError):
# 		new_dict["Value1"] = 1234
# 	new_dict["Key1"] = "Value1"
# 	new_dict["Value1"] = "Key1"
#
#


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
	assert utils.split_len("Spam Spam Spam Spam Spam Spam Spam Spam ", 5) == ["Spam "] * 8


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
