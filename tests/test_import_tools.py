# stdlib
import inspect
import platform
import re
import sys
from contextlib import contextmanager

# 3rd party
import pytest
from coincidence.regressions import AdvancedDataRegressionFixture
from coincidence.selectors import not_pypy, only_pypy, only_version

# this package
from domdf_python_tools.import_tools import (
		discover,
		discover_entry_points,
		discover_entry_points_by_name,
		iter_submodules
		)

sys.path.append('.')
sys.path.append("tests")

# 3rd party
import discover_demo_module  # type: ignore  # noqa: E402


def test_discover():
	# Alphabetical order regardless of order in the module.
	assert discover(discover_demo_module) == [
			discover_demo_module.foo_in_init,
			discover_demo_module.submodule_a.bar,
			discover_demo_module.submodule_a.foo,
			discover_demo_module.submodule_b.Alice,
			discover_demo_module.submodule_b.Bob,
			]


def test_discover_function_only():
	# Alphabetical order regardless of order in the module.
	assert discover(
			discover_demo_module, match_func=inspect.isfunction
			) == [
					discover_demo_module.foo_in_init,
					discover_demo_module.submodule_a.bar,
					discover_demo_module.submodule_a.foo,
					]


def test_discover_class_only():
	# Alphabetical order regardless of order in the module.
	assert discover(
			discover_demo_module, match_func=inspect.isclass
			) == [
					discover_demo_module.submodule_b.Alice,
					discover_demo_module.submodule_b.Bob,
					]


def test_discover_hasattr():

	def match_func(obj):
		return hasattr(obj, "foo")

	assert discover(discover_demo_module, match_func=match_func) == []


class HasPath:

	__path__ = "foo"


@contextmanager
def does_not_raise():
	yield


if sys.version_info <= (3, 7):
	haspath_error = does_not_raise()
else:
	haspath_error = pytest.raises(ValueError, match="^path must be None or list of paths to look for modules in$")


def raises_attribute_error(obj, **kwargs):
	return pytest.param(
			obj,
			pytest.raises(AttributeError, match=f"^'{type(obj).__name__}' object has no attribute '__name__'$"),
			**kwargs,
			)


@pytest.mark.parametrize(
		"obj, expects",
		[
				raises_attribute_error("abc", id="string"),
				raises_attribute_error(123, id="int"),
				raises_attribute_error(12.34, id="float"),
				raises_attribute_error([1, 2, 3], id="list"),
				raises_attribute_error((1, 2, 3), id="tuple"),
				raises_attribute_error({1, 2, 3}, id="set"),
				raises_attribute_error({'a': 1, 'b': 2, 'c': 3}, id="dictionary"),
				pytest.param(HasPath, haspath_error, id="HasPath"),
				],
		)
def test_discover_errors(obj, expects):
	with expects:
		discover(obj)


def test_discover_entry_points(advanced_data_regression: AdvancedDataRegressionFixture):
	entry_points = discover_entry_points("flake8.extension", lambda f: f.__name__.startswith("break"))
	advanced_data_regression.check([f.__name__ for f in entry_points])


def test_discover_entry_points_by_name_object_match_func(advanced_data_regression: AdvancedDataRegressionFixture):
	entry_points = discover_entry_points_by_name(
			"flake8.extension", object_match_func=lambda f: f.__name__.startswith("break")
			)
	advanced_data_regression.check({k: v.__name__ for k, v in entry_points.items()})


def test_discover_entry_points_by_name_name_match_func(advanced_data_regression: AdvancedDataRegressionFixture):
	entry_points = discover_entry_points_by_name(
			"flake8.extension", name_match_func=lambda n: n.startswith("pycodestyle.")
			)
	advanced_data_regression.check({k: v.__name__ for k, v in entry_points.items()})


iter_submodules_versions = pytest.mark.parametrize(
		"version",
		[
				pytest.param(3.6, marks=only_version(3.6, reason="Output differs on Python 3.6")),
				pytest.param(
						3.7,
						marks=[
								only_version(3.7, reason="Output differs on Python 3.7"),
								not_pypy("Output differs on PyPy")
								]
						),
				pytest.param(
						"3.7-pypy",
						marks=[
								only_version(3.7, reason="Output differs on Python 3.7"),
								only_pypy("Output differs on PyPy")
								]
						),
				pytest.param(
						3.8,
						marks=[
								only_version(3.8, reason="Output differs on Python 3.8"),
								not_pypy("Output differs on PyPy 3.8")
								]
						),
				pytest.param(
						"3.8_pypy",
						marks=[
								only_version(3.8, reason="Output differs on Python 3.8"),
								only_pypy("Output differs on PyPy 3.8")
								]
						),
				pytest.param(
						3.9,
						marks=[
								only_version(3.9, reason="Output differs on Python 3.9"),
								not_pypy("Output differs on PyPy 3.9")
								]
						),
				pytest.param(
						"3.9_pypy",
						marks=[
								only_version(3.9, reason="Output differs on Python 3.9"),
								only_pypy("Output differs on PyPy 3.9")
								]
						),
				pytest.param("3.10", marks=only_version("3.10", reason="Output differs on Python 3.10")),
				]
		)


@iter_submodules_versions
@pytest.mark.parametrize(
		"module",
		["collections", "importlib", "domdf_python_tools", "consolekit", "json", "cRQefleMvm", "reprlib"],
		)
def test_iter_submodules(version, module: str, advanced_data_regression: AdvancedDataRegressionFixture):
	advanced_data_regression.check(list(iter_submodules(module)))


if sys.version_info < (3, 10):
	# From https://github.com/python/cpython/blob/main/Lib/platform.py#L1319
	# License: https://github.com/python/cpython/blob/main/LICENSE

	### freedesktop.org os-release standard
	# https://www.freedesktop.org/software/systemd/man/os-release.html

	# NAME=value with optional quotes (' or "). The regular expression is less
	# strict than shell lexer, but that's ok.
	_os_release_line = re.compile("^(?P<name>[a-zA-Z0-9_]+)=(?P<quote>[\"']?)(?P<value>.*)(?P=quote)$")
	# unescape five special characters mentioned in the standard
	_os_release_unescape = re.compile(r"\\([\\\$\"\'`])")
	# /etc takes precedence over /usr/lib
	_os_release_candidates = ("/etc/os-release", "/usr/lib/os-release")

	def freedesktop_os_release():
		"""
		Return operation system identification from freedesktop.org os-release
		"""

		errno = None
		for candidate in _os_release_candidates:
			try:
				with open(candidate, encoding="utf-8") as f:
					info = {"ID": "linux"}

					for line in f:
						mo = _os_release_line.match(line)
						if mo is not None:
							info[mo.group("name")] = _os_release_unescape.sub(r"\1", mo.group("value"))

					return info

			except OSError as e:
				errno = e.errno

		raise OSError(errno, f"Unable to read files {', '.join(_os_release_candidates)}")

else:
	freedesktop_os_release = platform.freedesktop_os_release

on_alt_linux = False

if platform.system() == "Linux":
	try:
		on_alt_linux = freedesktop_os_release()["ID"] == "altlinux"
	except OSError:
		pass


@iter_submodules_versions
@pytest.mark.parametrize(
		"platform",
		[
				pytest.param('', marks=pytest.mark.skipif(on_alt_linux, reason="Not for ALT Linux")),
				pytest.param("altlinux", marks=pytest.mark.skipif(not on_alt_linux, reason="Only for ALT Linux")),
				]
		)
def test_iter_submodules_asyncio(
		platform,
		version,
		advanced_data_regression: AdvancedDataRegressionFixture,
		):
	advanced_data_regression.check(list(iter_submodules("asyncio")))
