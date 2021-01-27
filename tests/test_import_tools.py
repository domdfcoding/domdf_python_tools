# stdlib
import inspect
import sys
from contextlib import contextmanager

# 3rd party
import pytest
from pytest_regressions.data_regression import DataRegressionFixture

# this package
from domdf_python_tools.import_tools import discover, discover_entry_points, discover_entry_points_by_name

sys.path.append('.')
sys.path.append("tests")

# 3rd party
import discover_demo_module  # type: ignore  # noqa E402


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


def test_discover_entry_points(data_regression: DataRegressionFixture):
	entry_points = discover_entry_points("flake8.extension", lambda f: f.__name__.startswith("break"))
	data_regression.check([f.__name__ for f in entry_points])


def test_discover_entry_points_by_name_object_match_func(data_regression: DataRegressionFixture):
	entry_points = discover_entry_points_by_name(
			"flake8.extension", object_match_func=lambda f: f.__name__.startswith("break")
			)
	data_regression.check({k: v.__name__ for k, v in entry_points.items()})


def test_discover_entry_points_by_name_name_match_func(data_regression: DataRegressionFixture):
	entry_points = discover_entry_points_by_name(
			"flake8.extension", name_match_func=lambda n: n.startswith("pycodestyle.")
			)
	data_regression.check({k: v.__name__ for k, v in entry_points.items()})
