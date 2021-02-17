# stdlib
import datetime
import platform
import random
import re
import sys

# 3rd party
import pytest
from _pytest.mark import Mark, MarkDecorator
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from domdf_python_tools import testing
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.testing import (
		check_file_output,
		min_version,
		not_macos,
		not_pypy,
		not_windows,
		only_macos,
		only_pypy,
		only_version,
		only_windows,
		with_fixed_datetime
		)
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


@pytest.mark.parametrize(
		"py_version",
		[
				pytest.param((3, 4), marks=only_version(3.4, "Success")),
				pytest.param((3, 5), marks=only_version(3.5, "Success")),
				pytest.param((3, 6), marks=only_version(3.6, "Success")),
				pytest.param((3, 8), marks=only_version(3.8, "Success")),
				pytest.param((3, 9), marks=only_version(3.9, "Success")),
				pytest.param((3, 10), marks=only_version(3.10, "Success")),
				]
		)
def test_only_version(py_version):
	if sys.version_info[:2] != py_version:
		assert False  # noqa: PT015


@not_pypy("Success")
def test_not_pypy():
	if platform.python_implementation() == "PyPy":
		assert False  # noqa: PT015


@only_pypy("Success")
def test_only_pypy():
	if platform.python_implementation() != "PyPy":
		assert False  # noqa: PT015


@not_windows("Success")
def test_not_windows():
	if sys.platform == "win32":
		assert False  # noqa: PT015


@only_windows("Success")
def test_only_windows():
	if sys.platform != "win32":
		assert False  # noqa: PT015


@not_macos("Success")
def test_not_macos():
	if sys.platform == "darwin":
		assert False  # noqa: PT015


@only_macos("Success")
def test_only_macos():
	if sys.platform != "darwin":
		assert False  # noqa: PT015


def test_tmp_pathplus(tmp_pathplus: PathPlus):
	assert isinstance(tmp_pathplus, PathPlus)
	assert tmp_pathplus.exists()


def test_check_file_output(tmp_pathplus: PathPlus, file_regression: FileRegressionFixture):
	with pytest.raises(FileNotFoundError, match=r"No such file or directory: ('.*'|.*PathPlus\('.*'\))"):
		check_file_output(tmp_pathplus / "file.txt", file_regression)

	(tmp_pathplus / "file.txt").write_text("Success!")
	check_file_output(tmp_pathplus / "file.txt", file_regression)


def test_fixed_datetime(fixed_datetime):
	assert datetime.datetime.today() == datetime.datetime(2020, 10, 13)
	assert datetime.datetime.now() == datetime.datetime(2020, 10, 13, 2, 20)

	assert datetime.datetime.__name__ == "datetime"
	assert datetime.datetime.__qualname__ == "datetime"
	assert datetime.datetime.__module__ == "datetime"

	assert datetime.date.today() == datetime.date(2020, 10, 13)

	assert datetime.date.__name__ == "date"
	assert datetime.date.__qualname__ == "date"
	assert datetime.date.__module__ == "datetime"


@pytest.mark.parametrize(
		"fake_datetime, expected_date",
		[
				pytest.param(datetime.datetime(2020, 10, 13, 2, 20), datetime.datetime(2020, 10, 13), id='0'),
				pytest.param(datetime.datetime(2020, 7, 4, 10, 00), datetime.datetime(2020, 7, 4), id='1'),
				]
		)
def test_with_fixed_datetime(fake_datetime, expected_date: datetime.datetime):

	with with_fixed_datetime(fake_datetime):
		assert datetime.datetime.today() == expected_date
		assert datetime.datetime.now() == fake_datetime

		assert datetime.datetime.__name__ == "datetime"
		assert datetime.datetime.__qualname__ == "datetime"
		assert datetime.datetime.__module__ == "datetime"

		assert datetime.date.today() == expected_date.date()
		assert isinstance(datetime.date.today(), datetime.date)

		assert datetime.date.__name__ == "date"
		assert datetime.date.__qualname__ == "date"
		assert datetime.date.__module__ == "datetime"


@min_version((3, 4), reason="Failure")
def test_min_version():
	pass
