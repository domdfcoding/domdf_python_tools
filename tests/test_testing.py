# stdlib
import random
import re

# 3rd party
from _pytest.mark import Mark, MarkDecorator

# this package
from domdf_python_tools.testing import (
		count,
		generate_falsy_values,
		generate_truthy_values,
		testing_boolean_values,
		whitespace_perms,
		)
from domdf_python_tools.utils import strtobool


def test_count():
	assert isinstance(count(100), MarkDecorator)
	assert isinstance(count(100).mark, Mark)
	assert "count" in count(100).mark.args
	assert count(100).mark.args[0] == "count"
	assert count(100).mark.args[1] == range(0, 100)

	assert count(10).mark.args[1] == range(0, 10)
	assert count(10, 5).mark.args[1] == range(5, 10)  # order of count is "stop, start, step"
	assert count(10, 5, 2).mark.args[1] == range(5, 10, 2)  # order of count is "stop, start, step"


def test_whitespace_perms():
	random.seed(1234)

	assert isinstance(whitespace_perms(), MarkDecorator)
	assert isinstance(whitespace_perms().mark, Mark)
	assert "char" in whitespace_perms().mark.args
	assert whitespace_perms().mark.args[0] == "char"
	assert len(whitespace_perms().mark.args[1]) == 20
	assert len(whitespace_perms(1).mark.args[1]) == 41
	assert len(whitespace_perms(.1).mark.args[1]) == 4

	assert isinstance(whitespace_perms(.1).mark.args[1], list)
	assert isinstance(whitespace_perms(.1).mark.args[1][0], str)

	assert whitespace_perms(.1).mark.args[1] == ['\n\t\r', '\r\t', '\t \n', '\n\r']

	for string in whitespace_perms().mark.args[1]:
		assert re.match(r"^\s*$", string)


def test_testing_boolean_strings():
	assert isinstance(testing_boolean_values(), MarkDecorator)
	assert isinstance(testing_boolean_values().mark, Mark)
	assert "boolean_string, expected_boolean" in testing_boolean_values().mark.args
	assert testing_boolean_values().mark.args[0] == "boolean_string, expected_boolean"
	assert len(testing_boolean_values().mark.args[1]) == 28
	assert isinstance(testing_boolean_values().mark.args[1], list)
	assert isinstance(testing_boolean_values().mark.args[1][0], tuple)
	assert len(testing_boolean_values().mark.args[1][0]) == 2
	assert isinstance(testing_boolean_values().mark.args[1][0][0], bool)
	assert isinstance(testing_boolean_values().mark.args[1][0][1], bool)

	for value, expects in testing_boolean_values().mark.args[1]:
		assert strtobool(value) is expects


def test_generate_truthy():
	random.seed(1234)

	assert list(generate_truthy_values()) == [
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

	assert list(generate_truthy_values(["bar"])) == [
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

	assert list(generate_truthy_values(ratio=.3)) == ['1', 'yes', 'True', True]


def test_generate_falsy():
	random.seed(1234)

	assert list(generate_falsy_values()) == [
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

	assert list(generate_falsy_values(["bar"])) == [
			False, "False", "false", "falSE", 'n', 'N', "NO", "no", "nO", "OFF", "off", "oFF", '0', 0, "bar"
			]

	assert list(generate_falsy_values(ratio=.3)) == ['0', 'no', 'False', False]
