===========================
domdf_python_tools
===========================

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
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/domdf_python_tools/latest?logo=read-the-docs
	:target: https://domdf_python_tools.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |docs_check| image:: https://github.com/domdfcoding/domdf_python_tools/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/domdf_python_tools/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/domdf_python_tools/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/domdf_python_tools
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/domdf_python_tools/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/domdf_python_tools/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/domdf_python_tools/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/domdf_python_tools/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/domdf_python_tools/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/domdf_python_tools/requirements/?branch=master
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

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/domdf_python_tools/v0.4.4
	:target: https://github.com/domdfcoding/domdf_python_tools/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/domdf_python_tools
	:target: https://github.com/domdfcoding/domdf_python_tools/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. end shields


|

Installation
-------------

.. start installation

.. tabs::

	.. tab:: from PyPI

		.. prompt:: bash

			python3 -m pip install domdf_python_tools --user

	.. tab:: from Anaconda

		First add the required channels

		.. prompt:: bash

			conda config --add channels http://conda.anaconda.org/domdfcoding
			conda config --add channels http://conda.anaconda.org/conda-forge

		Then install

		.. prompt:: bash

			conda install domdf_python_tools

	.. tab:: from GitHub

		.. prompt:: bash

			python3 -m pip install git+https://github.com/domdfcoding/domdf_python_tools@master --user

.. end installation



.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:caption: API Reference
	:glob:

	api/*

.. toctree::
	:maxdepth: 3
	:caption: Documentation

	contributing
	Source

.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/domdf_python_tools>`__

.. end links
