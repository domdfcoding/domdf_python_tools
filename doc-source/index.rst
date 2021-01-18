====================
domdf_python_tools
====================

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
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |docs| rtfd-shield::
	:project: domdf_python_tools
	:alt: Documentation Build Status

.. |docs_check| actions-shield::
	:workflow: Docs Check
	:alt: Docs Check Status

.. |actions_linux| actions-shield::
	:workflow: Linux
	:alt: Linux Test Status

.. |actions_windows| actions-shield::
	:workflow: Windows
	:alt: Windows Test Status

.. |actions_macos| actions-shield::
	:workflow: macOS
	:alt: macOS Test Status

.. |actions_flake8| actions-shield::
	:workflow: Flake8
	:alt: Flake8 Status

.. |actions_mypy| actions-shield::
	:workflow: mypy
	:alt: mypy status

.. |requires| requires-io-shield::
	:alt: Requirements Status

.. |coveralls| coveralls-shield::
	:alt: Coverage

.. |codefactor| codefactor-shield::
	:alt: CodeFactor Grade

.. |pypi-version| pypi-shield::
	:project: domdf_python_tools
	:version:
	:alt: PyPI - Package Version

.. |supported-versions| pypi-shield::
	:project: domdf_python_tools
	:py-versions:
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| pypi-shield::
	:project: domdf_python_tools
	:implementations:
	:alt: PyPI - Supported Implementations

.. |wheel| pypi-shield::
	:project: domdf_python_tools
	:wheel:
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/domdf_python_tools?logo=anaconda
	:target: https://anaconda.org/domdfcoding/domdf_python_tools
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/domdf_python_tools?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/domdf_python_tools
	:alt: Conda - Platform

.. |license| github-shield::
	:license:
	:alt: License

.. |language| github-shield::
	:top-language:
	:alt: GitHub top language

.. |commits-since| github-shield::
	:commits-since: v2.3.0
	:alt: GitHub commits since tagged version

.. |commits-latest| github-shield::
	:last-commit:
	:alt: GitHub last commit

.. |maintained| maintained-shield:: 2021
	:alt: Maintenance

.. |pypi-downloads| pypi-shield::
	:project: domdf_python_tools
	:downloads: month
	:alt: PyPI - Downloads

.. |pre_commit_ci| pre-commit-ci-shield::
	:alt: pre-commit.ci status

.. end shields


Installation
-------------

.. start installation

.. installation:: domdf_python_tools
	:pypi:
	:github:
	:anaconda:
	:conda-channels: conda-forge, domdfcoding

.. end installation


Highlights
---------------

.. api-highlights::
	:module: domdf_python_tools
	:colours: blue,green,red,orange

	.stringlist.StringList
	.testing.check_file_regression
	.paths.PathPlus
	.iterative.groupfloats
	.words.Plural


.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 1
	:caption: API Reference
	:glob:

	api/*
	api/*/index

.. toctree::
	:maxdepth: 2
	:caption: Contributing

	contributing
	Source

.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/domdf_python_tools>`__

.. end links
