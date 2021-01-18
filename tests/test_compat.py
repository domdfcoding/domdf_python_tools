# this package
from domdf_python_tools.compat import nullcontext


def test_nullcontext():
	with nullcontext("foo") as f:
		assert f == "foo"

	assert f == "foo"
