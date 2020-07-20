"""
test_paths
~~~~~~~~~~~~~~~

Test functions in paths.py

"""

# stdlib
import contextlib
import os
import pathlib
import sys
from tempfile import TemporaryDirectory

# 3rd party
import pytest

# this package
from domdf_python_tools import paths
from domdf_python_tools.paths import clean_writer, PathPlus


# TODO: delete, write, read and append might want deprecating in favour of pathlib


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
		assert test_dir.exists() is False
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
	with TemporaryDirectory() as tmpdir:
		tmpdir = pathlib.Path(tmpdir)

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


def test_pathplus_write_clean():
	with TemporaryDirectory() as tmpdir:
		tempfile = PathPlus(tmpdir) / "tmpfile.txt"

		test_string = "\n".join([
				"Top line",
				"    ",
				"Line with whitespace   ",
				"Line with tabs				   ",
				"No newline at end of file",
				])

		with tempfile.open("w") as fp:
			tempfile.write_clean(test_string)

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
			tempfile.write_clean(test_string)

		assert tempfile.read_text() == """Top line

Line with whitespace
Line with tabs
Too many newlines
"""


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
