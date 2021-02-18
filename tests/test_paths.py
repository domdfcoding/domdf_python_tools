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
from pytest_regressions.data_regression import DataRegressionFixture

# this package
from domdf_python_tools import paths
from domdf_python_tools.compat import PYPY
from domdf_python_tools.paths import (
		PathPlus,
		TemporaryPathPlus,
		clean_writer,
		copytree,
		in_directory,
		matchglob,
		sort_paths,
		traverse_to_file
		)
from domdf_python_tools.testing import not_pypy, not_windows


def test_maybe_make(tmp_pathplus):
	test_dir = tmp_pathplus / "maybe_make"

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


def test_maybe_make_pathplus(tmp_pathplus):
	test_dir = tmp_pathplus / "maybe_make"

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


def test_maybe_make_string(tmp_pathplus):
	test_dir = tmp_pathplus / "maybe_make"

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


def test_maybe_make_parents(tmp_pathplus):
	test_dir = tmp_pathplus / "maybe_make" / "child1" / "child2"

	assert test_dir.exists() is False

	# Without parents=True should raise an error

	with pytest.raises(FileNotFoundError):
		paths.maybe_make(test_dir)

	# Maybe make the directory
	paths.maybe_make(test_dir, parents=True)

	assert test_dir.exists()


def test_maybe_make_parents_pathplus(tmp_pathplus):
	test_dir = tmp_pathplus / "maybe_make" / "child1" / "child2"

	assert test_dir.exists() is False

	# Without parents=True should raise an error

	with pytest.raises(FileNotFoundError):
		test_dir.maybe_make()

	# Maybe make the directory
	test_dir.maybe_make(parents=True)

	assert test_dir.exists()


def test_parent_path(tmp_pathplus):
	dir1 = tmp_pathplus / "dir1"
	dir2 = dir1 / "dir2"
	dir3 = dir2 / "dir3"

	assert paths.parent_path(dir1) == tmp_pathplus
	assert paths.parent_path(dir2) == dir1
	assert paths.parent_path(dir3) == dir2
	assert str(paths.parent_path("spam/spam/spam")) == os.path.join("spam", "spam")


@not_windows("Needs special-casing for Windows")
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


def test_clean_writer(tmp_pathplus):
	tempfile = tmp_pathplus / "tmpfile.txt"

	test_string = '\n'.join([
			"Top line",
			"    ",
			"Line with whitespace   ",
			"Line with tabs\t\t\t\t   ",
			"No newline at end of file",
			])

	with tempfile.open('w') as fp:
		clean_writer(test_string, fp)

	assert tempfile.read_text() == """Top line

Line with whitespace
Line with tabs
No newline at end of file
"""
	# Again with lots of newlines
	test_string = '\n'.join([
			"Top line",
			"    ",
			"Line with whitespace   ",
			"Line with tabs\t\t\t\t   ",
			"Too many newlines\n\n\n\n\n\n\n",
			])

	with tempfile.open('w') as fp:
		clean_writer(test_string, fp)

	assert tempfile.read_text() == """Top line

Line with whitespace
Line with tabs
Too many newlines
"""


@pytest.mark.parametrize(
		"input_string, output_string",
		[([
				"Top line",
				"    ",
				"Line with whitespace   ",
				"Line with tabs\t\t\t\t   ",
				"No newline at end of file",
				], [
						"Top line",
						'',
						"Line with whitespace",
						"Line with tabs",
						"No newline at end of file",
						'',
						]),
			([
					"Top line",
					"    ",
					"Line with whitespace   ",
					"Line with tabs\t\t\t\t   ",
					"Too many newlines\n\n\n\n\n\n\n"
					], [
							"Top line",
							'',
							"Line with whitespace",
							"Line with tabs",
							"Too many newlines",
							'',
							]), ([], [''])]
		)
def test_pathplus_write_clean(tmp_pathplus, input_string, output_string):
	tempfile = tmp_pathplus / "tmpfile.txt"

	tempfile.write_clean('\n'.join(input_string))
	assert tempfile.read_text() == '\n'.join(output_string)


@not_pypy()
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
	if os.name == "nt":
		with pytest.raises(NotImplementedError, match="cannot instantiate .* on your system"):
			paths.PosixPathPlus()
	else:
		with pytest.raises(NotImplementedError, match="cannot instantiate .* on your system"):
			paths.WindowsPathPlus()


def test_copytree(tmp_pathplus):
	srcdir = tmp_pathplus / "src"
	srcdir.mkdir()

	(srcdir / "root.txt").touch()

	(srcdir / 'a').mkdir()
	(srcdir / 'a' / "a.txt").touch()
	(srcdir / 'b').mkdir()
	(srcdir / 'b' / "b.txt").touch()
	(srcdir / 'c').mkdir()
	(srcdir / 'c' / "c.txt").touch()

	assert (srcdir / "root.txt").exists()
	assert (srcdir / "root.txt").is_file()
	assert (srcdir / 'a').exists()
	assert (srcdir / 'a').is_dir()
	assert (srcdir / 'a' / "a.txt").exists()
	assert (srcdir / 'a' / "a.txt").is_file()
	assert (srcdir / 'b').exists()
	assert (srcdir / 'b').is_dir()
	assert (srcdir / 'b' / "b.txt").exists()
	assert (srcdir / 'b' / "b.txt").is_file()
	assert (srcdir / 'c').exists()
	assert (srcdir / 'c').is_dir()
	assert (srcdir / 'c' / "c.txt").exists()
	assert (srcdir / 'c' / "c.txt").is_file()

	destdir = tmp_pathplus / "dest"
	destdir.mkdir()

	copytree(srcdir, destdir)

	assert set(os.listdir(srcdir)) == set(os.listdir(destdir))

	assert (destdir / "root.txt").exists()
	assert (destdir / "root.txt").is_file()
	assert (destdir / 'a').exists()
	assert (destdir / 'a').is_dir()
	assert (destdir / 'a' / "a.txt").exists()
	assert (destdir / 'a' / "a.txt").is_file()
	assert (destdir / 'b').exists()
	assert (destdir / 'b').is_dir()
	assert (destdir / 'b' / "b.txt").exists()
	assert (destdir / 'b' / "b.txt").is_file()
	assert (destdir / 'c').exists()
	assert (destdir / 'c').is_dir()
	assert (destdir / 'c' / "c.txt").exists()
	assert (destdir / 'c' / "c.txt").is_file()


def test_copytree_exists(tmp_pathplus):
	srcdir = tmp_pathplus / "src"
	srcdir.mkdir()

	(srcdir / "root.txt").touch()
	(srcdir / 'a').mkdir()
	(srcdir / 'a' / "a.txt").touch()
	(srcdir / 'b').mkdir()
	(srcdir / 'b' / "b.txt").touch()
	(srcdir / 'c').mkdir()
	(srcdir / 'c' / "c.txt").touch()

	assert (srcdir / "root.txt").exists()
	assert (srcdir / "root.txt").is_file()
	assert (srcdir / 'a').exists()
	assert (srcdir / 'a').is_dir()
	assert (srcdir / 'a' / "a.txt").exists()
	assert (srcdir / 'a' / "a.txt").is_file()
	assert (srcdir / 'b').exists()
	assert (srcdir / 'b').is_dir()
	assert (srcdir / 'b' / "b.txt").exists()
	assert (srcdir / 'b' / "b.txt").is_file()
	assert (srcdir / 'c').exists()
	assert (srcdir / 'c').is_dir()
	assert (srcdir / 'c' / "c.txt").exists()
	assert (srcdir / 'c' / "c.txt").is_file()

	destdir = tmp_pathplus / "dest"
	destdir.mkdir()

	copytree(srcdir, destdir)

	assert set(os.listdir(srcdir)) == set(os.listdir(destdir))

	assert (destdir / "root.txt").exists()
	assert (destdir / "root.txt").is_file()
	assert (destdir / 'a').exists()
	assert (destdir / 'a').is_dir()
	assert (destdir / 'a' / "a.txt").exists()
	assert (destdir / 'a' / "a.txt").is_file()
	assert (destdir / 'b').exists()
	assert (destdir / 'b').is_dir()
	assert (destdir / 'b' / "b.txt").exists()
	assert (destdir / 'b' / "b.txt").is_file()
	assert (destdir / 'c').exists()
	assert (destdir / 'c').is_dir()
	assert (destdir / 'c' / "c.txt").exists()
	assert (destdir / 'c' / "c.txt").is_file()


@pytest.mark.xfail(
		condition=(sys.version_info < (3, 6, 9) and platform.python_implementation() == "PyPy"),
		reason="Fails with unrelated error on PyPy 7.1.1 / 3.6.1",
		)
def test_copytree_exists_stdlib(tmp_pathplus):
	srcdir = tmp_pathplus / "src"
	srcdir.mkdir()

	(srcdir / "root.txt").touch()
	(srcdir / 'a').mkdir()
	(srcdir / 'a' / "a.txt").touch()
	(srcdir / 'b').mkdir()
	(srcdir / 'b' / "b.txt").touch()
	(srcdir / 'c').mkdir()
	(srcdir / 'c' / "c.txt").touch()

	assert (srcdir / "root.txt").exists()
	assert (srcdir / "root.txt").is_file()
	assert (srcdir / 'a').exists()
	assert (srcdir / 'a').is_dir()
	assert (srcdir / 'a' / "a.txt").exists()
	assert (srcdir / 'a' / "a.txt").is_file()
	assert (srcdir / 'b').exists()
	assert (srcdir / 'b').is_dir()
	assert (srcdir / 'b' / "b.txt").exists()
	assert (srcdir / 'b' / "b.txt").is_file()
	assert (srcdir / 'c').exists()
	assert (srcdir / 'c').is_dir()
	assert (srcdir / 'c' / "c.txt").exists()
	assert (srcdir / 'c' / "c.txt").is_file()

	destdir = tmp_pathplus / "dest"
	destdir.mkdir()

	with pytest.raises(FileExistsError, match=r".*[\\/]dest"):
		shutil.copytree(srcdir, destdir)


def test_write_lines(tmp_pathplus):
	tmp_file = tmp_pathplus / "test.txt"

	contents = [
			"this   ",
			"is",
			'a',
			"list",
			"of",
			"words",
			"to",
			"write\t\t\t",
			"to",
			"the",
			"file",
			]

	tmp_file.write_lines(contents)

	content = tmp_file.read_text()
	assert content == "this\nis\na\nlist\nof\nwords\nto\nwrite\nto\nthe\nfile\n"


def test_write_lines_trailing_whitespace(tmp_pathplus: PathPlus):
	tmp_file = tmp_pathplus / "test.txt"

	contents = [
			"this   ",
			"is",
			'a',
			"list",
			"of",
			"words",
			"to",
			"write\t\t\t",
			"to",
			"the",
			"file",
			]
	tmp_file.write_lines(contents, trailing_whitespace=True)

	content = tmp_file.read_text()
	assert content == "this   \nis\na\nlist\nof\nwords\nto\nwrite\t\t\t\nto\nthe\nfile\n"


def test_read_lines(tmp_pathplus: PathPlus):
	tmp_file = tmp_pathplus / "test.txt"

	contents = "this\nis\na\nlist\nof\nwords\nto\nwrite\nto\nthe\nfile\n"
	tmp_file.write_text(contents)

	expected = [
			"this",
			"is",
			'a',
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
	assert tmp_file.read_lines() == expected


def test_dump_json(tmpdir):
	tmpdir_p = PathPlus(tmpdir)

	tmp_file = tmpdir_p / "test.txt"

	tmp_file.dump_json({"key": "value", "int": 1234, "float": 12.34})

	assert tmp_file.read_text() == '{"key": "value", "int": 1234, "float": 12.34}\n'

	tmp_file.dump_json({"key": "value", "int": 1234, "float": 12.34}, indent=2)

	assert tmp_file.read_text() == dedent("""\
	{
	  "key": "value",
	  "int": 1234,
	  "float": 12.34
	}
""")


def test_dump_json_gzip(tmpdir):
	tmpdir_p = PathPlus(tmpdir)

	tmp_file = tmpdir_p / "test.txt"

	tmp_file.dump_json({"key": "value", "int": 1234, "float": 12.34}, compress=True)
	assert tmp_file.load_json(decompress=True) == {"key": "value", "int": 1234, "float": 12.34}

	tmp_file.dump_json({"key": "value", "int": 1234, "float": 12.34}, indent=2, compress=True)
	assert tmp_file.load_json(decompress=True) == {"key": "value", "int": 1234, "float": 12.34}


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


def test_in_directory(tmp_pathplus: PathPlus):
	cwd = os.getcwd()

	with in_directory(tmp_pathplus):
		assert str(os.getcwd()) == str(tmp_pathplus)

	assert os.getcwd() == cwd

	tmpdir = tmp_pathplus / "tmp"
	tmpdir.maybe_make()

	with in_directory(tmpdir):
		assert str(os.getcwd()) == str(tmpdir)

	assert os.getcwd() == cwd


@pytest.mark.parametrize(
		"location, expected",
		[
				("foo.yml", ''),
				("foo/foo.yml", "foo"),
				("foo/bar/foo.yml", "foo/bar"),
				("foo/bar/baz/foo.yml", "foo/bar/baz"),
				]
		)
def test_traverse_to_file(tmp_pathplus: PathPlus, location: str, expected: str):
	(tmp_pathplus / location).parent.maybe_make(parents=True)
	(tmp_pathplus / location).touch()
	assert traverse_to_file(tmp_pathplus / "foo" / "bar" / "baz", "foo.yml") == tmp_pathplus / expected


# TODO: height


def test_traverse_to_file_errors(tmp_pathplus: PathPlus):
	(tmp_pathplus / "foo/bar/baz").parent.maybe_make(parents=True)
	if os.sep == '/':
		with pytest.raises(FileNotFoundError, match="'foo.yml' not found in .*/foo/bar/baz"):
			traverse_to_file(tmp_pathplus / "foo" / "bar" / "baz", "foo.yml")
	elif os.sep == '\\':
		with pytest.raises(FileNotFoundError, match=r"'foo.yml' not found in .*\\foo\\bar\\baz"):
			traverse_to_file(tmp_pathplus / "foo" / "bar" / "baz", "foo.yml")
	else:
		raise NotImplementedError

	with pytest.raises(TypeError, match="traverse_to_file expected 2 or more arguments, got 1"):
		traverse_to_file(tmp_pathplus)


def test_iterchildren(data_regression: DataRegressionFixture):
	repo_path = PathPlus(__file__).parent.parent
	assert repo_path.is_dir()

	children = list((repo_path / "domdf_python_tools").iterchildren())
	assert children
	data_regression.check(sorted(p.relative_to(repo_path).as_posix() for p in children))


def test_iterchildren_exclusions():
	repo_path = PathPlus(__file__).parent.parent
	assert repo_path.is_dir()

	if (repo_path / "build").is_dir():
		shutil.rmtree(repo_path / "build")

	children = list(repo_path.iterchildren())
	assert children
	for directory in children:
		directory = directory.relative_to(repo_path)
		# print(directory)
		assert directory.parts[0] not in paths.unwanted_dirs


@pytest.mark.parametrize("absolute", [True, False])
def test_iterchildren_match(data_regression: DataRegressionFixture, absolute: bool):
	repo_path = PathPlus(__file__).parent.parent
	with in_directory(repo_path.parent):

		assert repo_path.is_dir()

		if not absolute:
			repo_path = repo_path.relative_to(repo_path.parent)

		if (repo_path / "build").is_dir():
			shutil.rmtree(repo_path / "build")

		children = list(repo_path.iterchildren(match="**/*.py"))
		assert children

		child_paths = sorted(p.relative_to(repo_path).as_posix() for p in children)

		for exclude_filename in {
				".coverage", "pathtype_demo.py", "dist", "htmlcov", "conda", ".idea", "mutdef.py"
				}:
			if exclude_filename in child_paths:
				child_paths.remove(exclude_filename)

		data_regression.check(child_paths, basename="test_iterchildren_match")


def test_iterchildren_no_exclusions(tmp_pathplus: PathPlus):
	(tmp_pathplus / ".git").mkdir()
	(tmp_pathplus / "venv").mkdir()
	(tmp_pathplus / ".venv").mkdir()
	(tmp_pathplus / ".tox").mkdir()
	(tmp_pathplus / ".tox4").mkdir()
	(tmp_pathplus / ".mypy_cache").mkdir()
	(tmp_pathplus / ".pytest_cache").mkdir()
	(tmp_pathplus / "normal_dir").mkdir()

	children = sorted(p.relative_to(tmp_pathplus) for p in tmp_pathplus.iterchildren(None))
	assert children == [
			PathPlus(".git"),
			PathPlus(".mypy_cache"),
			PathPlus(".pytest_cache"),
			PathPlus(".tox"),
			PathPlus(".tox4"),
			PathPlus(".venv"),
			PathPlus("normal_dir"),
			PathPlus("venv"),
			]

	children = sorted(p.relative_to(tmp_pathplus) for p in tmp_pathplus.iterchildren(()))
	assert children == [
			PathPlus(".git"),
			PathPlus(".mypy_cache"),
			PathPlus(".pytest_cache"),
			PathPlus(".tox"),
			PathPlus(".tox4"),
			PathPlus(".venv"),
			PathPlus("normal_dir"),
			PathPlus("venv"),
			]

	children = sorted(p.relative_to(tmp_pathplus) for p in tmp_pathplus.iterchildren((".git", ".tox")))
	assert children == [
			PathPlus(".mypy_cache"),
			PathPlus(".pytest_cache"),
			PathPlus(".tox4"),
			PathPlus(".venv"),
			PathPlus("normal_dir"),
			PathPlus("venv"),
			]

	children = sorted(p.relative_to(tmp_pathplus) for p in tmp_pathplus.iterchildren())
	assert children == [
			PathPlus("normal_dir"),
			]


@pytest.mark.parametrize(
		"pattern, filename, match",
		[
				("domdf_python_tools/**/", "domdf_python_tools", True),
				("domdf_python_tools/**/", "domdf_python_tools/testing/selectors.c", True),
				("domdf_python_tools/**/*.py", "domdf_python_tools/testing/selectors.c", False),
				("domdf_python_tools/**/*.py", "domdf_python_tools/foo/bar/baz.py", True),
				("domdf_python_tools/**/*.py", "domdf_python_tools/words.py", True),
				("domdf_python_tools/*.py", "domdf_python_tools/words.py", True),
				("domdf_python_tools/**/*.py", "domdf_python_tools/testing/selectors.py", True),
				("domdf_python_tools/**/*.py", "demo.py", False),
				("domdf_python_tools/*.py", "demo.py", False),
				("domdf_python_tools/[!abc].py", "domdf_python_tools/d.py", True),
				("domdf_python_tools/[!abc].py", "domdf_python_tools/a.py", False),
				("domdf_python_tools/[abc].py", "domdf_python_tools/d.py", False),
				("domdf_python_tools/[abc].py", "domdf_python_tools/a.py", True),
				("domdf_python_tools/?.py", "domdf_python_tools/a.py", True),
				("domdf_python_tools/?.py", "domdf_python_tools/Z.py", True),
				("domdf_python_tools/?.py", "domdf_python_tools/abc.py", False),
				("domdf_python_tools/Law*", "domdf_python_tools/Law", True),
				("domdf_python_tools/Law*", "domdf_python_tools/Laws", True),
				("domdf_python_tools/Law*", "domdf_python_tools/Lawyer", True),
				("domdf_python_tools/Law*", "domdf_python_tools/La", False),
				("domdf_python_tools/Law*", "domdf_python_tools/aw", False),
				("domdf_python_tools/Law*", "domdf_python_tools/GrokLaw", False),
				("domdf_python_tools/*Law*", "domdf_python_tools/Law", True),
				("domdf_python_tools/*Law*", "domdf_python_tools/Laws", True),
				("domdf_python_tools/*Law*", "domdf_python_tools/Lawyer", True),
				("domdf_python_tools/*Law*", "domdf_python_tools/La", False),
				("domdf_python_tools/*Law*", "domdf_python_tools/aw", False),
				("domdf_python_tools/*Law*", "domdf_python_tools/GrokLaw", True),
				("domdf_python_tools/?at", "domdf_python_tools/Cat", True),
				("domdf_python_tools/?at", "domdf_python_tools/cat", True),
				("domdf_python_tools/?at", "domdf_python_tools/Bat", True),
				("domdf_python_tools/?at", "domdf_python_tools/at", False),
				("domdf_python_tools/[A-Z]at", "domdf_python_tools/at", False),
				("domdf_python_tools/[A-Z]at", "domdf_python_tools/cat", False),
				("domdf_python_tools/[A-Z]at", "domdf_python_tools/Cat", True),
				("domdf_python_tools/Letter[!3-5]", "domdf_python_tools/Letter1", True),
				("domdf_python_tools/Letter[!3-5]", "domdf_python_tools/Letter6", True),
				(
						"/home/domdf/Python/01 GitHub Repos/03 Libraries/domdf_python_tools/**/*.py",
						"/home/domdf/Python/01 GitHub Repos/03 Libraries/domdf_python_tools/domdf_python_tools/pagesizes/units.py",
						True
						),
				("domdf_python_tools/**/*.py", "domdf_python_tools/domdf_python_tools/pagesizes/units.py", True),
				("**/*.py", ".pre-commit-config.yaml", False),
				("**/*.yaml", ".pre-commit-config.yaml", True),
				("./**/*.py", ".pre-commit-config.yaml", False),
				("./**/*.yaml", ".pre-commit-config.yaml", True),
				("foo/**/**/bar.py", "foo/bar.py", True),
				("foo/**/**/bar.py", "foo/baz/bar.py", True),
				("foo/**/**/bar.py", "foo/baz/baz/bar.py", True),
				("foo/**/**", "foo/", True),
				("foo/**/**", "foo/bar.py", True),
				("foo/**/**", "foo/baz/bar.py", True),
				("foo/**/**", "foo/baz/baz/bar.py", True),
				]
		)
def test_globpath(pattern: str, filename: str, match: bool):
	assert matchglob(filename, pattern) is match


pypy_no_symlink = pytest.mark.skipif(
		condition=PYPY and platform.system() == "Windows",
		reason="symlink() is not implemented for PyPy on Windows",
		)


@pypy_no_symlink
def test_abspath(tmp_pathplus: PathPlus):
	assert (tmp_pathplus / "foo" / "bar" / "baz" / "..").abspath() == tmp_pathplus / "foo" / "bar"

	file = tmp_pathplus / "foo" / "bar.py"
	file.parent.mkdir(parents=True)
	file.write_text("I'm the original")

	link = tmp_pathplus / "baz.py"
	os.symlink(file, link)

	assert link.read_text() == "I'm the original"
	assert link.is_symlink()
	assert link.resolve() == file
	assert link.abspath() == link

	file.unlink()
	file.parent.rmdir()

	assert isinstance((tmp_pathplus / "foo" / "bar" / "baz" / "..").abspath(), PathPlus)


@pypy_no_symlink
def test_abspath_dotted(tmp_pathplus: PathPlus):

	file = tmp_pathplus / "baz.py"
	file.write_text("I'm the original")

	link = tmp_pathplus / "bar" / "foo.py"
	link.parent.mkdir(parents=True)

	os.symlink(os.path.join(link.parent, "..", "baz.py"), link)

	assert link.read_text() == "I'm the original"
	assert link.is_symlink()
	assert link.resolve() == file
	assert link.abspath() == link


def test_temporarypathplus():
	with TemporaryPathPlus() as tmpdir:
		assert isinstance(tmpdir, PathPlus)
		assert tmpdir.exists()
		assert tmpdir.is_dir()

	t = TemporaryPathPlus()
	assert isinstance(t.name, PathPlus)
	assert t.name.exists()
	assert t.name.is_dir()
	t.cleanup()


def test_sort_paths():
	paths = ["foo.txt", "bar.toml", "bar.py", "baz.yaml", "fizz/buzz.c", "fizz/buzz.h"]
	expected = [
			PathPlus("fizz/buzz.c"),
			PathPlus("fizz/buzz.h"),
			PathPlus("bar.py"),
			PathPlus("bar.toml"),
			PathPlus("baz.yaml"),
			PathPlus("foo.txt"),
			]
	assert sort_paths(*paths) == expected
