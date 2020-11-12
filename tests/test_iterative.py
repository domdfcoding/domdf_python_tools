"""
iterative
~~~~~~~~~~~~~~~

Test functions in iterative.py

"""

# stdlib
from types import GeneratorType

# 3rd party
import pytest
from pytest_regressions.data_regression import DataRegressionFixture
from pytest_regressions.file_regression import FileRegressionFixture

# this package
from domdf_python_tools.iterative import Len, chunks, double_chain, flatten, make_tree, permutations, split_len
from domdf_python_tools.testing import check_file_regression


def test_chunks():
	assert isinstance(chunks(list(range(100)), 5), GeneratorType)
	assert list(chunks(list(range(100)), 5))[0] == [0, 1, 2, 3, 4]
	assert list(chunks(['a', 'b', 'c'], 1)) == [['a'], ['b'], ['c']]


def test_permutations():
	data = ["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"]

	assert permutations(data, 1) == [(x, ) for x in data]

	assert permutations(data, 2) == [
			("egg and bacon", "egg sausage and bacon"),
			("egg and bacon", "egg and spam"),
			("egg and bacon", "egg bacon and spam"),
			("egg sausage and bacon", "egg and spam"),
			("egg sausage and bacon", "egg bacon and spam"),
			("egg and spam", "egg bacon and spam"),
			]

	assert permutations(data, 3) == [
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

	assert permutations(data, 4) == [
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

	assert permutations(data, 5) == []
	assert permutations(data, 6) == []
	assert permutations(data, 10) == []
	assert permutations(data, 30) == []
	assert permutations(data, 100) == []

	with pytest.raises(ValueError, match="'n' cannot be 0"):
		permutations(data, 0)


def test_split_len():
	assert split_len("Spam Spam Spam Spam Spam Spam Spam Spam ", 5) == ["Spam "] * 8


def test_len(capsys):
	assert list(Len("Hello")) == [0, 1, 2, 3, 4]
	assert list(Len("Hello World")) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

	for val in Len("Hello World"):
		print(val)

	captured = capsys.readouterr()
	assert captured.out.splitlines() == ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', "10"]

	assert Len("Hello") == range(5)


@pytest.mark.parametrize(
		"value, expects",
		[
				([[(1, 2), (3, 4)], [(5, 6), (7, 8)]], [1, 2, 3, 4, 5, 6, 7, 8]),
				([[(1, 2), (3, 4)], ((5, 6), (7, 8))], [1, 2, 3, 4, 5, 6, 7, 8]),
				([((1, 2), (3, 4)), [(5, 6), (7, 8)]], [1, 2, 3, 4, 5, 6, 7, 8]),
				([((1, 2), (3, 4)), ((5, 6), (7, 8))], [1, 2, 3, 4, 5, 6, 7, 8]),
				((((1, 2), (3, 4)), ((5, 6), (7, 8))), [1, 2, 3, 4, 5, 6, 7, 8]),
				((("12", "34"), ("56", "78")), ['1', '2', '3', '4', '5', '6', '7', '8']),
				]
		)
def test_double_chain(value, expects):
	assert list(double_chain(value)) == expects


def test_make_tree(file_regression: FileRegressionFixture):
	check_file_regression(
			'\n'.join(
					make_tree([
							"apeye>=0.3.0",
							[
									"appdirs>=1.4.4",
									"cachecontrol[filecache]>=0.12.6",
									[
											"requests",
											[
													"chardet<4,>=3.0.2",
													"idna<3,>=2.5",
													"urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1",
													"certifi>=2017.4.17",
													],
											"msgpack>=0.5.2",
											],
									]
							])
					),
			file_regression
			)


@pytest.mark.parametrize(
		"data",
		[
				["abc", "def", ["ghi", "jkl", ["mno", "pqr"]]],
				["abc", "def", ["ghi", "jkl", "mno", "pqr"]],
				["abc", "def", "ghi", "jkl", ["mno", "pqr"]],
				["abc", "def", "ghi", "jkl", "mno", "pqr"],
				]
		)
def test_flatten(data, data_regression: DataRegressionFixture):
	data_regression.check(list(flatten(data)))
