#!/usr/bin/env python
#
#  __init__.py
"""
Handy functions for testing code.

.. extras-require:: testing
	:__pkginfo__:

.. versionadded:: 0.4.9

.. attention::

	:mod:`domdf_python_tools.testing` is deprecated since v2.4.0 and will be removed in v3.0.0.
	Use the new `coincidence <https://coincidence.readthedocs.io/en/latest/api/utils.html>`_ package instead,
	which has everything this module provides, and more!
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import datetime
import sys

# this package
from domdf_python_tools.testing.fixtures import fixed_datetime, original_datadir, tmp_pathplus
from domdf_python_tools.testing.params import count, testing_boolean_values, whitespace_perms
from domdf_python_tools.testing.regressions import check_file_output, check_file_regression
from domdf_python_tools.testing.selectors import (
		max_version,
		min_version,
		not_docker,
		not_macos,
		not_pypy,
		not_windows,
		only_docker,
		only_macos,
		only_pypy,
		only_version,
		only_windows,
		platform_boolean_factory
		)
from domdf_python_tools.testing.utils import (
		generate_falsy_values,
		generate_truthy_values,
		is_docker,
		whitespace,
		whitespace_perms_list,
		with_fixed_datetime
		)

__all__ = [
		"check_file_output",
		"check_file_regression",
		"count",
		"generate_falsy_values",
		"generate_truthy_values",
		"is_docker",
		"max_version",
		"min_version",
		"only_version",
		"not_windows",
		"only_windows",
		"not_pypy",
		"only_pypy",
		"not_macos",
		"only_macos",
		"not_docker",
		"only_docker",
		"pytest_report_header",
		"PEP_563",
		"original_datadir",
		"platform_boolean_factory",
		"testing_boolean_values",
		"tmp_pathplus",
		"whitespace",
		"whitespace_perms",
		"whitespace_perms_list",
		"fixed_datetime",
		"with_fixed_datetime",
		]


def pytest_report_header(config, startdir):
	"""
	Prints the start time of the pytest session.

	.. versionadded:: 1.2.0
	"""

	return f"Test session started at {datetime.datetime.now():%H:%M:%S}"


PEP_563: bool = (sys.version_info[:2] >= (3, 10))
"""
:py:obj:`True` if the current Python version implements :pep:`563` -- Postponed Evaluation of Annotations.

.. versionadded:: 1.4.2
"""
