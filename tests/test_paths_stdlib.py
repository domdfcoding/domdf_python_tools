#  Adapted from https://github.com/python/cpython/blob/master/Lib/test/test_pathlib.py
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#

# stdlib
import errno
import os
import pathlib
import pickle
import shutil
import socket
import stat
import sys
from typing import Iterator, Set
from unittest import mock

# 3rd party
import pytest

# this package
from domdf_python_tools.compat import PYPY
from domdf_python_tools.paths import PathPlus, PosixPathPlus, WindowsPathPlus

try:
	# stdlib
	import grp
	import pwd
except ImportError:
	grp = pwd = None  # type: ignore

if sys.version_info[:2] >= (3, 10):
	# stdlib
	from test.support.os_helper import TESTFN, can_symlink
else:
	# stdlib
	from test.support import TESTFN, can_symlink  # type: ignore


@pytest.fixture()
def _umask_0():
	old_mask = os.umask(0)
	try:
		yield
	finally:
		os.umask(old_mask)


only_nt = pytest.mark.skipif(condition=os.name != "nt", reason="test requires a Windows-compatible system")
only_posix = pytest.mark.skipif(condition=os.name == "nt", reason="test requires a POSIX-compatible system")


@pytest.fixture()
def BASE(tmp_pathplus: PathPlus) -> Iterator[PathPlus]:
	top_dir = tmp_pathplus
	tmp_pathplus = top_dir / "a/b/c/d"
	tmp_pathplus.maybe_make(parents=True)

	join = lambda *x: os.path.join(tmp_pathplus, *x)

	if os.name == "nt":
		# Workaround for http://bugs.python.org/issue13772.
		def dirlink(src, dest):
			os.symlink(src, dest, target_is_directory=True)
	else:

		def dirlink(src, dest):
			os.symlink(src, dest)

	os.mkdir(join("dirA"))
	os.mkdir(join("dirB"))
	os.mkdir(join("dirC"))
	os.mkdir(join("dirC", "dirD"))
	os.mkdir(join("dirE"))
	with open(join("fileA"), "wb") as f:
		f.write(b"this is file A\n")
	with open(join("dirB", "fileB"), "wb") as f:
		f.write(b"this is file B\n")
	with open(join("dirC", "fileC"), "wb") as f:
		f.write(b"this is file C\n")
	with open(join("dirC", "dirD", "fileD"), "wb") as f:
		f.write(b"this is file D\n")
	os.chmod(join("dirE"), 0)

	if not PYPY and sys.platform != "win32":
		# Relative symlinks.
		os.symlink("fileA", join("linkA"))
		os.symlink("non-existing", join("brokenLink"))
		dirlink("dirB", join("linkB"))
		dirlink(os.path.join("..", "dirB"), join("dirA", "linkC"))
		# This one goes upwards, creating a loop.
		dirlink(os.path.join("..", "dirB"), join("dirB", "linkD"))

	yield tmp_pathplus

	os.chmod(join("dirE"), 0o777)
	shutil.rmtree(top_dir)


def assertEqualNormCase(path_a, path_b):
	assert (os.path.normcase(path_a) == os.path.normcase(path_b))


if os.name == "nt":
	# Workaround for http://bugs.python.org/issue13772.
	def dirlink(src, dest):
		os.symlink(src, dest, target_is_directory=True)
else:

	def dirlink(src, dest):
		os.symlink(src, dest)


def test_stat(BASE: PathPlus):
	p = PathPlus(BASE) / "fileA"
	st = p.stat()
	assert (p.stat() == st)
	# Change file mode by flipping write bit.
	p.chmod(st.st_mode ^ 0o222)

	try:
		assert (p.stat() != st)
	finally:
		p.chmod(st.st_mode)


@pytest.mark.skipif(not hasattr(socket, "AF_UNIX"), reason="Unix sockets required")
def test_is_socket_true(BASE: PathPlus):
	P = PathPlus(BASE, "mysock")
	sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
	try:
		try:
			sock.bind(str(P))
		except OSError as e:
			if isinstance(e, PermissionError) or "AF_UNIX path too long" in str(e):
				pytest.skip("cannot bind Unix socket: " + str(e))
		assert (P.is_socket())
		assert not (P.is_fifo())
		assert not (P.is_file())
	finally:
		sock.close()


def test_cwd():
	p = PathPlus.cwd()
	q = PathPlus(os.getcwd())
	assert (p == q)
	assertEqualNormCase(str(p), str(q))
	assert (type(p) is type(q))
	assert (p.is_absolute())


def test_read_write_text(BASE: PathPlus):
	p = PathPlus(BASE)
	(p / "fileA").write_text("äbcdefg", encoding="latin-1")
	assert ((p / "fileA").read_text(encoding="utf-8", errors="ignore") == "bcdefg")
	# Check that trying to write bytes does not truncate the file.
	with pytest.raises(TypeError):
		(p / "fileA").write_text(b"somebytes")  # type: ignore
	assert ((p / "fileA").read_text(encoding="latin-1") == "äbcdefg")


def test_with(BASE: PathPlus):
	p = PathPlus(BASE)
	it = p.iterdir()
	it2 = p.iterdir()
	next(it2)
	with p:
		pass

	# Using a path as a context manager is a no-op, thus the following
	# operations should still succeed after the context manage exits.
	next(it)
	next(it2)
	p.exists()
	p.resolve()
	p.absolute()
	with p:
		pass


def test_chmod(BASE: PathPlus):
	p = PathPlus(BASE) / "fileA"
	mode = p.stat().st_mode
	# Clear writable bit.
	new_mode = mode & ~0o222
	p.chmod(new_mode)
	assert (p.stat().st_mode == new_mode)
	# Set writable bit.
	new_mode = mode | 0o222
	p.chmod(new_mode)
	assert (p.stat().st_mode == new_mode)


def test_lstat_nosymlink(BASE: PathPlus):
	p = PathPlus(BASE) / "fileA"
	st = p.stat()
	assert (st == p.lstat())


def test_owner(BASE: PathPlus):
	pwd = pytest.importorskip("pwd", reason="the pwd module is needed for this test")

	if sys.platform == "win32":
		return

	p = PathPlus(BASE) / "fileA"
	uid = p.stat().st_uid
	try:
		name = pwd.getpwuid(uid).pw_name
	except KeyError:
		pytest.skip(f"user {uid:d} doesn't have an entry in the system database")
	assert (name == p.owner())


def test_group(BASE: PathPlus):
	grp = pytest.importorskip("grp", reason="the grp module is needed for this test")

	if sys.platform == "win32":
		return

	p = PathPlus(BASE) / "fileA"
	gid = p.stat().st_gid
	try:
		name = grp.getgrgid(gid).gr_name
	except KeyError:
		pytest.skip(f"group {gid:d} doesn't have an entry in the system database")
	assert (name == p.group())


def test_unlink(BASE: PathPlus):
	p = PathPlus(BASE) / "fileA"
	p.unlink()
	with pytest.raises(FileNotFoundError):
		p.stat()
	with pytest.raises(FileNotFoundError):
		p.unlink()


def test_unlink_missing_ok(BASE: PathPlus):
	p = PathPlus(BASE) / "fileAAA"
	with pytest.raises(FileNotFoundError):
		p.unlink()
	p.unlink(missing_ok=True)


def test_rmdir(BASE: PathPlus):
	p = PathPlus(BASE) / "dirA"
	for q in p.iterdir():
		q.unlink()
	p.rmdir()
	with pytest.raises(FileNotFoundError):
		p.stat()
	with pytest.raises(FileNotFoundError):
		p.unlink()


@pytest.mark.skipif(hasattr(os, "link"), reason="os.link() is present")
def test_link_to_not_implemented(BASE: PathPlus):
	P = PathPlus(BASE) / TESTFN
	p = P / "fileA"
	# linking to another path.
	q = P / "dirA" / "fileAA"
	with pytest.raises(NotImplementedError):
		p.link_to(q)


def test_rename(BASE, tmp_pathplus: PathPlus):
	P = PathPlus(BASE)
	p = P / "fileA"
	size = p.stat().st_size
	# Renaming to another path.
	q = P / "dirA" / "fileAA"

	if sys.version_info < (3, 9):  # pragma: no cover (>=py39)
		p.replace(q)

	else:  # pragma: no cover (<py39)
		renamed_p = p.replace(q)
		assert (renamed_p == q)

	assert (q.stat().st_size == size)
	with pytest.raises(FileNotFoundError):
		p.stat()

	# Renaming to a str of a relative path.
	r = tmp_pathplus / "fileAAA"

	if sys.version_info < (3, 9):  # pragma: no cover (>=py39)
		q.replace(r)

	else:  # pragma: no cover (<py39)
		renamed_q = q.replace(r)
		assert (renamed_q == PathPlus(r))

	assert (os.stat(r).st_size == size)
	with pytest.raises(FileNotFoundError):
		q.stat()


def test_touch_common(BASE: PathPlus):
	P = PathPlus(BASE)
	p = P / "newfileA"
	assert not (p.exists())
	p.touch()
	assert (p.exists())


def test_touch_nochange(BASE: PathPlus):
	P = PathPlus(BASE)
	p = P / "fileA"
	p.touch()
	with p.open("rb") as f:
		assert (f.read().strip() == b"this is file A")


def test_mkdir(BASE: PathPlus):
	P = PathPlus(BASE)
	p = P / "newdirA"
	assert not (p.exists())
	p.mkdir()
	assert (p.exists())
	assert (p.is_dir())
	with pytest.raises(OSError) as cm:
		p.mkdir()
	assert (cm.value.errno == errno.EEXIST)


def test_mkdir_parents(BASE: PathPlus):
	# Creating a chain of directories.
	p = PathPlus(BASE, "newdirB", "newdirC")
	assert not (p.exists())
	with pytest.raises(OSError) as cm:
		p.mkdir()
	assert (cm.value.errno == errno.ENOENT)
	p.mkdir(parents=True)
	assert (p.exists())
	assert (p.is_dir())
	with pytest.raises(OSError) as cm:
		p.mkdir(parents=True)
	assert (cm.value.errno == errno.EEXIST)
	# Test `mode` arg.
	mode = stat.S_IMODE(p.stat().st_mode)  # Default mode.
	p = PathPlus(BASE, "newdirD", "newdirE")
	p.mkdir(0o555, parents=True)
	assert (p.exists())
	assert (p.is_dir())
	if os.name != "nt":
		# The directory's permissions follow the mode argument.
		assert (stat.S_IMODE(p.stat().st_mode) == 0o7555 & mode)
	# The parent's permissions follow the default process settings.
	assert (stat.S_IMODE(p.parent.stat().st_mode) == mode)


def test_mkdir_exist_ok(BASE: PathPlus):
	p = PathPlus(BASE, "dirB")
	st_ctime_first = p.stat().st_ctime
	assert (p.exists())
	assert (p.is_dir())
	with pytest.raises(FileExistsError) as cm:
		p.mkdir()
	assert (cm.value.errno == errno.EEXIST)
	p.mkdir(exist_ok=True)
	assert (p.exists())
	assert (p.stat().st_ctime == st_ctime_first)


def test_mkdir_exist_ok_with_parent(BASE: PathPlus):
	p = PathPlus(BASE, "dirC")
	assert p.exists()
	with pytest.raises(FileExistsError) as cm:
		p.mkdir()
	assert (cm.value.errno == errno.EEXIST)
	p = p / "newdirC"
	p.mkdir(parents=True)
	st_ctime_first = p.stat().st_ctime
	assert p.exists()
	with pytest.raises(FileExistsError) as cm:
		p.mkdir(parents=True)
	assert (cm.value.errno == errno.EEXIST)
	p.mkdir(parents=True, exist_ok=True)
	assert p.exists()
	assert (p.stat().st_ctime == st_ctime_first)


def test_mkdir_exist_ok_root():
	# Issue #25803: A drive root could raise PermissionError on Windows.
	PathPlus('/').resolve().mkdir(exist_ok=True)
	PathPlus('/').resolve().mkdir(parents=True, exist_ok=True)


@only_nt
def test_mkdir_with_unknown_drive():
	for d in "ZYXWVUTSRQPONMLKJIHGFEDCBA":
		p = PathPlus(d + ":\\")
		if not p.is_dir():
			break
	else:
		pytest.skip("cannot find a drive that doesn't exist")
	with pytest.raises(OSError):
		(p / "child" / "path").mkdir(parents=True)


def test_mkdir_with_child_file(BASE: PathPlus):
	p = PathPlus(BASE, "dirB", "fileB")
	assert p.exists()
	# An exception is raised when the last path component is an existing
	# regular file, regardless of whether exist_ok is true or not.
	with pytest.raises(FileExistsError) as exc_info:
		p.mkdir(parents=True)
	assert exc_info.value.errno == errno.EEXIST
	with pytest.raises(FileExistsError) as exc_info:
		p.mkdir(parents=True, exist_ok=True)
	assert exc_info.value.errno == errno.EEXIST


def test_mkdir_no_parents_file(BASE: PathPlus):
	p = PathPlus(BASE, "fileA")
	assert p.exists()
	# An exception is raised when the last path component is an existing
	# regular file, regardless of whether exist_ok is true or not.
	with pytest.raises(FileExistsError) as exc_info:
		p.mkdir()
	assert exc_info.value.errno == errno.EEXIST
	with pytest.raises(FileExistsError) as exc_info:
		p.mkdir(exist_ok=True)
	assert exc_info.value.errno == errno.EEXIST


def test_mkdir_concurrent_parent_creation(BASE: PathPlus):
	for pattern_num in range(32):
		p = PathPlus(BASE, "dirCPC%d" % pattern_num)
		assert not (p.exists())

		real_mkdir = os.mkdir

		def my_mkdir(path, mode=0o777):
			path = str(path)
			# Emulate another process that would create the directory
			# just before we try to create it ourselves.  We do it
			# in all possible pattern combinations, assuming that this
			# function is called at most 5 times (dirCPC/dir1/dir2,
			# dirCPC/dir1, dirCPC, dirCPC/dir1, dirCPC/dir1/dir2).
			if pattern.pop():
				real_mkdir(path, mode)  # From another process.
				concurrently_created.add(path)
			real_mkdir(path, mode)  # Our real call.

		pattern = [bool(pattern_num & (1 << n)) for n in range(5)]
		concurrently_created: Set = set()
		p12 = p / "dir1" / "dir2"
		try:
			if sys.version_info > (3, 11):
				cm = mock.patch("os.mkdir", my_mkdir)
			else:
				cm = mock.patch("pathlib._normal_accessor.mkdir", my_mkdir)
			with cm:
				p12.mkdir(parents=True, exist_ok=False)
		except FileExistsError:
			assert (str(p12) in concurrently_created)
		else:
			assert (str(p12) not in concurrently_created)
		assert (p.exists())


@pytest.mark.skipif(
		PYPY and sys.platform == "win32",
		reason="symlink() is not implemented for PyPy on Windows",
		)
def test_symlink_to(BASE: PathPlus):
	P = PathPlus(BASE)
	target = P / "fileA"
	# Symlinking a path target.
	link = P / "dirA" / "linkAA"
	link.symlink_to(target)
	assert link.stat() == target.stat()
	assert link.lstat() != target.stat()
	# Symlinking a str target.
	link = P / "dirA" / "linkAAA"
	link.symlink_to(str(target))
	assert link.stat() == target.stat()
	assert link.lstat() != target.stat()
	assert not link.is_dir()
	# Symlinking to a directory.
	target = P / "dirB"
	link = P / "dirA" / "linkAAAA"
	link.symlink_to(target, target_is_directory=True)
	assert link.stat() == target.stat()
	assert link.lstat() != target.stat()
	assert (link.is_dir())
	assert (list(link.iterdir()))


def test_is_dir(BASE: PathPlus):
	P = PathPlus(BASE)
	assert ((P / "dirA").is_dir())
	assert not ((P / "fileA").is_dir())
	assert not ((P / "non-existing").is_dir())
	assert not ((P / "fileA" / "bah").is_dir())

	if not PYPY and sys.platform != "win32":
		assert not ((P / "linkA").is_dir())
		assert ((P / "linkB").is_dir())
		assert not (P / "brokenLink").is_dir()


def test_is_file(BASE: PathPlus):
	P = PathPlus(BASE)
	assert ((P / "fileA").is_file())
	assert not ((P / "dirA").is_file())
	assert not ((P / "non-existing").is_file())
	assert not ((P / "fileA" / "bah").is_file())

	if not PYPY and sys.platform != "win32":
		assert ((P / "linkA").is_file())
		assert not ((P / "linkB").is_file())
		assert not ((P / "brokenLink").is_file())


@only_posix
def test_is_mount(BASE: PathPlus):
	P = PathPlus(BASE)
	R = PathPlus('/')  # TODO: Work out Windows.
	assert not ((P / "fileA").is_mount())
	assert not ((P / "dirA").is_mount())
	assert not ((P / "non-existing").is_mount())
	assert not ((P / "fileA" / "bah").is_mount())
	assert (R.is_mount())
	if can_symlink():
		assert not ((P / "linkA").is_mount())


def test_is_symlink(BASE: PathPlus):
	P = PathPlus(BASE)
	assert not ((P / "fileA").is_symlink())
	assert not ((P / "dirA").is_symlink())
	assert not ((P / "non-existing").is_symlink())
	assert not ((P / "fileA" / "bah").is_symlink())

	if not PYPY and sys.platform != "win32":
		assert ((P / "linkA").is_symlink())
		assert ((P / "linkB").is_symlink())
		assert ((P / "brokenLink").is_symlink())


def test_is_fifo_false(BASE: PathPlus):
	P = PathPlus(BASE)
	assert not ((P / "fileA").is_fifo())
	assert not ((P / "dirA").is_fifo())
	assert not ((P / "non-existing").is_fifo())
	assert not ((P / "fileA" / "bah").is_fifo())


def test_is_socket_false(BASE: PathPlus):
	P = PathPlus(BASE)
	assert not (P / "fileA").is_socket()
	assert not (P / "dirA").is_socket()
	assert not (P / "non-existing").is_socket()
	assert not (P / "fileA" / "bah").is_socket()


def test_is_block_device_false(tmp_pathplus: PathPlus):
	P = tmp_pathplus.resolve() / TESTFN
	assert not (P / "fileA").is_block_device()
	assert not (P / "dirA").is_block_device()
	assert not (P / "non-existing").is_block_device()
	assert not (P / "fileA" / "bah").is_block_device()


def test_is_char_device_false(tmp_pathplus: PathPlus):
	P = tmp_pathplus.resolve() / TESTFN
	assert not (P / "fileA").is_char_device()
	assert not (P / "dirA").is_char_device()
	assert not (P / "non-existing").is_char_device()
	assert not (P / "fileA" / "bah").is_char_device()


def test_is_char_device_true():
	# Under Unix, /dev/null should generally be a char device.
	P = PathPlus("/dev/null")
	if not P.exists():
		pytest.skip("/dev/null required")
	assert P.is_char_device()
	assert not P.is_block_device()
	assert not P.is_file()


def test_pickling_common(BASE: PathPlus):
	p = PathPlus(BASE, "fileA")
	for proto in range(0, pickle.HIGHEST_PROTOCOL + 1):
		dumped = pickle.dumps(p, proto)
		pp = pickle.loads(dumped)
		assert pp.stat() == p.stat()


def test_concrete_class():
	p = PathPlus('a')
	if os.name == "nt":
		assert type(p) is WindowsPathPlus  # pylint: disable=unidiomatic-typecheck
	else:
		assert type(p) is PosixPathPlus  # pylint: disable=unidiomatic-typecheck


def test_unsupported_flavour():
	if os.name == "nt":
		with pytest.raises(NotImplementedError):
			pathlib.PosixPath()
	else:
		with pytest.raises(NotImplementedError):
			pathlib.WindowsPath()


def test_glob_empty_pattern(tmp_pathplus: PathPlus):
	p = tmp_pathplus
	with pytest.raises(ValueError, match="Unacceptable pattern"):
		list(p.glob(''))


@pytest.mark.usefixtures("_umask_0")
@only_posix
def test_open_mode(BASE: PathPlus):

	p = PathPlus(BASE)
	with (p / "new_file").open("wb"):
		pass
	st = os.stat(os.path.join(BASE, "new_file"))
	assert stat.S_IMODE(st.st_mode) == 0o666
	os.umask(0o022)
	with (p / "other_new_file").open("wb"):
		pass
	st = os.stat(os.path.join(BASE, "other_new_file"))
	assert stat.S_IMODE(st.st_mode) == 0o644


@only_posix
def test_touch_mode(BASE: PathPlus):
	old_mask = os.umask(0)

	try:
		p = PathPlus(BASE)
		(p / "new_file").touch()
		st = os.stat(os.path.join(BASE, "new_file"))
		assert stat.S_IMODE(st.st_mode) == 0o666
		os.umask(0o022)
		(p / "other_new_file").touch()
		st = os.stat(os.path.join(BASE, "other_new_file"))
		assert stat.S_IMODE(st.st_mode) == 0o644
		(p / "masked_new_file").touch(mode=0o750)
		st = os.stat(os.path.join(BASE, "masked_new_file"))
		assert stat.S_IMODE(st.st_mode) == 0o750
	finally:
		os.umask(old_mask)
