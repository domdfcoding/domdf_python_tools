# -*- coding: utf-8 -*-
"""
test_utils
~~~~~~~~~~~~~~~

Test functions in utils.py

"""

import types
import pathlib
import decimal

import pytest  # type: ignore

from domdf_python_tools.utils import str2tuple, tuple2str, chunks, list2str, list2string, pyversion
from domdf_python_tools import utils


def test_pyversion():
	assert isinstance(pyversion, int)


@pytest.mark.parametrize(
		"value, expects",
		[
				(12345, "12345"),
				(123.45, "123.45"),
				([123.45], "[123.45]"),
				({123.45}, "{123.45}"),
				((123.45, ), "(123.45,)"),
				(None, ""),
				(pathlib.Path("."), "."),
				(decimal.Decimal("1234"), "1234"),
				]
		)
def test_as_text(value, expects):
	assert utils.as_text(value) == expects


def test_check_dependencies(capsys):
	deps = ["pytest", "domdf_python_tools", "madeup_module"]

	missing_deps = utils.check_dependencies(deps, False)
	assert isinstance(missing_deps, list)
	assert len(missing_deps) == 1
	assert missing_deps == ["madeup_module"]

	missing_deps = utils.check_dependencies(deps)
	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout[0] == "The following modules are missing."
	assert stdout[1] == "['madeup_module']"
	assert stdout[2] == "Please check the documentation."
	assert stdout[3] == ""
	assert isinstance(missing_deps, list)
	assert len(missing_deps) == 1
	assert missing_deps == ["madeup_module"]

	missing_deps = utils.check_dependencies(["pytest"])
	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout[0] == "All modules installed"
	assert stdout[1] == ""
	assert isinstance(missing_deps, list)
	assert len(missing_deps) == 0
	assert missing_deps == []


def test_chunks():
	assert isinstance(chunks(list(range(100)), 5), types.GeneratorType)
	assert list(chunks(list(range(100)), 5))[0] == [0, 1, 2, 3, 4]
	assert list(chunks(["a", "b", "c"], 1)) == [["a"], ["b"], ["c"]]


# TODO: cmp


@pytest.mark.parametrize(
		"value, expects",
		[
				([1, 2, 3], "1,2,3"),
				(["a", "b", "c"], "a,b,c"),
				(["a", "b", 1, 2], "a,b,1,2"),
				(["a", 2, pathlib.Path("foo.txt")], "a,2,foo.txt"),
				]
		)
def test_list2str(value, expects):
	str_representation = list2str(value)
	assert isinstance(str_representation, str)
	assert str_representation == expects

	str_representation = list2string(value)
	assert isinstance(str_representation, str)
	assert str_representation == expects


@pytest.mark.parametrize(
		"value, expects",
		[
				([1, 2, 3], "1;2;3"),
				(["a", "b", "c"], "a;b;c"),
				(["a", "b", 1, 2], "a;b;1;2"),
				(["a", 2, pathlib.Path("foo.txt")], "a;2;foo.txt"),
				]
		)
def test_list2str_semicolon(value, expects):
	str_representation = list2str(value, sep=";")
	assert isinstance(str_representation, str)
	assert str_representation == expects

	str_representation = list2string(value, sep=";")
	assert isinstance(str_representation, str)
	assert str_representation == expects


def test_permutations():
	data = ["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"]

	assert utils.permutations(data, 1) == [(x, ) for x in data]

	assert utils.permutations(data, 2) == [
			('egg and bacon', 'egg sausage and bacon'),
			('egg and bacon', 'egg and spam'),
			('egg and bacon', 'egg bacon and spam'),
			('egg sausage and bacon', 'egg and spam'),
			('egg sausage and bacon', 'egg bacon and spam'),
			('egg and spam', 'egg bacon and spam'),
			]

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
			('egg and spam', 'egg sausage and bacon', 'egg bacon and spam'),
			]

	assert utils.permutations(data, 4) == [
			('egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam'),
			('egg and bacon', 'egg sausage and bacon', 'egg bacon and spam', 'egg and spam'),
			('egg and bacon', 'egg and spam', 'egg sausage and bacon', 'egg bacon and spam'),
			('egg and bacon', 'egg and spam', 'egg bacon and spam', 'egg sausage and bacon'),
			('egg and bacon', 'egg bacon and spam', 'egg sausage and bacon', 'egg and spam'),
			('egg and bacon', 'egg bacon and spam', 'egg and spam', 'egg sausage and bacon'),
			('egg sausage and bacon', 'egg and bacon', 'egg and spam', 'egg bacon and spam'),
			('egg sausage and bacon', 'egg and bacon', 'egg bacon and spam', 'egg and spam'),
			('egg sausage and bacon', 'egg and spam', 'egg and bacon', 'egg bacon and spam'),
			('egg sausage and bacon', 'egg bacon and spam', 'egg and bacon', 'egg and spam'),
			('egg and spam', 'egg and bacon', 'egg sausage and bacon', 'egg bacon and spam'),
			('egg and spam', 'egg sausage and bacon', 'egg and bacon', 'egg bacon and spam'),
			]

	assert utils.permutations(data, 5) == []
	assert utils.permutations(data, 6) == []
	assert utils.permutations(data, 10) == []
	assert utils.permutations(data, 30) == []
	assert utils.permutations(data, 100) == []

	with pytest.raises(ValueError):
		utils.permutations(data, 0)


class CustomRepr:

	def __init__(self):
		pass

	def __repr__(self):
		return "This is my custom __repr__!"


class NoRepr:

	def __init__(self):
		pass


def test_printr(capsys):
	utils.printr("This is a test")
	utils.printr(pathlib.PurePosixPath("foo.txt"))
	utils.printr(1234)
	utils.printr(12.34)
	utils.printr(CustomRepr())
	utils.printr(NoRepr())

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout[0] == "'This is a test'"
	assert stdout[1] == "PurePosixPath('foo.txt')"
	assert stdout[2] == "1234"
	assert stdout[3] == "12.34"
	assert stdout[4] == "This is my custom __repr__!"
	assert stdout[5].startswith('')


def test_printt(capsys):
	utils.printt("This is a test")
	utils.printt(pathlib.PurePosixPath("foo.txt"))
	utils.printt(1234)
	utils.printt(12.34)
	utils.printt(CustomRepr())
	utils.printt(NoRepr())

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout[0] == "<class 'str'>"
	assert stdout[1] == "<class 'pathlib.PurePosixPath'>"
	assert stdout[2] == "<class 'int'>"
	assert stdout[3] == "<class 'float'>"
	assert stdout[4] == "<class 'tests.test_utils.CustomRepr'>"
	assert stdout[5] == "<class 'tests.test_utils.NoRepr'>"


def test_split_len():
	assert utils.split_len("Spam Spam Spam Spam Spam Spam Spam Spam ", 5) == ["Spam "] * 8


@pytest.mark.parametrize(
		"value, expects",
		[
				("1,2,3", (1, 2, 3)),  # tests without spaces
				("1, 2, 3", (1, 2, 3)),  # tests with spaces
				]
		)
def test_str2tuple(value, expects):
	assert isinstance(str2tuple(value), tuple)
	assert str2tuple(value) == expects


@pytest.mark.parametrize(
		"value, expects",
		[
				("1;2;3", (1, 2, 3)),  # tests without semicolon
				("1; 2; 3", (1, 2, 3)),  # tests with semicolon
				]
		)
def test_str2tuple_semicolon(value, expects):
	assert isinstance(str2tuple(value, sep=";"), tuple)
	assert str2tuple(value, sep=";") == expects
