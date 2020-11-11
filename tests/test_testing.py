# stdlib
import platform
import random
import re

# 3rd party
from _pytest.mark import Mark, MarkDecorator

# this package
from domdf_python_tools import testing
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.testing import not_pypy
from domdf_python_tools.utils import strtobool


def test_count():
	assert isinstance(testing.count(100), MarkDecorator)
	assert isinstance(testing.count(100).mark, Mark)
	assert "count" in testing.count(100).mark.args
	assert testing.count(100).mark.args[0] == "count"
	assert testing.count(100).mark.args[1] == range(0, 100)

	assert testing.count(10).mark.args[1] == range(0, 10)
	assert testing.count(10, 5).mark.args[1] == range(5, 10)  # order of count is "stop, start, step"
	assert testing.count(10, 5, 2).mark.args[1] == range(5, 10, 2)  # order of count is "stop, start, step"


def test_whitespace_perms():
	random.seed(1234)

	assert isinstance(testing.whitespace_perms(), MarkDecorator)
	assert isinstance(testing.whitespace_perms().mark, Mark)
	assert "char" in testing.whitespace_perms().mark.args
	assert testing.whitespace_perms().mark.args[0] == "char"
	assert len(testing.whitespace_perms().mark.args[1]) == 20
	assert len(testing.whitespace_perms(1).mark.args[1]) == 41
	assert len(testing.whitespace_perms(0.1).mark.args[1]) == 4

	assert isinstance(testing.whitespace_perms(0.1).mark.args[1], list)
	assert isinstance(testing.whitespace_perms(0.1).mark.args[1][0], str)

	assert testing.whitespace_perms(0.1).mark.args[1] == ["\n\t\r", "\r\t", "\t \n", "\n\r"]

	for string in testing.whitespace_perms().mark.args[1]:
		assert re.match(r"^\s*$", string)


def test_testing_boolean_strings():
	assert isinstance(testing.testing_boolean_values(), MarkDecorator)
	assert isinstance(testing.testing_boolean_values().mark, Mark)
	assert "boolean_string, expected_boolean" in testing.testing_boolean_values().mark.args
	assert testing.testing_boolean_values().mark.args[0] == "boolean_string, expected_boolean"
	assert len(testing.testing_boolean_values().mark.args[1]) == 28
	assert isinstance(testing.testing_boolean_values().mark.args[1], list)
	assert isinstance(testing.testing_boolean_values().mark.args[1][0], tuple)
	assert len(testing.testing_boolean_values().mark.args[1][0]) == 2
	assert isinstance(testing.testing_boolean_values().mark.args[1][0][0], bool)
	assert isinstance(testing.testing_boolean_values().mark.args[1][0][1], bool)

	for value, expects in testing.testing_boolean_values().mark.args[1]:
		assert strtobool(value) is expects


def test_generate_truthy():
	random.seed(1234)

	assert list(testing.generate_truthy_values()) == [
			True,
			"True",
			"true",
			"tRUe",
			'y',
			'Y',
			"YES",
			"yes",
			"Yes",
			"yEs",
			"ON",
			"on",
			'1',
			1,
			]

	assert list(testing.generate_truthy_values(["bar"])) == [
			True,
			"True",
			"true",
			"tRUe",
			'y',
			'Y',
			"YES",
			"yes",
			"Yes",
			"yEs",
			"ON",
			"on",
			'1',
			1,
			"bar",
			]

	assert list(testing.generate_truthy_values(ratio=0.3)) == ['1', "yes", "True", True]


def test_generate_falsy():
	random.seed(1234)

	assert list(testing.generate_falsy_values()) == [
			False,
			"False",
			"false",
			"falSE",
			'n',
			'N',
			"NO",
			"no",
			"nO",
			"OFF",
			"off",
			"oFF",
			'0',
			0,
			]

	assert list(testing.generate_falsy_values(["bar"])) == [
			False,
			"False",
			"false",
			"falSE",
			'n',
			'N',
			"NO",
			"no",
			"nO",
			"OFF",
			"off",
			"oFF",
			'0',
			0,
			"bar",
			]

	assert list(testing.generate_falsy_values(ratio=0.3)) == ['0', "no", "False", False]


@not_pypy("Success")
def test_not_pypy():
	if platform.python_implementation() == "PyPy":
		assert False  # noqa: PT015


pytest_plugins = ("domdf_python_tools.testing", )


def test_tmp_pathplus(tmp_pathplus):
	assert isinstance(tmp_pathplus, PathPlus)
	assert tmp_pathplus.exists()
