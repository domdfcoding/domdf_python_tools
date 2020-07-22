#  Adapted from https://github.com/python/cpython/blob/master/Lib/test/test_pathlib.py
#
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com . All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives . All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum . All rights reserved.
#

# stdlib
import collections.abc
import errno
import io
import os
import pathlib
import pickle
import platform
import socket
import stat
import sys
import tempfile
import unittest
from test import support  # type: ignore
from test.support import TESTFN  # type: ignore
from unittest import mock

# 3rd party
import pytest

# this package
from domdf_python_tools.paths import PathPlus, PosixPathPlus, WindowsPathPlus

try:
	# stdlib
	import grp
	import pwd
except ImportError:
	grp = pwd = None  # type: ignore

# Make sure any symbolic links in the base test path are resolved.
BASE = os.path.realpath(TESTFN)
join = lambda *x: os.path.join(BASE, *x)
rel_join = lambda *x: os.path.join(TESTFN, *x)


def symlink_skip_reason():
	if not pathlib.supports_symlinks:
		return "no system support for symlinks"
	try:
		os.symlink(__file__, BASE)
	except (OSError, NotImplementedError) as e:  # NotImplementedError is raised by PyPy
		return str(e)
	else:
		support.unlink(BASE)
	return None


symlink_skip_reason = symlink_skip_reason()
only_nt = pytest.mark.skipif(condition=os.name != 'nt', reason='test requires a Windows-compatible system')
only_posix = pytest.mark.skipif(condition=os.name == 'nt', reason='test requires a POSIX-compatible system')
with_symlinks = unittest.skipIf(symlink_skip_reason, symlink_skip_reason)  # type: ignore


class PathTest(unittest.TestCase):
	cls = PathPlus

	def setUp(self):

		def cleanup():
			os.chmod(join('dirE'), 0o777)
			support.rmtree(BASE)

		self.addCleanup(cleanup)
		os.mkdir(BASE)
		os.mkdir(join('dirA'))
		os.mkdir(join('dirB'))
		os.mkdir(join('dirC'))
		os.mkdir(join('dirC', 'dirD'))
		os.mkdir(join('dirE'))
		with open(join('fileA'), 'wb') as f:
			f.write(b"this is file A\n")
		with open(join('dirB', 'fileB'), 'wb') as f:
			f.write(b"this is file B\n")
		with open(join('dirC', 'fileC'), 'wb') as f:
			f.write(b"this is file C\n")
		with open(join('dirC', 'dirD', 'fileD'), 'wb') as f:
			f.write(b"this is file D\n")
		os.chmod(join('dirE'), 0)
		if not symlink_skip_reason:
			# Relative symlinks.
			os.symlink('fileA', join('linkA'))
			os.symlink('non-existing', join('brokenLink'))
			self.dirlink('dirB', join('linkB'))
			self.dirlink(os.path.join('..', 'dirB'), join('dirA', 'linkC'))
			# This one goes upwards, creating a loop.
			self.dirlink(os.path.join('..', 'dirB'), join('dirB', 'linkD'))

	if os.name == 'nt':
		# Workaround for http://bugs.python.org/issue13772.
		def dirlink(self, src, dest):
			os.symlink(src, dest, target_is_directory=True)
	else:

		def dirlink(self, src, dest):
			os.symlink(src, dest)

	def assertSame(self, path_a, path_b):
		self.assertTrue(
				os.path.samefile(str(path_a), str(path_b)),
				f"{path_a!r} and {path_b!r} don't point to the same file"
				)

	def assertFileNotFound(self, func, *args, **kwargs):
		with self.assertRaises(FileNotFoundError) as cm:
			func(*args, **kwargs)
		self.assertEqual(cm.exception.errno, errno.ENOENT)

	def assertEqualNormCase(self, path_a, path_b):
		self.assertEqual(os.path.normcase(path_a), os.path.normcase(path_b))

	def _test_cwd(self, p):
		q = PathPlus(os.getcwd())
		self.assertEqual(p, q)
		self.assertEqualNormCase(str(p), str(q))
		self.assertIs(type(p), type(q))
		self.assertTrue(p.is_absolute())

	def test_cwd(self):
		p = PathPlus.cwd()
		self._test_cwd(p)

	def _test_home(self, p):
		q = PathPlus(os.path.expanduser('~'))
		self.assertEqual(p, q)
		self.assertEqualNormCase(str(p), str(q))
		self.assertIs(type(p), type(q))
		self.assertTrue(p.is_absolute())

	def test_read_write_text(self):
		p = PathPlus(BASE)
		(p / 'fileA').write_text('äbcdefg', encoding='latin-1')
		self.assertEqual((p / 'fileA').read_text(encoding='utf-8', errors='ignore'), 'bcdefg')
		# Check that trying to write bytes does not truncate the file.
		self.assertRaises(TypeError, (p / 'fileA').write_text, b'somebytes')
		self.assertEqual((p / 'fileA').read_text(encoding='latin-1'), 'äbcdefg')

	def _check_resolve(self, p, expected, strict=True):
		q = p.resolve(strict)
		self.assertEqual(q, expected)

	# This can be used to check both relative and absolute resolutions.
	_check_resolve_relative = _check_resolve_absolute = _check_resolve

	def test_with(self):
		p = PathPlus(BASE)
		it = p.iterdir()
		it2 = p.iterdir()
		next(it2)
		with p:
			pass

		if sys.version_info < (3, 9):  # pragma: no cover (>=py39)
			# I/O operation on closed path
			self.assertRaises(ValueError, next, it)
			self.assertRaises(ValueError, next, it2)
			self.assertRaises(ValueError, p.open)
			self.assertRaises(ValueError, p.resolve)
			self.assertRaises(ValueError, p.absolute)
			self.assertRaises(ValueError, p.__enter__)

		else:  # pragma: no cover (<py39)
			# Using a path as a context manager is a no-op, thus the following
			# operations should still succeed after the context manage exits.
			next(it)
			next(it2)
			p.exists()
			p.resolve()
			p.absolute()
			with p:
				pass

	def test_chmod(self):
		p = PathPlus(BASE) / 'fileA'
		mode = p.stat().st_mode
		# Clear writable bit.
		new_mode = mode & ~0o222
		p.chmod(new_mode)
		self.assertEqual(p.stat().st_mode, new_mode)
		# Set writable bit.
		new_mode = mode | 0o222
		p.chmod(new_mode)
		self.assertEqual(p.stat().st_mode, new_mode)

	# XXX also need a test for lchmod.

	def test_stat(self):
		p = PathPlus(BASE) / 'fileA'
		st = p.stat()
		self.assertEqual(p.stat(), st)
		# Change file mode by flipping write bit.
		p.chmod(st.st_mode ^ 0o222)
		self.addCleanup(p.chmod, st.st_mode)
		self.assertNotEqual(p.stat(), st)

	@with_symlinks
	def test_lstat(self):
		p = PathPlus(BASE) / 'linkA'
		st = p.stat()
		self.assertNotEqual(st, p.lstat())

	def test_lstat_nosymlink(self):
		p = PathPlus(BASE) / 'fileA'
		st = p.stat()
		self.assertEqual(st, p.lstat())

	@unittest.skipUnless(pwd, "the pwd module is needed for this test")
	def test_owner(self):
		p = PathPlus(BASE) / 'fileA'
		uid = p.stat().st_uid
		try:
			name = pwd.getpwuid(uid).pw_name
		except KeyError:
			self.skipTest(f"user {uid:d} doesn't have an entry in the system database")
		self.assertEqual(name, p.owner())

	@unittest.skipUnless(grp, "the grp module is needed for this test")
	def test_group(self):
		p = PathPlus(BASE) / 'fileA'
		gid = p.stat().st_gid
		try:
			name = grp.getgrgid(gid).gr_name
		except KeyError:
			self.skipTest(f"group {gid:d} doesn't have an entry in the system database")
		self.assertEqual(name, p.group())

	def test_unlink(self):
		p = PathPlus(BASE) / 'fileA'
		p.unlink()
		self.assertFileNotFound(p.stat)
		self.assertFileNotFound(p.unlink)

	@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9 or higher")
	def test_unlink_missing_ok(self):  # pragma: no cover (<py37)
		p = PathPlus(BASE) / 'fileAAA'
		self.assertFileNotFound(p.unlink)
		p.unlink(missing_ok=True)

	def test_rmdir(self):
		p = PathPlus(BASE) / 'dirA'
		for q in p.iterdir():
			q.unlink()
		p.rmdir()
		self.assertFileNotFound(p.stat)
		self.assertFileNotFound(p.unlink)

	@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9 or higher")
	@unittest.skipUnless(hasattr(os, "link"), "os.link() is not present")
	def test_link_to(self):  # pragma: no cover (<py37)
		P = PathPlus(BASE)
		p = P / 'fileA'
		size = p.stat().st_size
		# linking to another path.
		q = P / 'dirA' / 'fileAA'
		try:
			p.link_to(q)
		except PermissionError as e:
			self.skipTest('os.link(): %s' % e)
		self.assertEqual(q.stat().st_size, size)
		self.assertEqual(os.path.samefile(p, q), True)
		self.assertTrue(p.stat)
		# Linking to a str of a relative path.
		r = rel_join('fileAAA')
		q.link_to(r)
		self.assertEqual(os.stat(r).st_size, size)
		self.assertTrue(q.stat)

	@unittest.skipIf(hasattr(os, "link"), "os.link() is present")
	def test_link_to_not_implemented(self):
		P = PathPlus(BASE)
		p = P / 'fileA'
		# linking to another path.
		q = P / 'dirA' / 'fileAA'
		with self.assertRaises(NotImplementedError):
			p.link_to(q)

	def test_rename(self):
		P = PathPlus(BASE)
		p = P / 'fileA'
		size = p.stat().st_size
		# Renaming to another path.
		q = P / 'dirA' / 'fileAA'

		if sys.version_info < (3, 9):  # pragma: no cover (>=py39)
			p.replace(q)

		else:  # pragma: no cover (<py39)
			renamed_p = p.replace(q)
			self.assertEqual(renamed_p, q)

		self.assertEqual(q.stat().st_size, size)
		self.assertFileNotFound(p.stat)

		# Renaming to a str of a relative path.
		r = rel_join('fileAAA')

		if sys.version_info < (3, 9):  # pragma: no cover (>=py39)
			q.replace(r)

		else:  # pragma: no cover (<py39)
			renamed_q = q.replace(r)
			self.assertEqual(renamed_q, PathPlus(r))

		self.assertEqual(os.stat(r).st_size, size)
		self.assertFileNotFound(q.stat)

	def test_replace(self):
		P = PathPlus(BASE)
		p = P / 'fileA'
		size = p.stat().st_size
		# Replacing a non-existing path.
		q = P / 'dirA' / 'fileAA'

		if sys.version_info < (3, 9):  # pragma: no cover (>=py39)
			p.replace(q)

		else:  # pragma: no cover (<py39)
			replaced_p = p.replace(q)
			self.assertEqual(replaced_p, q)

		self.assertEqual(q.stat().st_size, size)
		self.assertFileNotFound(p.stat)

		# Replacing another (existing) path.
		r = rel_join('dirB', 'fileB')

		if sys.version_info < (3, 9):  # pragma: no cover (>=py39)
			q.replace(r)

		else:  # pragma: no cover (<py39)
			replaced_q = q.replace(r)
			self.assertEqual(replaced_q, PathPlus(r))

		self.assertEqual(os.stat(r).st_size, size)
		self.assertFileNotFound(q.stat)

	@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires python3.9 or higher")
	@with_symlinks
	def test_readlink(self):  # pragma: no cover (<py39)
		P = PathPlus(BASE)
		self.assertEqual((P / 'linkA').readlink(), PathPlus('fileA'))
		self.assertEqual((P / 'brokenLink').readlink(), PathPlus('non-existing'))
		self.assertEqual((P / 'linkB').readlink(), PathPlus('dirB'))
		with self.assertRaises(OSError):
			(P / 'fileA').readlink()

	def test_touch_common(self):
		P = PathPlus(BASE)
		p = P / 'newfileA'
		self.assertFalse(p.exists())
		p.touch()
		self.assertTrue(p.exists())
		st = p.stat()
		old_mtime = st.st_mtime
		old_mtime_ns = st.st_mtime_ns
		# Rewind the mtime sufficiently far in the past to work around
		# filesystem-specific timestamp granularity.
		os.utime(str(p), (old_mtime - 10, old_mtime - 10))
		# The file mtime should be refreshed by calling touch() again.
		p.touch()
		st = p.stat()
		self.assertGreaterEqual(st.st_mtime_ns, old_mtime_ns)
		self.assertGreaterEqual(st.st_mtime, old_mtime)
		# Now with exist_ok=False.
		p = P / 'newfileB'
		self.assertFalse(p.exists())
		p.touch(mode=0o700, exist_ok=False)
		self.assertTrue(p.exists())
		self.assertRaises(OSError, p.touch, exist_ok=False)

	def test_touch_nochange(self):
		P = PathPlus(BASE)
		p = P / 'fileA'
		p.touch()
		with p.open('rb') as f:
			self.assertEqual(f.read().strip(), b"this is file A")

	def test_mkdir(self):
		P = PathPlus(BASE)
		p = P / 'newdirA'
		self.assertFalse(p.exists())
		p.mkdir()
		self.assertTrue(p.exists())
		self.assertTrue(p.is_dir())
		with self.assertRaises(OSError) as cm:
			p.mkdir()
		self.assertEqual(cm.exception.errno, errno.EEXIST)

	def test_mkdir_parents(self):
		# Creating a chain of directories.
		p = PathPlus(BASE, 'newdirB', 'newdirC')
		self.assertFalse(p.exists())
		with self.assertRaises(OSError) as cm:
			p.mkdir()
		self.assertEqual(cm.exception.errno, errno.ENOENT)
		p.mkdir(parents=True)
		self.assertTrue(p.exists())
		self.assertTrue(p.is_dir())
		with self.assertRaises(OSError) as cm:
			p.mkdir(parents=True)
		self.assertEqual(cm.exception.errno, errno.EEXIST)
		# Test `mode` arg.
		mode = stat.S_IMODE(p.stat().st_mode)  # Default mode.
		p = PathPlus(BASE, 'newdirD', 'newdirE')
		p.mkdir(0o555, parents=True)
		self.assertTrue(p.exists())
		self.assertTrue(p.is_dir())
		if os.name != 'nt':
			# The directory's permissions follow the mode argument.
			self.assertEqual(stat.S_IMODE(p.stat().st_mode), 0o7555 & mode)
		# The parent's permissions follow the default process settings.
		self.assertEqual(stat.S_IMODE(p.parent.stat().st_mode), mode)

	def test_mkdir_exist_ok(self):
		p = PathPlus(BASE, 'dirB')
		st_ctime_first = p.stat().st_ctime
		self.assertTrue(p.exists())
		self.assertTrue(p.is_dir())
		with self.assertRaises(FileExistsError) as cm:
			p.mkdir()
		self.assertEqual(cm.exception.errno, errno.EEXIST)
		p.mkdir(exist_ok=True)
		self.assertTrue(p.exists())
		self.assertEqual(p.stat().st_ctime, st_ctime_first)

	def test_mkdir_exist_ok_with_parent(self):
		p = PathPlus(BASE, 'dirC')
		self.assertTrue(p.exists())
		with self.assertRaises(FileExistsError) as cm:
			p.mkdir()
		self.assertEqual(cm.exception.errno, errno.EEXIST)
		p = p / 'newdirC'
		p.mkdir(parents=True)
		st_ctime_first = p.stat().st_ctime
		self.assertTrue(p.exists())
		with self.assertRaises(FileExistsError) as cm:
			p.mkdir(parents=True)
		self.assertEqual(cm.exception.errno, errno.EEXIST)
		p.mkdir(parents=True, exist_ok=True)
		self.assertTrue(p.exists())
		self.assertEqual(p.stat().st_ctime, st_ctime_first)

	def test_mkdir_exist_ok_root(self):
		# Issue #25803: A drive root could raise PermissionError on Windows.
		PathPlus('/').resolve().mkdir(exist_ok=True)
		PathPlus('/').resolve().mkdir(parents=True, exist_ok=True)

	@only_nt  # XXX: not sure how to test this on POSIX.
	def test_mkdir_with_unknown_drive(self):
		for d in 'ZYXWVUTSRQPONMLKJIHGFEDCBA':
			p = PathPlus(d + ':\\')
			if not p.is_dir():
				break
		else:
			self.skipTest("cannot find a drive that doesn't exist")
		with self.assertRaises(OSError):
			(p / 'child' / 'path').mkdir(parents=True)

	def test_mkdir_with_child_file(self):
		p = PathPlus(BASE, 'dirB', 'fileB')
		self.assertTrue(p.exists())
		# An exception is raised when the last path component is an existing
		# regular file, regardless of whether exist_ok is true or not.
		with self.assertRaises(FileExistsError) as cm:
			p.mkdir(parents=True)
		self.assertEqual(cm.exception.errno, errno.EEXIST)
		with self.assertRaises(FileExistsError) as cm:
			p.mkdir(parents=True, exist_ok=True)
		self.assertEqual(cm.exception.errno, errno.EEXIST)

	def test_mkdir_no_parents_file(self):
		p = PathPlus(BASE, 'fileA')
		self.assertTrue(p.exists())
		# An exception is raised when the last path component is an existing
		# regular file, regardless of whether exist_ok is true or not.
		with self.assertRaises(FileExistsError) as cm:
			p.mkdir()
		self.assertEqual(cm.exception.errno, errno.EEXIST)
		with self.assertRaises(FileExistsError) as cm:
			p.mkdir(exist_ok=True)
		self.assertEqual(cm.exception.errno, errno.EEXIST)

	def test_mkdir_concurrent_parent_creation(self):
		for pattern_num in range(32):
			p = PathPlus(BASE, 'dirCPC%d' % pattern_num)
			self.assertFalse(p.exists())

			def my_mkdir(path, mode=0o777):
				path = str(path)
				# Emulate another process that would create the directory
				# just before we try to create it ourselves.  We do it
				# in all possible pattern combinations, assuming that this
				# function is called at most 5 times (dirCPC/dir1/dir2,
				# dirCPC/dir1, dirCPC, dirCPC/dir1, dirCPC/dir1/dir2).
				if pattern.pop():
					os.mkdir(path, mode)  # From another process.
					concurrently_created.add(path)
				os.mkdir(path, mode)  # Our real call.

			pattern = [bool(pattern_num & (1 << n)) for n in range(5)]
			concurrently_created = set()
			p12 = p / 'dir1' / 'dir2'
			try:
				with mock.patch("pathlib._normal_accessor.mkdir", my_mkdir):
					p12.mkdir(parents=True, exist_ok=False)
			except FileExistsError:
				self.assertIn(str(p12), concurrently_created)
			else:
				self.assertNotIn(str(p12), concurrently_created)
			self.assertTrue(p.exists())

	@with_symlinks
	def test_symlink_to(self):
		P = PathPlus(BASE)
		target = P / 'fileA'
		# Symlinking a path target.
		link = P / 'dirA' / 'linkAA'
		link.symlink_to(target)
		self.assertEqual(link.stat(), target.stat())
		self.assertNotEqual(link.lstat(), target.stat())
		# Symlinking a str target.
		link = P / 'dirA' / 'linkAAA'
		link.symlink_to(str(target))
		self.assertEqual(link.stat(), target.stat())
		self.assertNotEqual(link.lstat(), target.stat())
		self.assertFalse(link.is_dir())
		# Symlinking to a directory.
		target = P / 'dirB'
		link = P / 'dirA' / 'linkAAAA'
		link.symlink_to(target, target_is_directory=True)
		self.assertEqual(link.stat(), target.stat())
		self.assertNotEqual(link.lstat(), target.stat())
		self.assertTrue(link.is_dir())
		self.assertTrue(list(link.iterdir()))

	def test_is_dir(self):
		P = PathPlus(BASE)
		self.assertTrue((P / 'dirA').is_dir())
		self.assertFalse((P / 'fileA').is_dir())
		self.assertFalse((P / 'non-existing').is_dir())
		self.assertFalse((P / 'fileA' / 'bah').is_dir())
		if not symlink_skip_reason:
			self.assertFalse((P / 'linkA').is_dir())
			self.assertTrue((P / 'linkB').is_dir())
			self.assertFalse((P / 'brokenLink').is_dir(), False)

	def test_is_file(self):
		P = PathPlus(BASE)
		self.assertTrue((P / 'fileA').is_file())
		self.assertFalse((P / 'dirA').is_file())
		self.assertFalse((P / 'non-existing').is_file())
		self.assertFalse((P / 'fileA' / 'bah').is_file())
		if not symlink_skip_reason:
			self.assertTrue((P / 'linkA').is_file())
			self.assertFalse((P / 'linkB').is_file())
			self.assertFalse((P / 'brokenLink').is_file())

	@pytest.mark.skipif(sys.version_info < (3, 7), reason="requires python3.7 or higher")
	@only_posix
	def test_is_mount(self):  # pragma: no cover (<py37)
		P = PathPlus(BASE)
		R = PathPlus('/')  # TODO: Work out Windows.
		self.assertFalse((P / 'fileA').is_mount())
		self.assertFalse((P / 'dirA').is_mount())
		self.assertFalse((P / 'non-existing').is_mount())
		self.assertFalse((P / 'fileA' / 'bah').is_mount())
		self.assertTrue(R.is_mount())
		if support.can_symlink():
			self.assertFalse((P / 'linkA').is_mount())

	def test_is_symlink(self):
		P = PathPlus(BASE)
		self.assertFalse((P / 'fileA').is_symlink())
		self.assertFalse((P / 'dirA').is_symlink())
		self.assertFalse((P / 'non-existing').is_symlink())
		self.assertFalse((P / 'fileA' / 'bah').is_symlink())
		if not symlink_skip_reason:
			self.assertTrue((P / 'linkA').is_symlink())
			self.assertTrue((P / 'linkB').is_symlink())
			self.assertTrue((P / 'brokenLink').is_symlink())

	def test_is_fifo_false(self):
		P = PathPlus(BASE)
		self.assertFalse((P / 'fileA').is_fifo())
		self.assertFalse((P / 'dirA').is_fifo())
		self.assertFalse((P / 'non-existing').is_fifo())
		self.assertFalse((P / 'fileA' / 'bah').is_fifo())

	@unittest.skipUnless(hasattr(os, "mkfifo"), "os.mkfifo() required")
	def test_is_fifo_true(self):
		P = PathPlus(BASE, 'myfifo')
		try:
			os.mkfifo(str(P))
		except PermissionError as e:
			self.skipTest('os.mkfifo(): %s' % e)
		self.assertTrue(P.is_fifo())
		self.assertFalse(P.is_socket())
		self.assertFalse(P.is_file())

	def test_is_socket_false(self):
		P = PathPlus(BASE)
		self.assertFalse((P / 'fileA').is_socket())
		self.assertFalse((P / 'dirA').is_socket())
		self.assertFalse((P / 'non-existing').is_socket())
		self.assertFalse((P / 'fileA' / 'bah').is_socket())

	@unittest.skipUnless(hasattr(socket, "AF_UNIX"), "Unix sockets required")
	def test_is_socket_true(self):
		P = PathPlus(BASE, 'mysock')
		sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.addCleanup(sock.close)
		try:
			sock.bind(str(P))
		except OSError as e:
			if isinstance(e, PermissionError) or "AF_UNIX path too long" in str(e):
				self.skipTest("cannot bind Unix socket: " + str(e))
		self.assertTrue(P.is_socket())
		self.assertFalse(P.is_fifo())
		self.assertFalse(P.is_file())

	def test_is_block_device_false(self):
		P = PathPlus(BASE)
		self.assertFalse((P / 'fileA').is_block_device())
		self.assertFalse((P / 'dirA').is_block_device())
		self.assertFalse((P / 'non-existing').is_block_device())
		self.assertFalse((P / 'fileA' / 'bah').is_block_device())

	def test_is_char_device_false(self):
		P = PathPlus(BASE)
		self.assertFalse((P / 'fileA').is_char_device())
		self.assertFalse((P / 'dirA').is_char_device())
		self.assertFalse((P / 'non-existing').is_char_device())
		self.assertFalse((P / 'fileA' / 'bah').is_char_device())

	def test_is_char_device_true(self):
		# Under Unix, /dev/null should generally be a char device.
		P = PathPlus('/dev/null')
		if not P.exists():
			self.skipTest("/dev/null required")
		self.assertTrue(P.is_char_device())
		self.assertFalse(P.is_block_device())
		self.assertFalse(P.is_file())

	def test_pickling_common(self):
		p = PathPlus(BASE, 'fileA')
		for proto in range(0, pickle.HIGHEST_PROTOCOL + 1):
			dumped = pickle.dumps(p, proto)
			pp = pickle.loads(dumped)
			self.assertEqual(pp.stat(), p.stat())

	def _check_complex_symlinks(self, link0_target):
		# Test solving a non-looping chain of symlinks (issue #19887).
		P = PathPlus(BASE)
		self.dirlink(os.path.join('link0', 'link0'), join('link1'))
		self.dirlink(os.path.join('link1', 'link1'), join('link2'))
		self.dirlink(os.path.join('link2', 'link2'), join('link3'))
		self.dirlink(link0_target, join('link0'))

		# Resolve absolute paths.
		p = (P / 'link0').resolve()
		self.assertEqual(p, P)
		self.assertEqualNormCase(str(p), BASE)
		p = (P / 'link1').resolve()
		self.assertEqual(p, P)
		self.assertEqualNormCase(str(p), BASE)
		p = (P / 'link2').resolve()
		self.assertEqual(p, P)
		self.assertEqualNormCase(str(p), BASE)
		p = (P / 'link3').resolve()
		self.assertEqual(p, P)
		self.assertEqualNormCase(str(p), BASE)

		# Resolve relative paths.
		old_path = os.getcwd()
		os.chdir(BASE)
		try:
			p = PathPlus('link0').resolve()
			self.assertEqual(p, P)
			self.assertEqualNormCase(str(p), BASE)
			p = PathPlus('link1').resolve()
			self.assertEqual(p, P)
			self.assertEqualNormCase(str(p), BASE)
			p = PathPlus('link2').resolve()
			self.assertEqual(p, P)
			self.assertEqualNormCase(str(p), BASE)
			p = PathPlus('link3').resolve()
			self.assertEqual(p, P)
			self.assertEqualNormCase(str(p), BASE)
		finally:
			os.chdir(old_path)

	@with_symlinks
	def test_complex_symlinks_absolute(self):
		self._check_complex_symlinks(BASE)

	@with_symlinks
	def test_complex_symlinks_relative(self):
		self._check_complex_symlinks('.')

	@with_symlinks
	def test_complex_symlinks_relative_dot_dot(self):
		self._check_complex_symlinks(os.path.join('dirA', '..'))

	def test_concrete_class(self):
		p = PathPlus('a')
		self.assertIs(type(p), WindowsPathPlus if os.name == 'nt' else PosixPathPlus)

	def test_unsupported_flavour(self):
		if os.name == 'nt':
			self.assertRaises(NotImplementedError, pathlib.PosixPath)
		else:
			self.assertRaises(NotImplementedError, pathlib.WindowsPath)

	def test_glob_empty_pattern(self):
		p = PathPlus()
		with self.assertRaisesRegex(ValueError, 'Unacceptable pattern'):
			list(p.glob(''))


@only_posix
class PosixPathTest(PathTest, unittest.TestCase):  # pragma: no cover (!Linux !Darwin)

	def _check_symlink_loop(self, *args, strict=True):
		path = PathPlus(*args)
		with self.assertRaises(RuntimeError):
			print(path.resolve(strict))

	def test_open_mode(self):
		old_mask = os.umask(0)
		self.addCleanup(os.umask, old_mask)
		p = PathPlus(BASE)
		with (p / 'new_file').open('wb'):
			pass
		st = os.stat(join('new_file'))
		self.assertEqual(stat.S_IMODE(st.st_mode), 0o666)
		os.umask(0o022)
		with (p / 'other_new_file').open('wb'):
			pass
		st = os.stat(join('other_new_file'))
		self.assertEqual(stat.S_IMODE(st.st_mode), 0o644)

	def test_touch_mode(self):
		old_mask = os.umask(0)
		self.addCleanup(os.umask, old_mask)
		p = PathPlus(BASE)
		(p / 'new_file').touch()
		st = os.stat(join('new_file'))
		self.assertEqual(stat.S_IMODE(st.st_mode), 0o666)
		os.umask(0o022)
		(p / 'other_new_file').touch()
		st = os.stat(join('other_new_file'))
		self.assertEqual(stat.S_IMODE(st.st_mode), 0o644)
		(p / 'masked_new_file').touch(mode=0o750)
		st = os.stat(join('masked_new_file'))
		self.assertEqual(stat.S_IMODE(st.st_mode), 0o750)

	@with_symlinks
	def test_resolve_loop(self):
		# Loops with relative symlinks.
		os.symlink('linkX/inside', join('linkX'))
		self._check_symlink_loop(BASE, 'linkX')
		os.symlink('linkY', join('linkY'))
		self._check_symlink_loop(BASE, 'linkY')
		os.symlink('linkZ/../linkZ', join('linkZ'))
		self._check_symlink_loop(BASE, 'linkZ')
		# Non-strict
		self._check_symlink_loop(BASE, 'linkZ', 'foo', strict=False)
		# Loops with absolute symlinks.
		os.symlink(join('linkU/inside'), join('linkU'))
		self._check_symlink_loop(BASE, 'linkU')
		os.symlink(join('linkV'), join('linkV'))
		self._check_symlink_loop(BASE, 'linkV')
		os.symlink(join('linkW/../linkW'), join('linkW'))
		self._check_symlink_loop(BASE, 'linkW')
		# Non-strict
		self._check_symlink_loop(BASE, 'linkW', 'foo', strict=False)

	def test_glob(self):
		P = PathPlus
		p = P(BASE)
		given = set(p.glob("FILEa"))
		expect = set() if not support.fs_is_case_insensitive(BASE) else given
		self.assertEqual(given, expect)
		self.assertEqual(set(p.glob("FILEa*")), set())

	def test_rglob(self):
		P = PathPlus
		p = P(BASE, "dirC")
		given = set(p.rglob("FILEd"))
		expect = set() if not support.fs_is_case_insensitive(BASE) else given
		self.assertEqual(given, expect)
		self.assertEqual(set(p.rglob("FILEd*")), set())

	@unittest.skipUnless(hasattr(pwd, 'getpwall'), 'pwd module does not expose getpwall()')
	def test_expanduser(self):
		P = PathPlus
		support.import_module('pwd')
		# stdlib
		import pwd
		pwdent = pwd.getpwuid(os.getuid())
		username = pwdent.pw_name
		userhome = pwdent.pw_dir.rstrip('/') or '/'
		# Find arbitrary different user (if exists).
		for pwdent in pwd.getpwall():
			othername = pwdent.pw_name
			otherhome = pwdent.pw_dir.rstrip('/')
			if othername != username and otherhome:
				break
		else:
			othername = username
			otherhome = userhome

		p1 = P('~/Documents')
		p2 = P('~' + username + '/Documents')
		p3 = P('~' + othername + '/Documents')
		p4 = P('../~' + username + '/Documents')
		p5 = P('/~' + username + '/Documents')
		p6 = P('')
		p7 = P('~fakeuser/Documents')

		with support.EnvironmentVarGuard() as env:
			env.pop('HOME', None)

			self.assertEqual(p1.expanduser(), P(userhome) / 'Documents')
			self.assertEqual(p2.expanduser(), P(userhome) / 'Documents')
			self.assertEqual(p3.expanduser(), P(otherhome) / 'Documents')
			self.assertEqual(p4.expanduser(), p4)
			self.assertEqual(p5.expanduser(), p5)
			self.assertEqual(p6.expanduser(), p6)
			self.assertRaises(RuntimeError, p7.expanduser)

			env['HOME'] = '/tmp'
			self.assertEqual(p1.expanduser(), P('/tmp/Documents'))
			self.assertEqual(p2.expanduser(), P(userhome) / 'Documents')
			self.assertEqual(p3.expanduser(), P(otherhome) / 'Documents')
			self.assertEqual(p4.expanduser(), p4)
			self.assertEqual(p5.expanduser(), p5)
			self.assertEqual(p6.expanduser(), p6)
			self.assertRaises(RuntimeError, p7.expanduser)


@only_nt
class WindowsPathTest(PathTest, unittest.TestCase):  # pragma: no cover (!Windows)

	def test_glob(self):
		P = PathPlus
		p = P(BASE)
		self.assertEqual(set(p.glob("FILEa")), {P(BASE, "fileA")})
		self.assertEqual(set(p.glob("F*a")), {P(BASE, "fileA")})
		self.assertEqual(set(map(str, p.glob("FILEa"))), {f"{p}\\FILEa"})
		self.assertEqual(set(map(str, p.glob("F*a"))), {f"{p}\\fileA"})

	def test_rglob(self):
		P = PathPlus
		p = P(BASE, "dirC")
		self.assertEqual(set(p.rglob("FILEd")), {P(BASE, "dirC/dirD/fileD")})
		self.assertEqual(set(map(str, p.rglob("FILEd"))), {f"{p}\\dirD\\FILEd"})

	def test_expanduser(self):
		P = PathPlus
		with support.EnvironmentVarGuard() as env:
			env.pop('HOME', None)
			env.pop('USERPROFILE', None)
			env.pop('HOMEPATH', None)
			env.pop('HOMEDRIVE', None)
			env['USERNAME'] = 'alice'

			# test that the path returns unchanged
			p1 = P('~/My Documents')
			p2 = P('~alice/My Documents')
			p3 = P('~bob/My Documents')
			p4 = P('/~/My Documents')
			p5 = P('d:~/My Documents')
			p6 = P('')
			self.assertRaises(RuntimeError, p1.expanduser)
			self.assertRaises(RuntimeError, p2.expanduser)
			self.assertRaises(RuntimeError, p3.expanduser)
			self.assertEqual(p4.expanduser(), p4)
			self.assertEqual(p5.expanduser(), p5)
			self.assertEqual(p6.expanduser(), p6)

			def check():
				env.pop('USERNAME', None)
				self.assertEqual(p1.expanduser(), P('C:/Users/alice/My Documents'))
				self.assertRaises(KeyError, p2.expanduser)
				env['USERNAME'] = 'alice'
				self.assertEqual(p2.expanduser(), P('C:/Users/alice/My Documents'))
				self.assertEqual(p3.expanduser(), P('C:/Users/bob/My Documents'))
				self.assertEqual(p4.expanduser(), p4)
				self.assertEqual(p5.expanduser(), p5)
				self.assertEqual(p6.expanduser(), p6)

			env['HOMEPATH'] = 'C:\\Users\\alice'
			check()

			env['HOMEDRIVE'] = 'C:\\'
			env['HOMEPATH'] = 'Users\\alice'
			check()

			env.pop('HOMEDRIVE', None)
			env.pop('HOMEPATH', None)
			env['USERPROFILE'] = 'C:\\Users\\alice'
			check()

			# bpo-38883: ignore `HOME` when set on windows
			env['HOME'] = 'C:\\Users\\eve'
			check()


if __name__ == "__main__":  # pragma: no cover
	unittest.main()