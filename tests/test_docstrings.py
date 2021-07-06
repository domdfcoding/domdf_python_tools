# stdlib
import doctest
import inspect
import shutil
from textwrap import indent

# 3rd party
import pytest

# this package
from domdf_python_tools import getters, iterative, pagesizes, secrets, stringlist, utils, words
from domdf_python_tools.utils import redirect_output

VERBOSE = 1

ret = 0


@pytest.mark.parametrize("module", [iterative, getters, secrets, stringlist, utils, words, pagesizes.units])
def test_docstrings(module):
	# Check that we were actually given a module.
	if inspect.ismodule(module):
		print(f"Running doctest in {module!r}".center(shutil.get_terminal_size().columns, '='))
	else:
		raise TypeError(f"testmod: module required; {module!r}")

	with redirect_output(combine=True) as (stdout, stderr):

		# Find, parse, and run all tests in the given module.
		finder = doctest.DocTestFinder()
		runner = doctest.DocTestRunner(verbose=VERBOSE >= 2)

		for test in finder.find(module, module.__name__):
			runner.run(test)

		runner.summarize(verbose=bool(VERBOSE))

	# results = doctest.TestResults(runner.failures, runner.tries)
	print(indent(stdout.getvalue(), "  "))

	if runner.failures:
		pytest.fail(msg=f"{runner.failures} tests failed")
