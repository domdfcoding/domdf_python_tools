from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	name="domdf_python_tools",
	version="0.1.1",
    author='Dominic Davis-Foster',
	author_email="dominic@davis-foster.co.uk",
	packages=find_packages(),
	license="OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
	url="https://github.com/domdfcoding/domdf_python_tools",
	description='Helpful functions for Python',
	long_description=long_description,
	long_description_content_type="text/markdown",
	classifiers=[
        "Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
		"Development Status :: 4 - Beta",
    ],

)
