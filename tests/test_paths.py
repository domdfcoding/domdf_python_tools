"""
test_paths
~~~~~~~~~~~~~~~

Test functions in paths.py

"""

# stdlib
import contextlib
import pathlib
from tempfile import TemporaryDirectory

# 3rd party
import pytest  # type: ignore

# this package
from domdf_python_tools import paths

# TODO: delete, write, read and append might want deprecating in favour of pathlib


def test_maybe_make():
	# TODO: test making parents

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


@pytest.mark.parametrize(
		"relto, relpath",
		[
				("/home/username/Documents/games/chess.py", "/home/username/Documents/letter.doc"),
				("/home/username/Documents", "letter.doc"),
				(pathlib.Path("/home/username/Documents/games/chess.py"), "/home/username/Documents/letter.doc"),
				(pathlib.Path("/home/username/Documents"), "letter.doc"),
				]
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
