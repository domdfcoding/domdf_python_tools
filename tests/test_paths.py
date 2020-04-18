# -*- coding: utf-8 -*-
"""
test_paths
~~~~~~~~~~~~~~~

Test functions in paths.py

"""

# stdlib
import pathlib
from tempfile import TemporaryDirectory

# this package
from domdf_python_tools import paths

# TODO: Still need tests for copytree, relpath, relpath2, delete, write,
#  read and append.
#  Some of those might want deprecating in favour of pathlib


def test_maybe_make():
	# TODO: test with strings as well as pathlib
	with TemporaryDirectory() as tmpdir:
		
		test_dir = pathlib.Path(tmpdir) / "maybe_make"
		
		assert test_dir.exists() is False
		
		# Maybe make the directory
		paths.maybe_make(test_dir)
		
		assert test_dir.exists()
		
		# Maybe make the directory
		paths.maybe_make(test_dir)
		
		assert test_dir.exists()
		
		# Delete the directory and replace with a file
		test_dir.rmdir()
		assert test_dir.exists() is False
		test_dir.write_text("")
		assert test_dir.exists()
		assert test_dir.is_file()
		
		paths.maybe_make(test_dir)
		assert test_dir.exists() and test_dir.is_file()
		
		
def test_parent_path():
	with TemporaryDirectory() as tmpdir:
		tmpdir = pathlib.Path(tmpdir)
		
		dir1 = tmpdir / "dir1"
		dir2 = dir1 / "dir2"
		dir3 = dir2 / "dir3"
		
		assert paths.parent_path(dir1) == tmpdir
		assert paths.parent_path(dir2) == dir1
		assert paths.parent_path(dir3) == dir2
		assert str(paths.parent_path("spam/spam/spam")) == "spam/spam"
