=====================
domdf_python_tools
=====================

.. start short_desc

**Helpful functions for Python 🐍 🛠️**

.. end short_desc

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/domdf-python-tools/latest?logo=read-the-docs
	:target: https://domdf-python-tools.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/domdf_python_tools/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/domdf_python_tools/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/domdf_python_tools/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/domdf_python_tools/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/domdf_python_tools/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/domdf_python_tools/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/domdf_python_tools/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/domdf_python_tools/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/domdf_python_tools/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/domdf_python_tools/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/domdf_python_tools/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/domdf_python_tools/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/domdfcoding/domdf_python_tools/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/domdfcoding/domdf_python_tools/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/domdf_python_tools/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/domdf_python_tools?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/domdf_python_tools?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/domdf_python_tools
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/domdf_python_tools
	:target: https://pypi.org/project/domdf_python_tools/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/domdf_python_tools?logo=python&logoColor=white
	:target: https://pypi.org/project/domdf_python_tools/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/domdf_python_tools
	:target: https://pypi.org/project/domdf_python_tools/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/domdf_python_tools
	:target: https://pypi.org/project/domdf_python_tools/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/domdf_python_tools?logo=anaconda
	:target: https://anaconda.org/domdfcoding/domdf_python_tools
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/domdf_python_tools?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/domdf_python_tools
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/domdfcoding/domdf_python_tools
	:target: https://github.com/domdfcoding/domdf_python_tools/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/domdf_python_tools
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/domdf_python_tools/v3.7.0
	:target: https://github.com/domdfcoding/domdf_python_tools/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/domdf_python_tools
	:target: https://github.com/domdfcoding/domdf_python_tools/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2023
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/domdf_python_tools
	:target: https://pypi.org/project/domdf_python_tools/
	:alt: PyPI - Downloads

.. end shields


**Note:** Before version 3 ``domdf_python_tools`` was licensed under the LGPLv3+.
Version 3 and later are licensed under the MIT License.


.. start installation

``domdf_python_tools`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install domdf_python_tools

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install domdf_python_tools

.. end installation
