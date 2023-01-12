"""
iterative
~~~~~~~~~~~~~~~

Test functions in iterative.py

"""

#  test_count, test_count_with_stride and pickletest
#  adapted from https://github.com/python/cpython/blob/master/Lib/test/test_itertools.py
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2021 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#

# stdlib
import pickle
import sys
from itertools import islice
from random import shuffle
from types import GeneratorType
from typing import Any, Iterable, List, Optional, Sequence, Tuple, TypeVar

# 3rd party
import pytest
from coincidence.regressions import (
		AdvancedDataRegressionFixture,
		AdvancedFileRegressionFixture,
		check_file_regression
		)

# this package
from domdf_python_tools.iterative import (
		Len,
		chunks,
		count,
		double_chain,
		extend,
		extend_with,
		extend_with_none,
		flatten,
		groupfloats,
		make_tree,
		natmax,
		natmin,
		permutations,
		ranges_from_iterable,
		split_len
		)
from domdf_python_tools.utils import trim_precision


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


def test_make_tree(advanced_file_regression: AdvancedFileRegressionFixture):
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
									],
							"domdf_python_tools==2.2.0",
							])
					),
			advanced_file_regression
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
def test_flatten(data, advanced_data_regression: AdvancedDataRegressionFixture):
	advanced_data_regression.check(list(flatten(data)))


@pytest.mark.parametrize(
		"data",
		[
				pytest.param([1, 3, 5, 7, 9], id="integers"),
				pytest.param([1.2, 3.4, 5.6, 7.8, 9.0], id="floats"),
				pytest.param(['1', '3', '5', '7', '9'], id="numerical_strings"),
				pytest.param(["1.2", "3.4", "5.6", "7.8", "9.0"], id="float strings"),
				pytest.param(["0.9", "0.12.4", '1', "2.5"], id="versions"),
				]
		)
def test_natmin(data):
	orig_data = data[:]
	for _ in range(5):
		shuffle(data)
		assert natmin(data) == orig_data[0]


@pytest.mark.parametrize(
		"data",
		[
				pytest.param([1, 3, 5, 7, 9], id="integers"),
				pytest.param([1.2, 3.4, 5.6, 7.8, 9.0], id="floats"),
				pytest.param(['1', '3', '5', '7', '9'], id="numerical_strings"),
				pytest.param(["1.2", "3.4", "5.6", "7.8", "9.0"], id="float strings"),
				pytest.param(["0.9", "0.12.4", '1', "2.5"], id="versions"),
				]
		)
def test_natmax(data):
	orig_data = data[:]
	for _ in range(5):
		shuffle(data)
		assert natmax(data) == orig_data[-1]


def test_groupfloats():
	expects: List[Tuple[float, ...]] = [(170.0, 170.05, 170.1, 170.15), (171.05, 171.1, 171.15, 171.2)]
	assert list(groupfloats([170.0, 170.05, 170.1, 170.15, 171.05, 171.1, 171.15, 171.2], step=0.05)) == expects

	expects = [(170.0, 170.05, 170.1, 170.15), (171.05, 171.1, 171.15, 171.2)]
	values = [170.0, 170.05, 170.10000000000002, 170.15, 171.05, 171.10000000000002, 171.15, 171.2]
	values = list(map(lambda v: trim_precision(v, 4), values))

	assert list(groupfloats(values, step=0.05)) == expects

	expects = [(1, 2, 3, 4, 5), (7, 8, 9, 10)]
	assert list(groupfloats([1, 2, 3, 4, 5, 7, 8, 9, 10])) == expects


def test_ranges_from_iterable():
	expects = [(170.0, 170.15), (171.05, 171.2)]
	assert list(
			ranges_from_iterable([170.0, 170.05, 170.1, 170.15, 171.05, 171.1, 171.15, 171.2], step=0.05)
			) == expects

	expects = [(1, 5), (7, 10)]
	assert list(ranges_from_iterable([1, 2, 3, 4, 5, 7, 8, 9, 10])) == expects


def _extend_param(sequence: str, expects: Any):
	return pytest.param(sequence, expects, id=sequence)


@pytest.mark.parametrize(
		"sequence, expects",
		[
				_extend_param('a', "aaaa"),
				_extend_param("ab", "abab"),
				_extend_param("abc", "abca"),
				_extend_param("abcd", "abcd"),
				_extend_param("abcde", "abcde"),
				pytest.param(('a', 'b', 'c', 'd', 'e'), "abcde", id="tuple"),
				pytest.param(['a', 'b', 'c', 'd', 'e'], "abcde", id="list"),
				]
		)
def test_extend(sequence: Sequence[str], expects: str):
	assert ''.join(extend(sequence, 4)) == expects


@pytest.mark.parametrize(
		"sequence, expects",
		[
				_extend_param('a', "azzz"),
				_extend_param("ab", "abzz"),
				_extend_param("abc", "abcz"),
				_extend_param("abcd", "abcd"),
				_extend_param("abcde", "abcde"),
				pytest.param(('a', 'b', 'c', 'd', 'e'), "abcde", id="tuple"),
				pytest.param(['a', 'b', 'c', 'd', 'e'], "abcde", id="list"),
				]
		)
def test_extend_with(sequence: Sequence[str], expects: str):
	assert ''.join(extend_with(sequence, 4, 'z')) == expects


def test_extend_with_none():
	expects = ('a', 'b', 'c', 'd', 'e', 'f', 'g', None, None, None)
	assert tuple(extend_with("abcdefg", 10, None)) == expects

	expects = ('a', 'b', 'c', 'd', 'e', 'f', 'g', None, None, None)
	assert tuple(extend_with_none("abcdefg", 10)) == expects


def test_extend_with_int():
	expects = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 0, 0, 0)
	assert tuple(extend_with("abcdefg", 10, 0)) == expects


def lzip(*args):
	return list(zip(*args))


_T = TypeVar("_T")


def take(n: Optional[int], seq: Iterable[_T]) -> List[_T]:
	"""
	Convenience function for partially consuming a long of infinite iterable
	"""

	return list(islice(seq, n))


def test_count():
	assert lzip("abc", count()) == [('a', 0), ('b', 1), ('c', 2)]
	assert lzip("abc", count(3)) == [('a', 3), ('b', 4), ('c', 5)]
	assert take(2, lzip("abc", count(3))) == [('a', 3), ('b', 4)]
	assert take(2, zip("abc", count(-1))) == [('a', -1), ('b', 0)]
	assert take(2, zip("abc", count(-3))) == [('a', -3), ('b', -2)]

	with pytest.raises(TypeError, match=r"count\(\) takes from 0 to 2 positional arguments but 3 were given"):
		count(2, 3, 4)  # type: ignore[call-arg]

	with pytest.raises(TypeError, match="a number is required"):
		count('a')  # type: ignore[type-var]

	assert take(10, count(sys.maxsize - 5)) == list(range(sys.maxsize - 5, sys.maxsize + 5))
	assert take(10, count(-sys.maxsize - 5)) == list(range(-sys.maxsize - 5, -sys.maxsize + 5))
	assert take(3, count(3.25)) == [3.25, 4.25, 5.25]
	assert take(3, count(3.25 - 4j)) == [3.25 - 4j, 4.25 - 4j, 5.25 - 4j]

	BIGINT = 1 << 1000
	assert take(3, count(BIGINT)) == [BIGINT, BIGINT + 1, BIGINT + 2]

	c = count(3)
	assert repr(c) == "count(3)"
	next(c)
	assert repr(c) == "count(4)"
	c = count(-9)
	assert repr(c) == "count(-9)"
	next(c)
	assert next(c) == -8

	assert repr(count(10.25)) == "count(10.25)"
	assert repr(count(10.0)) == "count(10.0)"
	assert type(next(count(10.0))) == float  # pylint: disable=unidiomatic-typecheck

	for i in (-sys.maxsize - 5, -sys.maxsize + 5, -10, -1, 0, 10, sys.maxsize - 5, sys.maxsize + 5):
		# Test repr
		r1 = repr(count(i))
		r2 = "count(%r)".__mod__(i)
		assert r1 == r2

	# # check copy, deepcopy, pickle
	# for value in -3, 3, sys.maxsize - 5, sys.maxsize + 5:
	# 	c = count(value)
	# 	assert next(copy.copy(c)) == value
	# 	assert next(copy.deepcopy(c)) == value
	# 	for proto in range(pickle.HIGHEST_PROTOCOL + 1):
	# 		pickletest(proto, count(value))

	# check proper internal error handling for large "step' sizes
	count(1, sys.maxsize + 5)
	sys.exc_info()


def test_count_with_stride():
	assert lzip("abc", count(2, 3)) == [('a', 2), ('b', 5), ('c', 8)]
	assert lzip("abc", count(start=2, step=3)) == [('a', 2), ('b', 5), ('c', 8)]
	assert lzip("abc", count(step=-1)) == [('a', 0), ('b', -1), ('c', -2)]

	with pytest.raises(TypeError, match="a number is required"):
		count('a', 'b')  # type: ignore[type-var]

	with pytest.raises(TypeError, match="a number is required"):
		count(5, 'b')  # type: ignore[type-var]

	assert lzip("abc", count(2, 0)) == [('a', 2), ('b', 2), ('c', 2)]
	assert lzip("abc", count(2, 1)) == [('a', 2), ('b', 3), ('c', 4)]
	assert lzip("abc", count(2, 3)) == [('a', 2), ('b', 5), ('c', 8)]
	assert take(20, count(sys.maxsize - 15, 3)) == take(20, range(sys.maxsize - 15, sys.maxsize + 100, 3))
	assert take(20, count(-sys.maxsize - 15, 3)) == take(20, range(-sys.maxsize - 15, -sys.maxsize + 100, 3))
	assert take(3, count(10, sys.maxsize + 5)) == list(range(10, 10 + 3 * (sys.maxsize + 5), sys.maxsize + 5))
	assert take(3, count(2, 1.25)) == [2, 3.25, 4.5]
	assert take(3, count(2, 3.25 - 4j)) == [2, 5.25 - 4j, 8.5 - 8j]

	BIGINT = 1 << 1000
	assert take(3, count(step=BIGINT)) == [0, BIGINT, 2 * BIGINT]
	assert repr(take(3, count(10, 2.5))) == repr([10, 12.5, 15.0])

	c = count(3, 5)
	assert repr(c) == "count(3, 5)"
	next(c)
	assert repr(c) == "count(8, 5)"
	c = count(-9, 0)
	assert repr(c) == "count(-9, 0)"
	next(c)
	assert repr(c) == "count(-9, 0)"
	c = count(-9, -3)
	assert repr(c) == "count(-9, -3)"
	next(c)
	assert repr(c) == "count(-12, -3)"
	assert repr(c) == "count(-12, -3)"

	assert repr(count(10.5, 1.25)) == "count(10.5, 1.25)"
	assert repr(count(10.5, 1)) == "count(10.5)"  # suppress step=1 when it's an int
	assert repr(count(10.5, 1.00)) == "count(10.5, 1.0)"  # do show float values like 1.0
	assert repr(count(10, 1.00)) == "count(10, 1.0)"

	c = count(10, 1.0)
	assert type(next(c)) == int  # pylint: disable=unidiomatic-typecheck
	assert type(next(c)) == float  # pylint: disable=unidiomatic-typecheck

	for i in (-sys.maxsize - 5, -sys.maxsize + 5, -10, -1, 0, 10, sys.maxsize - 5, sys.maxsize + 5):
		for j in (-sys.maxsize - 5, -sys.maxsize + 5, -10, -1, 0, 1, 10, sys.maxsize - 5, sys.maxsize + 5):
			# Test repr
			r1 = repr(count(i, j))

			if j == 1:
				r2 = ("count(%r)" % i)
			else:
				r2 = (f'count({i!r}, {j!r})')
			assert r1 == r2

			# for proto in range(pickle.HIGHEST_PROTOCOL + 1):
			# 	pickletest(proto, count(i, j))


def pickletest(protocol: int, it, stop: int = 4, take: int = 1, compare=None):
	"""
	Test that an iterator is the same after pickling, also when part-consumed
	"""

	def expand(it, i=0):
		# Recursively expand iterables, within sensible bounds
		if i > 10:
			raise RuntimeError("infinite recursion encountered")
		if isinstance(it, str):
			return it
		try:
			l = list(islice(it, stop))
		except TypeError:
			return it  # can't expand it
		return [expand(e, i + 1) for e in l]

	# Test the initial copy against the original
	dump = pickle.dumps(it, protocol)  # nosec: B301
	i2 = pickle.loads(dump)  # nosec: B301
	assert type(it) is type(i2)  # pylint: disable=unidiomatic-typecheck
	a, b = expand(it), expand(i2)
	assert a == b
	if compare:
		c = expand(compare)
		assert a == c

	# Take from the copy, and create another copy and compare them.
	i3 = pickle.loads(dump)  # nosec: B301
	took = 0
	try:
		for i in range(take):
			next(i3)
			took += 1
	except StopIteration:
		pass  # in case there is less data than 'take'

	dump = pickle.dumps(i3, protocol)  # nosec: B301
	i4 = pickle.loads(dump)  # nosec: B301
	a, b = expand(i3), expand(i4)
	assert a == b
	if compare:
		c = expand(compare[took:])
		assert a == c


def test_subclassing_count():
	CountType = type(count(1))

	with pytest.raises(
			TypeError,
			match="type 'domdf_python_tools.iterative.count' is not an acceptable base type",
			):

		class MyCount(CountType):  # type: ignore[valid-type,misc]
			pass
