"""
test_utils
~~~~~~~~~~~~~~~

Test functions in utils.py

"""

# stdlib
import decimal
import pathlib
import platform
import re
import sys
import types

# 3rd party
import pytest

# this package
from domdf_python_tools import utils
from domdf_python_tools.testing import testing_boolean_values
from domdf_python_tools.utils import Len, chunks, double_chain, list2str, posargs2kwargs, pyversion, str2tuple


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
				(None, ''),
				(pathlib.Path('.'), '.'),
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
	assert stdout[3] == ''
	assert isinstance(missing_deps, list)
	assert len(missing_deps) == 1
	assert missing_deps == ["madeup_module"]

	missing_deps = utils.check_dependencies(["pytest"])
	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
	assert stdout[0] == "All modules installed"
	assert stdout[1] == ''
	assert isinstance(missing_deps, list)
	assert len(missing_deps) == 0
	assert missing_deps == []


def test_chunks():
	assert isinstance(chunks(list(range(100)), 5), types.GeneratorType)
	assert list(chunks(list(range(100)), 5))[0] == [0, 1, 2, 3, 4]
	assert list(chunks(['a', 'b', 'c'], 1)) == [['a'], ['b'], ['c']]


# TODO: cmp


@pytest.mark.parametrize(
		"value, expects",
		[
				([1, 2, 3], "1,2,3"),
				(['a', 'b', 'c'], "a,b,c"),
				(['a', 'b', 1, 2], "a,b,1,2"),
				(['a', 2, pathlib.Path("foo.txt")], "a,2,foo.txt"),
				],
		)
def test_list2str(value, expects):
	str_representation = list2str(value)
	assert isinstance(str_representation, str)
	assert str_representation == expects


@pytest.mark.parametrize(
		"value, expects",
		[
				([1, 2, 3], "1;2;3"),
				(['a', 'b', 'c'], "a;b;c"),
				(['a', 'b', 1, 2], "a;b;1;2"),
				(['a', 2, pathlib.Path("foo.txt")], "a;2;foo.txt"),
				],
		)
def test_list2str_semicolon(value, expects):
	str_representation = list2str(value, sep=';')
	assert isinstance(str_representation, str)
	assert str_representation == expects


def test_permutations():
	data = ["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"]

	assert utils.permutations(data, 1) == [(x, ) for x in data]

	assert utils.permutations(data, 2) == [
			("egg and bacon", "egg sausage and bacon"),
			("egg and bacon", "egg and spam"),
			("egg and bacon", "egg bacon and spam"),
			("egg sausage and bacon", "egg and spam"),
			("egg sausage and bacon", "egg bacon and spam"),
			("egg and spam", "egg bacon and spam"),
			]

	assert utils.permutations(data, 3) == [
			("egg and bacon", "egg sausage and bacon", "egg and spam"),
			("egg and bacon", "egg sausage and bacon", "egg bacon and spam"),
			("egg and bacon", "egg and spam", "egg sausage and bacon"),
			("egg and bacon", "egg and spam", "egg bacon and spam"),
			("egg and bacon", "egg bacon and spam", "egg sausage and bacon"),
			("egg and bacon", "egg bacon and spam", "egg and spam"),
			("egg sausage and bacon", "egg and bacon", "egg and spam"),
			("egg sausage and bacon", "egg and bacon", "egg bacon and spam"),
			("egg sausage and bacon", "egg and spam", "egg bacon and spam"),
			("egg sausage and bacon", "egg bacon and spam", "egg and spam"),
			("egg and spam", "egg and bacon", "egg bacon and spam"),
			("egg and spam", "egg sausage and bacon", "egg bacon and spam"),
			]

	assert utils.permutations(data, 4) == [
			("egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"),
			("egg and bacon", "egg sausage and bacon", "egg bacon and spam", "egg and spam"),
			("egg and bacon", "egg and spam", "egg sausage and bacon", "egg bacon and spam"),
			("egg and bacon", "egg and spam", "egg bacon and spam", "egg sausage and bacon"),
			("egg and bacon", "egg bacon and spam", "egg sausage and bacon", "egg and spam"),
			("egg and bacon", "egg bacon and spam", "egg and spam", "egg sausage and bacon"),
			("egg sausage and bacon", "egg and bacon", "egg and spam", "egg bacon and spam"),
			("egg sausage and bacon", "egg and bacon", "egg bacon and spam", "egg and spam"),
			("egg sausage and bacon", "egg and spam", "egg and bacon", "egg bacon and spam"),
			("egg sausage and bacon", "egg bacon and spam", "egg and bacon", "egg and spam"),
			("egg and spam", "egg and bacon", "egg sausage and bacon", "egg bacon and spam"),
			("egg and spam", "egg sausage and bacon", "egg and bacon", "egg bacon and spam"),
			]

	assert utils.permutations(data, 5) == []
	assert utils.permutations(data, 6) == []
	assert utils.permutations(data, 10) == []
	assert utils.permutations(data, 30) == []
	assert utils.permutations(data, 100) == []

	with pytest.raises(ValueError, match="'n' cannot be 0"):
		utils.permutations(data, 0)


class CustomRepr:

	def __init__(self):
		pass

	def __repr__(self):
		return "This is my custom __repr__!"


class NoRepr:

	def __init__(self):
		pass


no_repr_instance = NoRepr()


def get_mem_addr(obj):
	if sys.platform == "win32" and platform.python_implementation() != "PyPy":
		return f"0x0*{hex(id(obj))[2:].upper()}"
	else:
		return f"0x0*{hex(id(obj))[2:]}"


@pytest.mark.parametrize(
		"obj, expects",
		[
				("This is a test", "'This is a test'"),
				(pathlib.PurePosixPath("foo.txt"), r"PurePosixPath\('foo.txt'\)"),
				(1234, "1234"),
				(12.34, "12.34"),
				(CustomRepr(), "This is my custom __repr__!"),
				(no_repr_instance, f"<tests.test_utils.NoRepr object at {get_mem_addr(no_repr_instance)}>"),
				],
		)
def test_printr(obj, expects, capsys):
	utils.printr(obj)

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert re.match(expects, stdout[0])


@pytest.mark.parametrize(
		"obj, expects",
		[
				("This is a test", "<class 'str'>"),
				(pathlib.PurePosixPath("foo.txt"), "<class 'pathlib.PurePosixPath'>"),
				(1234, "<class 'int'>"),
				(12.34, "<class 'float'>"),
				(CustomRepr(), "<class 'tests.test_utils.CustomRepr'>"),
				(no_repr_instance, "<class 'tests.test_utils.NoRepr'>"),
				],
		)
def test_printt(obj, expects, capsys):
	utils.printt(obj)

	captured = capsys.readouterr()
	stdout = captured.out.split("\n")
	assert stdout[0] == expects


@pytest.mark.parametrize(
		"obj, expects",
		[
				("This is a test", "This is a test"),
				(pathlib.PurePosixPath("foo.txt"), "foo.txt"),
				(1234, "1234"),
				(12.34, "12.34"),
				(CustomRepr(), "This is my custom __repr__!"),
				(no_repr_instance, f"<tests.test_utils.NoRepr object at {get_mem_addr(no_repr_instance)}>"),
				],
		)
def test_stderr_writer(obj, expects, capsys):
	utils.stderr_writer(obj)

	captured = capsys.readouterr()
	stderr = captured.err.split("\n")
	assert re.match(expects, stderr[0])


def test_split_len():
	assert utils.split_len("Spam Spam Spam Spam Spam Spam Spam Spam ", 5) == ["Spam "] * 8


@pytest.mark.parametrize(
		"value, expects",
		[
				("1,2,3", (1, 2, 3)),  # tests without spaces
				("1, 2, 3", (1, 2, 3)),  # tests with spaces
				],
		)
def test_str2tuple(value, expects):
	assert isinstance(str2tuple(value), tuple)
	assert str2tuple(value) == expects


@pytest.mark.parametrize(
		"value, expects",
		[
				("1;2;3", (1, 2, 3)),  # tests without semicolon
				("1; 2; 3", (1, 2, 3)),  # tests with semicolon
				],
		)
def test_str2tuple_semicolon(value, expects):
	assert isinstance(str2tuple(value, sep=';'), tuple)
	assert str2tuple(value, sep=';') == expects


@testing_boolean_values(extra_truthy=[50, -1])
def test_strtobool(boolean_string, expected_boolean):
	assert utils.strtobool(boolean_string) == expected_boolean


@pytest.mark.parametrize(
		"obj, expects",
		[
				("truthy", ValueError),
				("foo", ValueError),
				("bar", ValueError),
				(None, AttributeError),
				(1.0, AttributeError),
				(0.0, AttributeError),
				],
		)
def test_strtobool_errors(obj, expects):
	with pytest.raises(expects):
		utils.strtobool(obj)


@pytest.mark.parametrize(
		"obj, expects",
		[
				(True, True),
				("True", "True"),
				("true", "'true'"),
				('y', "'y'"),
				('Y', "'Y'"),
				(1, 1),
				(0, 0),
				(50, 50),
				(1.0, 1.0),
				(0.0, 0.0),
				(50.0, 50.0),
				(decimal.Decimal("50.0"), "'50.0'"),
				(False, False),
				("False", "False"),
				("false", "'false'"),
				("Hello World", "'Hello World'"),
				],
		)
def test_enquote_value(obj, expects):
	assert utils.enquote_value(obj) == expects


#
#
# @pytest.mark.parametrize("obj, expects", [
# 		("truthy", ValueError),
# 		("foo", ValueError),
# 		("bar", ValueError),
# 		(None, AttributeError),
# 		(1.0, AttributeError),
# 		(0.0, AttributeError),
# 		])
# def test_enquote_value_errors(obj, expects):
# 	with pytest.raises(expects):
# 		utils.enquote_value(obj)


def test_cmp():
	assert isinstance(utils.cmp(5, 20), int)
	assert utils.cmp(5, 20) < 0
	assert utils.cmp(5, 20) == -1

	assert isinstance(utils.cmp(20, 5), int)
	assert utils.cmp(20, 5) > 0
	assert utils.cmp(20, 5) == 1

	assert isinstance(utils.cmp(20, 20), int)
	assert utils.cmp(20, 20) == 0


@pytest.mark.parametrize(
		"value, expects",
		[
				([[(1, 2), (3, 4)], [(5, 6), (7, 8)]], [1, 2, 3, 4, 5, 6, 7, 8]),
				([[(1, 2), (3, 4)], ((5, 6), (7, 8))], [1, 2, 3, 4, 5, 6, 7, 8]),
				([((1, 2), (3, 4)), [(5, 6), (7, 8)]], [1, 2, 3, 4, 5, 6, 7, 8]),
				([((1, 2), (3, 4)), ((5, 6), (7, 8))], [1, 2, 3, 4, 5, 6, 7, 8]),
				((((1, 2), (3, 4)), ((5, 6), (7, 8))), [1, 2, 3, 4, 5, 6, 7, 8]),
				((("12", "34"), ("56", "78")), ["1", "2", "3", "4", "5", "6", "7", "8"]),
				]
		)
def test_double_chain(value, expects):
	assert list(double_chain(value)) == expects


def test_len(capsys):
	assert list(Len("Hello")) == [0, 1, 2, 3, 4]
	assert list(Len("Hello World")) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

	for val in Len("Hello World"):
		print(val)

	captured = capsys.readouterr()
	assert captured.out.splitlines() == ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

	assert Len("Hello") == range(5)


def demo_function(arg1, arg2, arg3):
	pass


@pytest.mark.parametrize(
		"args, posarg_names, kwargs, expects",
		[
				((1, 2, 3), ("arg1", "arg2", "arg3"), {}, {"arg1": 1, "arg2": 2, "arg3": 3}),
				((1, 2, 3), ("arg1", "arg2", "arg3"), None, {"arg1": 1, "arg2": 2, "arg3": 3}),
				((1, 2, 3), ("arg1", "arg2", "arg3"), {"arg4": 4}, {"arg1": 1, "arg2": 2, "arg3": 3, "arg4": 4}),
				((1, 2, 3), demo_function, None, {
						"arg1": 1,
						"arg2": 2,
						"arg3": 3,
						}),
				]
		)
def test_posargs2kwargs(args, posarg_names, kwargs, expects):
	assert posargs2kwargs(args, posarg_names, kwargs) == expects
