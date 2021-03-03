"""
test_typing
~~~~~~~~~~~~~~~

Test functions in typing.py

"""

# stdlib
import os
import pathlib
from typing import Dict, List, Sequence, Set, Tuple, Union

# 3rd party
import pytest

# this package
from domdf_python_tools.typing import PathLike, check_membership


@pytest.mark.parametrize(
		"obj, type_",
		[
				("abc", Union[str, int, float, bytes]),
				(1234, Union[str, int, float, bytes]),
				(12.34, Union[str, int, float, bytes]),
				(b"\x0F", Union[str, int, float, bytes]),
				("abc", List[str]),
				(1234, Sequence[int]),
				(12.34, Set[float]),
				(1234, Tuple[int, float, str]),
				(12.34, Tuple[int, float, str]),
				("abc", Tuple[int, float, str]),
				(1234, Dict[int, float]),
				(12.34, Dict[int, float]),
				],
		)
def test_check_membership_true(obj, type_):
	# todo: Positions for Tuple and Dict
	assert check_membership(obj, type_)


@pytest.mark.parametrize(
		"obj, type_",
		[
				("abc", Union[float, bytes]),
				(1234, Union[str, float, bytes]),
				(12.34, Union[str, int]),
				(b"\x0F", Union[str, int, float]),
				("abc", List[int]),
				(1234, Sequence[bytes]),
				(12.34, Set[str]),
				(1234, Tuple[str, float, bytes]),
				(12.34, Tuple[int, bytes, str]),
				("abc", Tuple[int, float, bytes]),
				(1234, Dict[bytes, float]),
				(12.34, Dict[int, str]),
				],
		)
def test_check_membership_false(obj, type_):
	# todo: Positions for Tuple and Dict
	assert not check_membership(obj, type_)


class MyPathLike(os.PathLike):

	def __init__(self, directory, filename):
		self.directory = str(directory)
		self.filename = str(filename)

	def __fspath__(self):
		os.path.join(self.directory, self.filename)


class MyStr(str):
	__slots__ = ()


class MyPath(type(pathlib.Path())):  # type: ignore
	pass


@pytest.mark.parametrize(
		"obj",
		[
				"/home/domdf/Python",
				"test_typing.py",
				pathlib.Path("/home/domdf/Python"),
				pathlib.Path("test_typing.py"),
				pathlib.PurePosixPath("test_typing.py"),
				pathlib.PureWindowsPath("test_typing.py"),
				MyPath("/home/domdf/Python"),
				MyPath("test_typing.py"),
				MyStr("/home/domdf/Python"),
				MyStr("test_typing.py"),
				MyPathLike("/home/domdf", "Python"),
				MyPathLike('.', "test_typing.py"),
				],
		)
def test_pathlike_true(obj):
	assert check_membership(obj, PathLike)


@pytest.mark.parametrize(
		"obj", [
				1234,
				12.34,
				[1, 2, 3, 4, 5],
				{1, 2, 3, 4, 5},
				(1, 2, 3, 4, 5),
				{'a': 1, 'b': 2},
				]
		)
def test_pathlike_false(obj):
	assert not check_membership(obj, PathLike)
