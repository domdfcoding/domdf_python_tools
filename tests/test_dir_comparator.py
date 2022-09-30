#  Adapted from https://github.com/python/cpython/blob/master/Lib/test/test_filecmp.py
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#

# stdlib
import filecmp
import os
import shutil
from contextlib import redirect_stdout
from io import StringIO

# 3rd party
import pytest

# this package
from domdf_python_tools.paths import DirComparator, PathPlus, compare_dirs


class ComparatorTmpdirData:
	__slots__ = ("dir", "dir_same", "dir_diff", "dir_ignored", "caseinsensitive")
	dir: str  # noqa: A003  # pylint: disable=redefined-builtin
	dir_same: str
	dir_diff: str
	dir_ignored: str
	caseinsensitive: bool


@pytest.fixture()
def comparator_tmpdir(tmp_pathplus: PathPlus) -> ComparatorTmpdirData:
	data = ComparatorTmpdirData()
	data.dir = os.path.join(tmp_pathplus, "dir")
	data.dir_same = os.path.join(tmp_pathplus, "dir-same")
	data.dir_diff = os.path.join(tmp_pathplus, "dir-diff")

	# Another dir is created under dir_same, but it has a name from the
	# ignored list so it should not affect testing results.
	data.dir_ignored = os.path.join(data.dir_same, ".hg")

	data.caseinsensitive = os.path.normcase('A') == os.path.normcase('a')

	for dir in (data.dir, data.dir_same, data.dir_diff, data.dir_ignored):  # noqa: A001  # pylint: disable=redefined-builtin
		shutil.rmtree(dir, True)
		os.mkdir(dir)
		subdir_path = os.path.join(dir, "subdir")
		os.mkdir(subdir_path)
		if data.caseinsensitive and dir is data.dir_same:
			fn = "FiLe"  # Verify case-insensitive comparison
		else:
			fn = "file"
		with open(os.path.join(dir, fn), 'w', encoding="UTF-8") as output:
			output.write('Contents of file go here.\n')

	with open(os.path.join(data.dir_diff, "file2"), 'w', encoding="UTF-8") as output:
		output.write('An extra file.\n')

	return data


class TestDirComparator:

	def test_default_ignores(self):
		assert ".hg" in filecmp.DEFAULT_IGNORES

	# @pytest.mark.parametrize()
	def test_cmpfiles(self, comparator_tmpdir):
		assert filecmp.cmpfiles(
			comparator_tmpdir.dir,
			comparator_tmpdir.dir,
			["file"],
			) == (["file"], [], []), "Comparing directory to itself fails"
		assert filecmp.cmpfiles(
			comparator_tmpdir.dir,
			comparator_tmpdir.dir_same,
			["file"],
			) == (["file"], [], []), "Comparing directory to same fails"

		# Try it with shallow=False
		assert filecmp.cmpfiles(
			comparator_tmpdir.dir,
			comparator_tmpdir.dir,
			["file"],
			shallow=False,
			) == (["file"], [], []), "Comparing directory to itself fails"
		assert filecmp.cmpfiles(
			comparator_tmpdir.dir,
			comparator_tmpdir.dir_same,
			["file"],
			shallow=False,
			), "Comparing directory to same fails"

		# Add different file2
		with open(os.path.join(comparator_tmpdir.dir, "file2"), 'w', encoding="UTF-8") as output:
			output.write('Different contents.\n')

		assert filecmp.cmpfiles(
			comparator_tmpdir.dir,
			comparator_tmpdir.dir_same,
			["file", "file2"],
			) != (["file"], ["file2"], []), "Comparing mismatched directories fails"

	def _assert_lists(self, actual, expected):
		"""
		Assert that two lists are equal, up to ordering.
		"""

		assert sorted(actual) == sorted(expected)

	def test_dircmp(self, comparator_tmpdir):
		# Check attributes for comparison of two identical directories
		left_dir, right_dir = comparator_tmpdir.dir, comparator_tmpdir.dir_same
		d = DirComparator(left_dir, right_dir)
		assert d.left == left_dir
		assert d.right == right_dir
		if comparator_tmpdir.caseinsensitive:
			self._assert_lists(d.left_list, ["file", "subdir"])
			self._assert_lists(d.right_list, ["FiLe", "subdir"])
		else:
			self._assert_lists(d.left_list, ["file", "subdir"])
			self._assert_lists(d.right_list, ["file", "subdir"])
		self._assert_lists(d.common, ["file", "subdir"])
		self._assert_lists(d.common_dirs, ["subdir"])
		assert d.left_only == []
		assert d.right_only == []
		assert d.same_files == ["file"]
		assert d.diff_files == []
		expected_report = [
				f"diff {comparator_tmpdir.dir} {comparator_tmpdir.dir_same}",
				"Identical files : ['file']",
				"Common subdirectories : ['subdir']",
				]
		self._assert_report(d.report, expected_report)

		# Check attributes for comparison of two different directories (right)
		left_dir, right_dir = comparator_tmpdir.dir, comparator_tmpdir.dir_diff
		d = DirComparator(left_dir, right_dir)
		assert d.left == left_dir
		assert d.right == right_dir
		self._assert_lists(d.left_list, ["file", "subdir"])
		self._assert_lists(d.right_list, ["file", "file2", "subdir"])
		self._assert_lists(d.common, ["file", "subdir"])
		self._assert_lists(d.common_dirs, ["subdir"])
		assert d.left_only == []
		assert d.right_only == ["file2"]
		assert d.same_files == ["file"]
		assert d.diff_files == []
		expected_report = [
				f"diff {comparator_tmpdir.dir} {comparator_tmpdir.dir_diff}",
				f"Only in {comparator_tmpdir.dir_diff} : ['file2']",
				"Identical files : ['file']",
				"Common subdirectories : ['subdir']",
				]
		self._assert_report(d.report, expected_report)

		# Check attributes for comparison of two different directories (left)
		left_dir, right_dir = comparator_tmpdir.dir, comparator_tmpdir.dir_diff

		shutil.move(
				os.path.join(comparator_tmpdir.dir_diff, "file2"),
				os.path.join(comparator_tmpdir.dir, "file2"),
				)

		d = DirComparator(left_dir, right_dir)
		assert d.left == left_dir
		assert d.right == right_dir
		self._assert_lists(d.left_list, ["file", "file2", "subdir"])
		self._assert_lists(d.right_list, ["file", "subdir"])
		self._assert_lists(d.common, ["file", "subdir"])
		assert d.left_only == ["file2"]
		assert d.right_only == []
		assert d.same_files == ["file"]
		assert d.diff_files == []
		expected_report = [
				f"diff {comparator_tmpdir.dir} {comparator_tmpdir.dir_diff}",
				f"Only in {comparator_tmpdir.dir} : ['file2']",
				"Identical files : ['file']",
				"Common subdirectories : ['subdir']",
				]
		self._assert_report(d.report, expected_report)

		# Add different file2
		with open(os.path.join(comparator_tmpdir.dir_diff, "file2"), 'w', encoding="UTF-8") as output:
			output.write('Different contents.\n')
		d = DirComparator(comparator_tmpdir.dir, comparator_tmpdir.dir_diff)
		assert d.same_files == ["file"]
		assert d.diff_files == ["file2"]
		expected_report = [
				f"diff {comparator_tmpdir.dir} {comparator_tmpdir.dir_diff}",
				"Identical files : ['file']",
				"Differing files : ['file2']",
				"Common subdirectories : ['subdir']",
				]
		self._assert_report(d.report, expected_report)

	def test_dircmp_subdirs_type(self, comparator_tmpdir):
		"""
		Check that dircmp.subdirs respects subclassing.
		"""

		class MyDirCmp(DirComparator):
			pass

		d = MyDirCmp(comparator_tmpdir.dir, comparator_tmpdir.dir_diff)
		sub_dirs = d.subdirs
		assert list(sub_dirs.keys()) == ["subdir"]
		sub_dcmp = sub_dirs["subdir"]
		assert type(sub_dcmp) == MyDirCmp  # pylint: disable=unidiomatic-typecheck

	def test_report_partial_closure(self, comparator_tmpdir):
		left_dir, right_dir = comparator_tmpdir.dir, comparator_tmpdir.dir_same
		d = DirComparator(left_dir, right_dir)
		left_subdir = os.path.join(left_dir, "subdir")
		right_subdir = os.path.join(right_dir, "subdir")
		expected_report = [
				f"diff {comparator_tmpdir.dir} {comparator_tmpdir.dir_same}",
				"Identical files : ['file']",
				"Common subdirectories : ['subdir']",
				'',
				f"diff {left_subdir} {right_subdir}",
				]
		self._assert_report(d.report_partial_closure, expected_report)

	def test_report_full_closure(self, comparator_tmpdir):
		left_dir, right_dir = comparator_tmpdir.dir, comparator_tmpdir.dir_same
		d = DirComparator(left_dir, right_dir)
		left_subdir = os.path.join(left_dir, "subdir")
		right_subdir = os.path.join(right_dir, "subdir")
		expected_report = [
				f"diff {comparator_tmpdir.dir} {comparator_tmpdir.dir_same}",
				"Identical files : ['file']",
				"Common subdirectories : ['subdir']",
				'',
				f"diff {left_subdir} {right_subdir}",
				]
		self._assert_report(d.report_full_closure, expected_report)

	def _assert_report(self, dircmp_report, expected_report_lines):
		stdout = StringIO()
		with redirect_stdout(stdout):
			dircmp_report()
			report_lines = stdout.getvalue().strip().split('\n')
			assert report_lines == expected_report_lines


def test_compare_dirs(tmp_pathplus: PathPlus):

	dir_a = tmp_pathplus / "dir_a"
	dir_b = tmp_pathplus / "dir_b"

	dir_a.mkdir()
	dir_b.mkdir()

	(dir_a / "foo").mkdir()
	(dir_b / "foo").mkdir()

	(dir_a / "bar").mkdir()
	(dir_b / "bar").mkdir()

	(dir_a / "baz").mkdir()
	(dir_a / "baz" / "code.py").touch()

	(dir_b / "foo" / "src").mkdir()
	(dir_b / "foo" / "src" / "code.py").touch()

	assert not compare_dirs(dir_a, dir_b)
