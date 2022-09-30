# stdlib
import copy
import pickle
import platform
import sys
from typing import Any

# 3rd party
import pytest

# this package
from domdf_python_tools.versions import Version, _iter_float, _iter_string, _prep_for_eq

pytestmark = pytest.mark.skipif(
		condition=sys.version_info[:3] <= (3, 6, 1) and platform.python_implementation() == "PyPy",
		reason="Strange bug in PyPy 7.1.1/3.6.1 on Travis when subclassing from Tuple[int, int, int]",
		)


@pytest.mark.parametrize(
		"string, expects",
		[
				('1', (1, )),
				("1.0", (1, 0)),
				("1.5", (1, 5)),
				("1.5.1", (1, 5, 1)),
				("1.5.1.2.3.4.5", (1, 5, 1, 2, 3, 4, 5)),
				("15", (15, )),
				],
		)
def test_iter_string(string, expects):
	assert tuple(_iter_string(string)) == expects


@pytest.mark.parametrize(
		"float_, expects",
		[
				(1, (1, )),
				(1.0, (1, 0)),
				(1.5, (1, 5)),
				(15, (15, )),
				('1', (1, )),
				("1.0", (1, 0)),
				("1.5", (1, 5)),
				("1.5.1", (1, 5, 1)),
				("1.5.1.2.3.4.5", (1, 5, 1, 2, 3, 4, 5)),
				("15", (15, )),
				],
		)
def test_iter_float(float_, expects):
	assert tuple(_iter_float(float_)) == expects


@pytest.mark.parametrize(
		"other, expects",
		[
				(1, (1, )),
				(1.0, (1, 0)),
				(1.5, (1, 5)),
				(15, (15, )),
				('1', (1, )),
				("1.0", (1, 0)),
				("1.5", (1, 5)),
				("1.5.1", (1, 5, 1)),
				("1.5.1.2.3.4.5", (1, 5, 1, 2, 3, 4, 5)),
				("15", (15, )),
				(('1', ), (1, )),
				(('1', '0'), (1, 0)),
				(('1', '5'), (1, 5)),
				(('1', '5', '1'), (1, 5, 1)),
				(('1', '5', '1', '2', '3', '4', '5'), (1, 5, 1, 2, 3, 4, 5)),
				(("15", ), (15, )),
				([
						'1',
						], (1, )),
				(['1', '0'], (1, 0)),
				(['1', '5'], (1, 5)),
				(['1', '5', '1'], (1, 5, 1)),
				(['1', '5', '1', '2', '3', '4', '5'], (1, 5, 1, 2, 3, 4, 5)),
				([
						"15",
						], (15, )),
				((1, ), (1, )),
				((1, 0), (1, 0)),
				((1, 5), (1, 5)),
				((1, 5, 1), (1, 5, 1)),
				((1, 5, 1, 2, 3, 4, 5), (1, 5, 1, 2, 3, 4, 5)),
				((15, ), (15, )),
				([
						1,
						], (1, )),
				([1, 0], (1, 0)),
				([1, 5], (1, 5)),
				([1, 5, 1], (1, 5, 1)),
				([1, 5, 1, 2, 3, 4, 5], (1, 5, 1, 2, 3, 4, 5)),
				([
						15,
						], (15, )),
				(Version(1, 2, 3), (1, 2, 3)),
				(Version(1, 2), (1, 2, 0)),
				(Version(1), (1, 0, 0)),
				],
		)
def test_prep_for_eq(other, expects):
	assert _prep_for_eq(other) == expects


@pytest.mark.parametrize(
		"float_, expects",
		[
				(1, Version(1)),
				(1.0, Version(1)),
				(1.1, Version(1, 1)),
				(1.5, Version(1, 5)),
				(2.0, Version(2)),
				],
		)
def test_from_float(float_, expects):
	assert Version.from_float(float_) == expects


@pytest.mark.parametrize(
		"string, expects",
		[
				('1', Version(1)),
				("1.0", Version(1)),
				("1.1", Version(1, 1)),
				("1.5", Version(1, 5)),
				("2.0", Version(2)),
				("1.0.0", Version(1)),
				("1.0.1", Version(1, 0, 1)),
				("1.1.5", Version(1, 1, 5)),
				("1.5.2", Version(1, 5, 2)),
				],
		)
def test_from_str(string, expects):
	assert Version.from_str(string) == expects


@pytest.mark.parametrize(
		"tuple_, expects",
		[
				(('1', ), Version(1)),
				(('1', '0'), Version(1, 0)),
				(('1', '5'), Version(1, 5)),
				(('1', '5', '1'), Version(1, 5, 1)),
				(("15", ), Version(15)),
				([
						'1',
						], Version(1)),
				(['1', '0'], Version(1, 0)),
				(['1', '5'], Version(1, 5)),
				(['1', '5', '1'], Version(1, 5, 1)),
				([
						"15",
						], Version(15)),
				((1, ), Version(1)),
				((1, 0), Version(1, 0)),
				((1, 5), Version(1, 5)),
				((1, 5, 1), Version(1, 5, 1)),
				((15, ), Version(15)),
				([
						1,
						], Version(1)),
				([1, 0], Version(1, 0)),
				([1, 5], Version(1, 5)),
				([1, 5, 1], Version(1, 5, 1)),
				([
						15,
						], Version(15)),
				],
		)
def test_from_tuple(tuple_, expects):
	assert Version.from_tuple(tuple_) == expects


def test_too_many_values():
	with pytest.raises(TypeError, match=".* takes from 1 to 4 positional arguments but 5 were given"):
		Version.from_str("1.2.3.4")
	with pytest.raises(TypeError, match=".* takes from 1 to 4 positional arguments but 5 were given"):
		Version(1, 2, 3, 4)  # type: ignore
	with pytest.raises(TypeError, match=".* takes from 1 to 4 positional arguments but 5 were given"):
		Version('1', '2', '3', '4')  # type: ignore
	# with pytest.raises(TypeError, match=".* takes from 1 to 4 positional arguments but 8 were given"):
	# 	Version.from_tuple(("1", "5", "1", "2", "3", "4", "5"))  # type: ignore
	# with pytest.raises(TypeError, match=".* takes from 1 to 4 positional arguments but 8 were given"):
	# 	Version.from_tuple(["1", "5", "1", "2", "3", "4", "5"])  # type: ignore
	# with pytest.raises(TypeError, match=".* takes from 1 to 4 positional arguments but 8 were given"):
	# 	Version.from_tuple((1, 5, 1, 2, 3, 4, 5))  # type: ignore
	# with pytest.raises(TypeError, match=".* takes from 1 to 4 positional arguments but 8 were given"):
	# 	Version.from_tuple([1, 5, 1, 2, 3, 4, 5])  # type: ignore


@pytest.mark.parametrize(
		"value, version",
		[
				(('1', ), Version(1)),
				(('1', '0'), Version(1, 0)),
				(('1', '5'), Version(1, 5)),
				(('1', '5', '1'), Version(1, 5, 1)),
				(("15", ), Version(15)),
				([
						'1',
						], Version(1)),
				(['1', '0'], Version(1, 0)),
				(['1', '5'], Version(1, 5)),
				(['1', '5', '1'], Version(1, 5, 1)),
				([
						"15",
						], Version(15)),
				((1, ), Version(1)),
				((1, 0), Version(1, 0)),
				((1, 5), Version(1, 5)),
				((1, 5, 1), Version(1, 5, 1)),
				((15, ), Version(15)),
				([
						1,
						], Version(1)),
				([1, 0], Version(1, 0)),
				([1, 5], Version(1, 5)),
				([1, 5, 1], Version(1, 5, 1)),
				([
						15,
						], Version(15)),
				('1', Version(1)),
				("1.0", Version(1, 0)),
				("1.5", Version(1, 5)),
				("1.5.1", Version(1, 5, 1)),
				("1.5.1.2.3.4.5", Version(1, 5, 1)),
				('1', Version(1, 2)),
				("15", Version(15)),
				(1, Version(1)),
				(1.0, Version(1, 0)),
				(1.5, Version(1, 5)),
				(15, Version(15)),
				],
		)
def test_equals(value, version):
	assert version == value
	assert value == version


@pytest.mark.parametrize(
		"value, version",
		[
				(1.2, Version(1.1)),
				(1.2, Version(1)),
				(1.2, Version(0, 9)),
				("1.2", Version(1.1)),
				("1.2", Version(1)),
				("1.2", Version(0, 9)),
				("1.1.1", Version(1.1)),
				("0.9.1", Version(0, 9)),
				((1, 2), Version(1.1)),
				((1, 2), Version(1)),
				((1, 2), Version(0, 9)),
				((1, 1, 1), Version(1.1)),
				((0, 9, 1), Version(0, 9)),
				([1, 2], Version(1.1)),
				([1, 1, 1], Version(1.1)),
				([0, 9, 1], Version(0, 9)),
				],
		)
def test_lt(value: Any, version: Version):
	assert value > version
	assert version < value


@pytest.mark.parametrize(
		"value, version",
		[
				(1.0, Version(1.1)),
				(0.9, Version(1)),
				(0.9, Version(0, 9)),
				("1.0", Version(1.1)),
				("1.0", Version(1)),
				("0.8", Version(0, 9)),
				("0.9.9", Version(1.1)),
				((1, ), Version(1.1)),
				((0, 9), Version(1)),
				((0, 8, 8), Version(0, 9)),
				([
						1,
						], Version(1.1)),
				([0, 9], Version(1)),
				([0, 8, 8], Version(0, 9)),
				],
		)
def test_gt(value, version):
	assert value < version
	assert version > value


@pytest.mark.parametrize(
		"value, version",
		[
				(1.2, Version(1.1)),
				(1.2, Version(1)),
				(1.2, Version(0, 9)),
				("1.2", Version(1.1)),
				("1.2", Version(1)),
				("1.2", Version(0, 9)),
				("1.1.1", Version(1.1)),
				("0.9.1", Version(0, 9)),
				((1, 2), Version(1.1)),
				((1, 2), Version(1)),
				((1, 2), Version(0, 9)),
				((1, 1, 1), Version(1.1)),
				((0, 9, 1), Version(0, 9)),
				([1, 2], Version(1.1)),
				([1, 1, 1], Version(1.1)),
				([0, 9, 1], Version(0, 9)),
				(('1', ), Version(1)),
				(('1', '0'), Version(1, 0)),
				(('1', '5'), Version(1, 5)),
				(('1', '5', '1'), Version(1, 5, 1)),
				(("15", ), Version(15)),
				([
						'1',
						], Version(1)),
				(['1', '0'], Version(1, 0)),
				(['1', '5'], Version(1, 5)),
				(['1', '5', '1'], Version(1, 5, 1)),
				([
						"15",
						], Version(15)),
				((1, ), Version(1)),
				((1, 0), Version(1, 0)),
				((1, 5), Version(1, 5)),
				((1, 5, 1), Version(1, 5, 1)),
				((15, ), Version(15)),
				([
						1,
						], Version(1)),
				([1, 0], Version(1, 0)),
				([1, 5], Version(1, 5)),
				([1, 5, 1], Version(1, 5, 1)),
				([
						15,
						], Version(15)),
				('1', Version(1)),
				("1.0", Version(1, 0)),
				("1.5", Version(1, 5)),
				("1.5.1", Version(1, 5, 1)),
				('1', Version(1, 2)),
				("15", Version(15)),
				(1, Version(1)),
				(1.0, Version(1, 0)),
				(1.5, Version(1, 5)),
				(15, Version(15)),
				("1.5.1.2.3.4.5", Version(1, 5, 1)),
				],
		)
def test_le(value, version):
	assert value >= version
	assert version <= value


@pytest.mark.parametrize(
		"value, version",
		[
				(1.0, Version(1.1)),
				(0.9, Version(1)),
				(0.9, Version(0, 9)),
				("1.0", Version(1.1)),
				("1.0", Version(1)),
				("0.8", Version(0, 9)),
				("0.9.9", Version(1.1)),
				((1, ), Version(1.1)),
				((0, 9), Version(1)),
				((0, 8, 8), Version(0, 9)),
				([
						1,
						], Version(1.1)),
				([0, 9], Version(1)),
				([0, 8, 8], Version(0, 9)),
				(('1', ), Version(1)),
				(('1', '0'), Version(1, 0)),
				(('1', '5'), Version(1, 5)),
				(('1', '5', '1'), Version(1, 5, 1)),
				(("15", ), Version(15)),
				([
						'1',
						], Version(1)),
				(['1', '0'], Version(1, 0)),
				(['1', '5'], Version(1, 5)),
				(['1', '5', '1'], Version(1, 5, 1)),
				([
						"15",
						], Version(15)),
				((1, ), Version(1)),
				((1, 0), Version(1, 0)),
				((1, 5), Version(1, 5)),
				((1, 5, 1), Version(1, 5, 1)),
				((15, ), Version(15)),
				([
						1,
						], Version(1)),
				([1, 0], Version(1, 0)),
				([1, 5], Version(1, 5)),
				([1, 5, 1], Version(1, 5, 1)),
				([
						15,
						], Version(15)),
				('1', Version(1)),
				("1.0", Version(1, 0)),
				("1.5", Version(1, 5)),
				("1.5.1", Version(1, 5, 1)),
				('1', Version(1, 2)),
				("15", Version(15)),
				(1, Version(1)),
				(1.0, Version(1, 0)),
				(1.5, Version(1, 5)),
				(15, Version(15)),
				("1.5.0.2.3.4.5", Version(1, 5, 1)),
				],
		)
def test_ge(value, version):
	assert value <= version
	assert version >= value


@pytest.mark.parametrize(
		"version, expects",
		[
				(Version(1), "Version(major=1, minor=0, patch=0)"),
				(Version(2), "Version(major=2, minor=0, patch=0)"),
				(Version(2, patch=3), "Version(major=2, minor=0, patch=3)"),
				(Version(2, 3), "Version(major=2, minor=3, patch=0)"),
				(Version(2, 3, 4), "Version(major=2, minor=3, patch=4)"),
				(Version(minor=3, patch=4), "Version(major=0, minor=3, patch=4)"),
				],
		)
def test_repr(version, expects):
	assert repr(version) == expects


@pytest.mark.parametrize(
		"version, expects",
		[
				(Version(1), "v1.0.0"),
				(Version(2), "v2.0.0"),
				(Version(2, patch=3), "v2.0.3"),
				(Version(2, 3), "v2.3.0"),
				(Version(2, 3, 4), "v2.3.4"),
				(Version(minor=3, patch=4), "v0.3.4"),
				],
		)
def test_str(version, expects):
	assert str(version) == expects


@pytest.mark.parametrize(
		"version, expects",
		[
				(Version(1), 1.0),
				(Version(2), 2.0),
				(Version(2, patch=3), 2.0),
				(Version(2, 3), 2.3),
				(Version(2, 3, 4), 2.3),
				(Version(minor=3, patch=4), 0.3),
				],
		)
def test_float(version, expects):
	assert float(version) == expects


@pytest.mark.parametrize(
		"version, expects",
		[
				(Version(1), 1),
				(Version(2), 2),
				(Version(2, patch=3), 2),
				(Version(2, 3), 2),
				(Version(2, 3, 4), 2),
				(Version(minor=3, patch=4), 0),
				],
		)
def test_int(version, expects):
	assert int(version) == expects


@pytest.mark.parametrize(
		"obj",
		[
				Version(1),
				Version(2),
				Version(2, patch=3),
				Version(2, 3),
				Version(2, 3, 4),
				Version(minor=3, patch=4),
				Version(1, 2, 3),
				],
		)
def test_pickle(obj):
	assert pickle.loads(pickle.dumps(obj)) == obj  # nosec: B301


@pytest.mark.parametrize(
		"obj",
		[
				Version(1),
				Version(2),
				Version(2, patch=3),
				Version(2, 3),
				Version(2, 3, 4),
				Version(minor=3, patch=4),
				Version(1, 2, 3),
				],
		)
def test_copy(obj):
	assert copy.copy(obj) == obj
