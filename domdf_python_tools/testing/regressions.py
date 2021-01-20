#!/usr/bin/env python
#
#  regressions.py
"""
Regression test helpers.

.. extras-require:: testing
	:__pkginfo__:

.. versionadded:: 2.2.0
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
from typing import Optional, Union

# 3rd party
from pytest_regressions.file_regression import FileRegressionFixture  # nodep

# this package
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.stringlist import StringList
from domdf_python_tools.typing import PathLike

__all__ = ["check_file_output", "check_file_regression"]


def check_file_regression(
		data: Union[str, StringList],
		file_regression: FileRegressionFixture,
		extension: str = ".txt",
		**kwargs,
		):
	r"""
	Check the given data against that in the reference file.

	.. versionadded:: 1.5.0

	:param data:
	:param file_regression: The file regression fixture for the test.
	:param extension: The extension of the reference file.
	:param \*\*kwargs: Additional keyword arguments passed to
		:meth:`pytest_regressions.file_regression.FileRegressionFixture.check`.
	"""

	__tracebackhide__ = True

	if isinstance(data, StringList):
		data = str(data)

	file_regression.check(data, encoding="UTF-8", extension=extension, **kwargs)

	return True


def check_file_output(
		filename: PathLike,
		file_regression: FileRegressionFixture,
		extension: Optional[str] = None,
		newline: Optional[str] = '\n',
		**kwargs,
		):
	r"""
	Check the content of the given file against the reference file.

	.. versionadded:: 1.5.0

	:param filename:
	:param file_regression: The file regression fixture for the test.
	:param extension: The extension of the reference file.
		If :py:obj:`None` the extension is determined from ``filename``.
	:param newline: Controls how universal newlines mode works. See :func:`open`.
	:param \*\*kwargs: Additional keyword arguments passed to
		:meth:`pytest_regressions.file_regression.FileRegressionFixture.check`.

	.. versionchanged:: 1.7.1  Changed the default for ``newline`` to ``'\n'``.
	"""

	__tracebackhide__ = True

	filename = PathPlus(filename)

	data = filename.read_text(encoding="UTF-8")
	extension = extension or filename.suffix

	if extension == ".py":
		extension = "._py_"

	return check_file_regression(data, file_regression, extension, newline=newline, **kwargs)
