"""
test_paths
~~~~~~~~~~~~~~~

Test functions in paths.py

"""

# stdlib
import contextlib
import os
import pathlib
import platform
import shutil
import sys
from tempfile import TemporaryDirectory
from textwrap import dedent

# 3rd party
import pytest

# this package
from domdf_python_tools import paths
from domdf_python_tools.paths import PathPlus, clean_writer, copytree


def test_maybe_make():
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
		test_dir.touch()
		assert test_dir.exists()
		assert test_dir.is_file()

		paths.maybe_make(test_dir)
		assert test_dir.exists()
		assert test_dir.is_file()


def test_maybe_make_pathplus():
	with TemporaryDirectory() as tmpdir:
		test_dir = PathPlus(tmpdir) / "maybe_make"

		assert test_dir.exists() is False

		# Maybe make the directory
		test_dir.maybe_make()

		assert test_dir.exists()

		# Maybe make the directory
		test_dir.maybe_make()

		assert test_dir.exists()

		# Delete the directory and replace with a file
		test_dir.rmdir()
		assert test_dir.exists() is False
		test_dir.touch()
		assert test_dir.exists()
		assert test_dir.is_file()

		test_dir.maybe_make()
		assert test_dir.exists()
		assert test_dir.is_file()


def test_maybe_make_string():
	with TemporaryDirectory() as tmpdir:
		test_dir = pathlib.Path(tmpdir) / "maybe_make"

		assert test_dir.exists() is False

		# Maybe make the directory
		paths.maybe_make(str(test_dir))

		assert test_dir.exists()

		# Maybe make the directory
		paths.maybe_make(str(test_dir))

		assert test_dir.exists()

		# Delete the directory and replace with a file
		test_dir.rmdir()
		assert not test_dir.exists()
		test_dir.touch()
		assert test_dir.exists()
		assert test_dir.is_file()

		paths.maybe_make(str(test_dir))
		assert test_dir.exists()
		assert test_dir.is_file()


def test_maybe_make_parents():
	with TemporaryDirectory() as tmpdir:
		test_dir = pathlib.Path(tmpdir) / "maybe_make" / "child1" / "child2"

		assert test_dir.exists() is False

		# Without parents=True should raise an error

		with pytest.raises(FileNotFoundError):
			paths.maybe_make(test_dir)

		# Maybe make the directory
		paths.maybe_make(test_dir, parents=True)

		assert test_dir.exists()


def test_maybe_make_parents_pathplus():
	with TemporaryDirectory() as tmpdir:
		test_dir = PathPlus(tmpdir) / "maybe_make" / "child1" / "child2"

		assert test_dir.exists() is False

		# Without parents=True should raise an error

		with pytest.raises(FileNotFoundError):
			test_dir.maybe_make()

		# Maybe make the directory
		test_dir.maybe_make(parents=True)

		assert test_dir.exists()


def test_parent_path():
	with TemporaryDirectory() as tmpdir_:
		tmpdir = pathlib.Path(tmpdir_)

		dir1 = tmpdir / "dir1"
		dir2 = dir1 / "dir2"
		dir3 = dir2 / "dir3"

		assert paths.parent_path(dir1) == tmpdir
		assert paths.parent_path(dir2) == dir1
		assert paths.parent_path(dir3) == dir2
		assert str(paths.parent_path("spam/spam/spam")) == os.path.join("spam", "spam")


@pytest.mark.skipif(sys.platform == "win32", reason="Needs special-casing for Windows")
@pytest.mark.parametrize(
		"relto, relpath",
		[
				("/home/username/Documents/games/chess.py", "/home/username/Documents/letter.doc"),
				("/home/username/Documents", "letter.doc"),
				(pathlib.Path("/home/username/Documents/games/chess.py"), "/home/username/Documents/letter.doc"),
				(pathlib.Path("/home/username/Documents"), "letter.doc"),
				(None, pathlib.Path("/home/username/Documents/letter.doc")),
				],
		)
def test_relpath(relto, relpath):
	path = "/home/username/Documents/letter.doc"
	assert paths.relpath(path, relative_to=relto) == pathlib.Path(relpath)
	assert isinstance(paths.relpath(path, relative_to=relto), pathlib.Path)


class TestCurrentDirOperations:

	def test_append(self):
		file = pathlib.Path("paths_append_test_file.txt")
		file.write_text("initial content\n")
		paths.append("appended content", str(file))
		assert file.read_text() == "initial content\nappended content"
		file.unlink()

	def test_append_pathplus(self):
		file = PathPlus("paths_append_test_file.txt")
		file.write_text("initial content\n")
		file.append_text("appended content")
		assert file.read_text() == "initial content\nappended content"
		file.unlink()

	def test_delete(self):
		file = pathlib.Path("paths_delete_test_file.txt")
		file.write_text("initial content\n")
		paths.delete(str(file))
		assert not file.exists()

	def test_read(self):
		file = pathlib.Path("paths_read_test_file.txt")
		file.write_text("initial content\n")
		assert paths.read(str(file)) == "initial content\n"
		file.unlink()

	def test_write(self):
		file = pathlib.Path("paths_write_test_file.txt")
		file.write_text("initial content\n")
		paths.write("overwritten content", str(file))
		assert paths.read(str(file)) == "overwritten content"
		file.unlink()

	@classmethod
	def teardown_class(cls):
		for file in [
				"paths_append_test_file.txt",
				"paths_delete_test_file.txt",
				"paths_read_test_file.txt",
				"paths_write_test_file.txt",
				]:
			with contextlib.suppress(FileNotFoundError):
				pathlib.Path(file).unlink()


def test_clean_writer():
	with TemporaryDirectory() as tmpdir:
		tempfile = pathlib.Path(tmpdir) / "tmpfile.txt"

		test_string = "\n".join([
				"Top line",
				"    ",
				"Line with whitespace   ",
				"Line with tabs				   ",
				"No newline at end of file",
				])

		with tempfile.open("w") as fp:
			clean_writer(test_string, fp)

		assert tempfile.read_text() == """Top line

Line with whitespace
Line with tabs
No newline at end of file
"""
		# Again with lots of newlines
		test_string = "\n".join([
				"Top line",
				"    ",
				"Line with whitespace   ",
				"Line with tabs				   ",
				"Too many newlines\n\n\n\n\n\n\n",
				])

		with tempfile.open("w") as fp:
			clean_writer(test_string, fp)

		assert tempfile.read_text() == """Top line

Line with whitespace
Line with tabs
Too many newlines
"""


@pytest.mark.parametrize(
		"input_string, output_string",
		[(["Top line", "    ", "Line with whitespace   ", "Line with tabs				   ", "No newline at end of file"
			], ["Top line", '', "Line with whitespace", "Line with tabs", "No newline at end of file", ""]),
			([
					"Top line",
					"    ",
					"Line with whitespace   ",
					"Line with tabs				   ",
					"Too many newlines\n\n\n\n\n\n\n"
					], [
							"Top line",
							"",
							"Line with whitespace",
							"Line with tabs",
							"Too many newlines",
							"",
							]), ([], [''])]
		)
def test_pathplus_write_clean(input_string, output_string):
	with TemporaryDirectory() as tmpdir:
		tempfile = PathPlus(tmpdir) / "tmpfile.txt"

		tempfile.write_clean("\n".join(input_string))
		assert tempfile.read_text() == "\n".join(output_string)


@pytest.mark.xfail(reason="Unsupported on PyPy3 <7.2", condition=(platform.python_implementation() == "PyPy"))
def test_make_executable():
	with TemporaryDirectory() as tmpdir:
		tempfile = pathlib.Path(tmpdir) / "tmpfile.sh"
		tempfile.touch()

		paths.make_executable(tempfile)

		assert os.access(tempfile, os.X_OK)

	with TemporaryDirectory() as tmpdir:
		tempfile = pathlib.Path(tmpdir) / "tmpfile.sh"
		tempfile.touch()

		paths.make_executable(str(tempfile))

		assert os.access(str(tempfile), os.X_OK)

	with TemporaryDirectory() as tmpdir:
		tempfile = PathPlus(tmpdir) / "tmpfile.sh"
		tempfile.touch()

		tempfile.make_executable()

		assert os.access(tempfile, os.X_OK)


def test_instantiate_wrong_platform():
	if os.name == 'nt':
		with pytest.raises(NotImplementedError, match="cannot instantiate .* on your system"):
			paths.PosixPathPlus()
	else:
		with pytest.raises(NotImplementedError, match="cannot instantiate .* on your system"):
			paths.WindowsPathPlus()


def test_copytree():
	with TemporaryDirectory() as tmpdir:
		tmpdir_p = pathlib.Path(tmpdir)

		srcdir = tmpdir_p / "src"
		srcdir.mkdir()

		(srcdir / "root.txt").touch()
		(srcdir / "a").mkdir()
		(srcdir / "a" / "a.txt").touch()
		(srcdir / "b").mkdir()
		(srcdir / "b" / "b.txt").touch()
		(srcdir / "c").mkdir()
		(srcdir / "c" / "c.txt").touch()

		assert (srcdir / "root.txt").exists()
		assert (srcdir / "root.txt").is_file()
		assert (srcdir / "a").exists()
		assert (srcdir / "a").is_dir()
		assert (srcdir / "a" / "a.txt").exists()
		assert (srcdir / "a" / "a.txt").is_file()
		assert (srcdir / "b").exists()
		assert (srcdir / "b").is_dir()
		assert (srcdir / "b" / "b.txt").exists()
		assert (srcdir / "b" / "b.txt").is_file()
		assert (srcdir / "c").exists()
		assert (srcdir / "c").is_dir()
		assert (srcdir / "c" / "c.txt").exists()
		assert (srcdir / "c" / "c.txt").is_file()

		destdir = tmpdir_p / "dest"

		copytree(srcdir, destdir)

		assert set(os.listdir(srcdir)) == set(os.listdir(destdir))

		assert (destdir / "root.txt").exists()
		assert (destdir / "root.txt").is_file()
		assert (destdir / "a").exists()
		assert (destdir / "a").is_dir()
		assert (destdir / "a" / "a.txt").exists()
		assert (destdir / "a" / "a.txt").is_file()
		assert (destdir / "b").exists()
		assert (destdir / "b").is_dir()
		assert (destdir / "b" / "b.txt").exists()
		assert (destdir / "b" / "b.txt").is_file()
		assert (destdir / "c").exists()
		assert (destdir / "c").is_dir()
		assert (destdir / "c" / "c.txt").exists()
		assert (destdir / "c" / "c.txt").is_file()


def test_copytree_exists():
	with TemporaryDirectory() as tmpdir:
		tmpdir_p = pathlib.Path(tmpdir)

		srcdir = tmpdir_p / "src"
		srcdir.mkdir()

		(srcdir / "root.txt").touch()
		(srcdir / "a").mkdir()
		(srcdir / "a" / "a.txt").touch()
		(srcdir / "b").mkdir()
		(srcdir / "b" / "b.txt").touch()
		(srcdir / "c").mkdir()
		(srcdir / "c" / "c.txt").touch()

		assert (srcdir / "root.txt").exists()
		assert (srcdir / "root.txt").is_file()
		assert (srcdir / "a").exists()
		assert (srcdir / "a").is_dir()
		assert (srcdir / "a" / "a.txt").exists()
		assert (srcdir / "a" / "a.txt").is_file()
		assert (srcdir / "b").exists()
		assert (srcdir / "b").is_dir()
		assert (srcdir / "b" / "b.txt").exists()
		assert (srcdir / "b" / "b.txt").is_file()
		assert (srcdir / "c").exists()
		assert (srcdir / "c").is_dir()
		assert (srcdir / "c" / "c.txt").exists()
		assert (srcdir / "c" / "c.txt").is_file()

		destdir = tmpdir_p / "dest"
		destdir.mkdir()

		copytree(srcdir, destdir)

		assert set(os.listdir(srcdir)) == set(os.listdir(destdir))

		assert (destdir / "root.txt").exists()
		assert (destdir / "root.txt").is_file()
		assert (destdir / "a").exists()
		assert (destdir / "a").is_dir()
		assert (destdir / "a" / "a.txt").exists()
		assert (destdir / "a" / "a.txt").is_file()
		assert (destdir / "b").exists()
		assert (destdir / "b").is_dir()
		assert (destdir / "b" / "b.txt").exists()
		assert (destdir / "b" / "b.txt").is_file()
		assert (destdir / "c").exists()
		assert (destdir / "c").is_dir()
		assert (destdir / "c" / "c.txt").exists()
		assert (destdir / "c" / "c.txt").is_file()


@pytest.mark.xfail(
		condition=(sys.version_info < (3, 6, 9) and platform.python_implementation() == "PyPy"),
		reason="Fails with unrelated error on PyPy 7.1.1 / 3.6.1",
		)
def test_copytree_exists_stdlib():
	with TemporaryDirectory() as tmpdir:
		tmpdir_p = pathlib.Path(tmpdir)

		srcdir = tmpdir_p / "src"
		srcdir.mkdir()

		(srcdir / "root.txt").touch()
		(srcdir / "a").mkdir()
		(srcdir / "a" / "a.txt").touch()
		(srcdir / "b").mkdir()
		(srcdir / "b" / "b.txt").touch()
		(srcdir / "c").mkdir()
		(srcdir / "c" / "c.txt").touch()

		assert (srcdir / "root.txt").exists()
		assert (srcdir / "root.txt").is_file()
		assert (srcdir / "a").exists()
		assert (srcdir / "a").is_dir()
		assert (srcdir / "a" / "a.txt").exists()
		assert (srcdir / "a" / "a.txt").is_file()
		assert (srcdir / "b").exists()
		assert (srcdir / "b").is_dir()
		assert (srcdir / "b" / "b.txt").exists()
		assert (srcdir / "b" / "b.txt").is_file()
		assert (srcdir / "c").exists()
		assert (srcdir / "c").is_dir()
		assert (srcdir / "c" / "c.txt").exists()
		assert (srcdir / "c" / "c.txt").is_file()

		destdir = tmpdir_p / "dest"
		destdir.mkdir()

		with pytest.raises(FileExistsError, match=r".*[\\/]dest"):
			shutil.copytree(srcdir, destdir)


def test_write_lines():
	with TemporaryDirectory() as tmpdir:
		tmpdir_p = PathPlus(tmpdir)

		tmp_file = tmpdir_p / "test.txt"

		contents = [
				"this",
				"is",
				"a",
				"list",
				"of",
				"words",
				"to",
				"write",
				"to",
				"the",
				"file",
				]

		tmp_file.write_lines(contents)

		assert tmp_file.read_text(
		) == dedent("""\
		this
		is
		a
		list
		of
		words
		to
		write
		to
		the
		file
		""")


def test_read_lines(tmpdir):
	tmpdir_p = PathPlus(tmpdir)

	tmp_file = tmpdir_p / "test.txt"

	contents = dedent("""\
	this
	is
	a
	list
	of
	words
	to
	write
	to
	the
	file
	""")

	tmp_file.write_text(contents)

	assert tmp_file.read_lines() == [
			"this",
			"is",
			"a",
			"list",
			"of",
			"words",
			"to",
			"write",
			"to",
			"the",
			"file",
			'',
			]


def test_dump_json(tmpdir):
	tmpdir_p = PathPlus(tmpdir)

	tmp_file = tmpdir_p / "test.txt"

	tmp_file.dump_json({"key": "value", "int": 1234, "float": 12.34})

	assert tmp_file.read_text() == '{"key": "value", "int": 1234, "float": 12.34}'

	tmp_file.dump_json({"key": "value", "int": 1234, "float": 12.34}, indent=2)

	assert tmp_file.read_text() == dedent("""\
	{
	  "key": "value",
	  "int": 1234,
	  "float": 12.34
	}""")


def test_load_json(tmpdir):
	tmpdir_p = PathPlus(tmpdir)

	tmp_file = tmpdir_p / "test.txt"

	tmp_file.write_text('{"key": "value", "int": 1234, "float": 12.34}')

	assert tmp_file.load_json() == {"key": "value", "int": 1234, "float": 12.34}

	tmp_file.write_text(dedent("""\
	{
	  "key": "value",
	  "int": 1234,
	  "float": 12.34
	}"""))

	assert tmp_file.load_json() == {"key": "value", "int": 1234, "float": 12.34}
