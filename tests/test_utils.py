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
from collections import namedtuple

# 3rd party
import click
import coincidence
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture

# this package
from domdf_python_tools.typing import HasHead
from domdf_python_tools.utils import (
		cmp,
		convert_indents,
		divide,
		double_repr_string,
		enquote_value,
		head,
		list2str,
		posargs2kwargs,
		printr,
		printt,
		pyversion,
		redirect_output,
		redivide,
		replace_nonprinting,
		stderr_writer,
		str2tuple,
		strtobool,
		trim_precision,
		unique_sorted
		)


def test_pyversion():
	assert isinstance(pyversion, int)


class TestList2Str:

	@pytest.mark.parametrize(
			"value, expects",
			[
					([1, 2, 3], "1,2,3"),
					(['a', 'b', 'c'], "a,b,c"),
					(['a', 'b', 1, 2], "a,b,1,2"),
					(['a', 2, pathlib.Path("foo.txt")], "a,2,foo.txt"),
					],
			)
	def test_list2str(self, value, expects):
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
	def test_list2str_semicolon(self, value, expects):
		str_representation = list2str(value, sep=';')
		assert isinstance(str_representation, str)
		assert str_representation == expects


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
	printr(obj)

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
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
	printt(obj)

	captured = capsys.readouterr()
	stdout = captured.out.split('\n')
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
	stderr_writer(obj)

	captured = capsys.readouterr()
	stderr = captured.err.split('\n')
	assert re.match(expects, stderr[0])


class TestStr2Tuple:

	@pytest.mark.parametrize(
			"value, expects",
			[
					("1,2,3", (1, 2, 3)),  # tests without spaces
					("1, 2, 3", (1, 2, 3)),  # tests with spaces
					],
			)
	def test_str2tuple(self, value, expects):
		assert isinstance(str2tuple(value), tuple)
		assert str2tuple(value) == expects

	@pytest.mark.parametrize(
			"value, expects",
			[
					("1;2;3", (1, 2, 3)),  # tests without semicolon
					("1; 2; 3", (1, 2, 3)),  # tests with semicolon
					],
			)
	def test_str2tuple_semicolon(self, value, expects):
		assert isinstance(str2tuple(value, sep=';'), tuple)
		assert str2tuple(value, sep=';') == expects


class TestStrToBool:

	@coincidence.testing_boolean_values(extra_truthy=[50, -1])
	def test_strtobool(self, boolean_string, expected_boolean):
		assert strtobool(boolean_string) == expected_boolean

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
	def test_strtobool_errors(self, obj, expects):
		with pytest.raises(expects):
			strtobool(obj)


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
	assert enquote_value(obj) == expects


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
# 		enquote_value(obj)


def test_cmp():
	assert isinstance(cmp(5, 20), int)
	assert cmp(5, 20) < 0
	assert cmp(5, 20) == -1

	assert isinstance(cmp(20, 5), int)
	assert cmp(20, 5) > 0
	assert cmp(20, 5) == 1

	assert isinstance(cmp(20, 20), int)
	assert cmp(20, 20) == 0


def demo_function(arg1, arg2, arg3):
	pass


cwd = pathlib.Path.cwd()


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
				((cwd, "wb", -1, "UTF-8"),
					pathlib.Path.open,
					None, {
							"self": cwd,
							"mode": "wb",
							"buffering": -1,
							"encoding": "UTF-8",
							}),
				(("wb", -1, "UTF-8"),
					pathlib.Path().open,
					None, {
							"mode": "wb",
							"buffering": -1,
							"encoding": "UTF-8",
							}),
				]
		)
def test_posargs2kwargs(args, posarg_names, kwargs, expects):
	assert posargs2kwargs(args, posarg_names, kwargs) == expects


def test_convert_indents():

	# TODO: test 'to'

	assert convert_indents("hello world") == "hello world"
	assert convert_indents("\thello world") == "    hello world"
	assert convert_indents("\t\thello world") == "        hello world"
	assert convert_indents("\t    hello world") == "        hello world"

	assert convert_indents("hello world", tab_width=2) == "hello world"
	assert convert_indents("\thello world", tab_width=2) == "  hello world"
	assert convert_indents("\t\thello world", tab_width=2) == "    hello world"
	assert convert_indents("\t    hello world", tab_width=2) == "      hello world"

	assert convert_indents("hello world", from_="    ") == "hello world"
	assert convert_indents("    hello world", from_="    ") == "    hello world"
	assert convert_indents("        hello world", from_="    ") == "        hello world"
	assert convert_indents("        hello world", from_="    ") == "        hello world"

	assert convert_indents("hello world", tab_width=2, from_="    ") == "hello world"
	assert convert_indents("    hello world", tab_width=2, from_="    ") == "  hello world"
	assert convert_indents("        hello world", tab_width=2, from_="    ") == "    hello world"


class TestHead:

	def test_protocol(self):
		assert not isinstance(str, HasHead)
		assert not isinstance(int, HasHead)
		assert not isinstance(float, HasHead)
		assert not isinstance(tuple, HasHead)
		assert not isinstance(list, HasHead)

	def test_protocol_pandas(self):
		pandas = pytest.importorskip("pandas")

		assert isinstance(pandas.DataFrame, HasHead)
		assert isinstance(pandas.Series, HasHead)

	foo = namedtuple("foo", "a, b, c, d, e, f, g, h, i, j, k, l, m")

	@pytest.mark.parametrize(
			"args, expects",
			[
					((foo(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), ),
						"foo(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10, ...)"),
					((foo(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), 13),
						"foo(a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, j=10, k=11, l=12, m=13)"),
					]
			)
	def test_namedtuple(self, args, expects):
		assert head(*args) == expects

	@pytest.mark.parametrize(
			"args, expects",
			[
					(((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13), ), "(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...)"),
					((
							(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13),
							13,
							),
						"(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)"),
					]
			)
	def test_tuple(self, args, expects):
		assert head(*args) == expects

	@pytest.mark.parametrize(
			"args, expects",
			[
					(([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], ), "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]"),
					((
							[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
							13,
							),
						"[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]"),
					]
			)
	def test_list(self, args, expects):
		assert head(*args) == expects

	def test_data_frame(self):
		pandas = pytest.importorskip("pandas")

		df = pandas.DataFrame(
				data=[["Bob", 20, "Apprentice"], ["Alice", 23, "Secretary"], ["Mario", 39, "Plumber"]],
				columns=["Name", "Age", "Occupation"],
				)
		assert head(
				df
				) == """    Name  Age  Occupation
0    Bob   20  Apprentice
1  Alice   23   Secretary
2  Mario   39     Plumber\
"""
		assert head(df, 1) == "  Name  Age  Occupation\n0  Bob   20  Apprentice"

	def test_series(self):
		pandas = pytest.importorskip("pandas")

		df = pandas.DataFrame(
				data=[["Bob", 20, "Apprentice"], ["Alice", 23, "Secretary"], ["Mario", 39, "Plumber"]],
				columns=["Name", "Age", "Occupation"],
				)
		ser = df.iloc[0]
		assert head(ser) == """\
Name                 Bob
Age                   20
Occupation    Apprentice\
"""
		assert head(ser, 1) == "Name    Bob"

	def test_str(self):
		assert head("Hello World") == "Hello Worl..."
		assert head("Hello World", 11) == "Hello World"
		assert head("Hello World", 5) == "Hello..."


def test_trim_precision():
	assert 170.10000000000002 != 170.1
	assert trim_precision(170.10000000000002, 1) == 170.1
	assert trim_precision(170.10000000000002, 2) == 170.1
	assert trim_precision(170.10000000000002, 3) == 170.1
	assert trim_precision(170.10000000000002, 4) == 170.1
	assert trim_precision(170.10000000000002, 5) == 170.1
	assert trim_precision(170.10000000000002) == 170.1

	assert 170.15800000000002 != 170.158
	assert trim_precision(170.15800000000002, 1) == 170.2
	assert trim_precision(170.15800000000002, 2) == 170.16
	assert trim_precision(170.15800000000002, 3) == 170.158
	assert trim_precision(170.15800000000002, 4) == 170.158
	assert trim_precision(170.15800000000002, 5) == 170.158
	assert trim_precision(170.15800000000002) == 170.158


@pytest.mark.parametrize(
		"value, expects",
		[
				("foo", '"foo"'),
				("'foo'", "\"'foo'\""),
				("don't", "\"don't\""),
				("Here's a single quote \"", "\"Here's a single quote \\\"\""),
				(enquote_value('☃'), "\"'☃'\""),
				]
		)
def test_double_repr_string(value: str, expects: str):
	assert double_repr_string(value) == expects


def test_redirect_output():
	with redirect_output() as (stdout, stderr):
		print("I'm going to stdout")
		click.echo("I'm going to stderr", file=sys.stderr)
		click.echo("I'm also going to stdout", file=stdout)
		print("I'm also going to stderr", file=stderr)

	assert stdout.getvalue() == "I'm going to stdout\nI'm also going to stdout\n"
	assert stderr.getvalue() == "I'm going to stderr\nI'm also going to stderr\n"


def test_redirect_output_combine():
	with redirect_output(combine=True) as (stdout, stderr):
		click.echo("I'm going to stdout")
		print("I'm going to stderr", file=sys.stderr)
		print("I'm also going to stdout", file=stdout)
		click.echo("I'm also going to stderr", file=stderr)

	expected = "I'm going to stdout\nI'm going to stderr\nI'm also going to stdout\nI'm also going to stderr\n"
	assert stdout.getvalue() == expected
	assert stderr.getvalue() == expected


@pytest.mark.parametrize(
		"string, sep",
		[
				("hello=world", '='),
				("hello = world", '='),
				("hello = world", " = "),
				("hello: world", ':'),
				("hello: world", ": "),
				]
		)
def test_divide(string: str, sep: str, advanced_data_regression: AdvancedDataRegressionFixture):
	data = dict(divide(e, sep) for e in [string, string, string])

	advanced_data_regression.check(data)


def test_divide_errors():
	with pytest.raises(ValueError, match="'=' not in 'hello: world'"):
		divide("hello: world", '=')


@pytest.mark.parametrize(
		"string, sep",
		[
				("hello=world", r"\s?=\s?"),
				("hello = world", r"\s?=\s?"),
				("hello = world", '='),
				("hello: world", r":\s?"),
				("hello: world", r"\s?:\s?"),
				]
		)
def test_redivide(string: str, sep: str, advanced_data_regression: AdvancedDataRegressionFixture):
	data = dict(redivide(e, sep) for e in [string, string, string])

	advanced_data_regression.check(data)


def test_redivide_errors():
	with pytest.raises(ValueError, match=r"re.compile\('='\) has no matches in 'hello: world'"):
		redivide("hello: world", '=')
	with pytest.raises(ValueError, match=r"re.compile\(.*\) has no matches in 'hello: world'"):
		redivide("hello: world", r"\d")


@pytest.mark.parametrize(
		"values, expected",
		[
				(("foo", "bar"), ["bar", "foo"]),
				(("foo", "foo", "bar"), ["bar", "foo"]),
				(("foo", "bar", "bar"), ["bar", "foo"]),
				]
		)
def test_unique_sorted(values, expected):
	assert unique_sorted(values) == expected


@pytest.mark.parametrize(
		"the_string, expected",
		[
				("\t\t\t", "^I^I^I"),
				("\u0000\u0000\u0000", "^@^@^@"),
				("\r\n", "^M^J"),
				("\b\u000b", "^H^K"),
				("\u001a", "^Z^?"),
				('\x81', "M+A"),
				]
		)
def test_replace_nonprinting(the_string: str, expected: str):
	assert replace_nonprinting(the_string) == expected
