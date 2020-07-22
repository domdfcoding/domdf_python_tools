# stdlib
import collections.abc
import errno
import io
import os
import pathlib
import pickle
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


class _BaseFlavourTest(object):

	def _check_parse_parts(self, arg, expected):
		f = self.flavour.parse_parts
		sep = self.flavour.sep
		altsep = self.flavour.altsep
		actual = f([x.replace('/', sep) for x in arg])
		self.assertEqual(actual, expected)
		if altsep:
			actual = f([x.replace('/', altsep) for x in arg])
			self.assertEqual(actual, expected)

	def test_parse_parts_common(self):
		check = self._check_parse_parts
		sep = self.flavour.sep
		# Unanchored parts.
		check([], ('', '', []))
		check(['a'], ('', '', ['a']))
		check(['a/'], ('', '', ['a']))
		check(['a', 'b'], ('', '', ['a', 'b']))
		# Expansion.
		check(['a/b'], ('', '', ['a', 'b']))
		check(['a/b/'], ('', '', ['a', 'b']))
		check(['a', 'b/c', 'd'], ('', '', ['a', 'b', 'c', 'd']))
		# Collapsing and stripping excess slashes.
		check(['a', 'b//c', 'd'], ('', '', ['a', 'b', 'c', 'd']))
		check(['a', 'b/c/', 'd'], ('', '', ['a', 'b', 'c', 'd']))
		# Eliminating standalone dots.
		check(['.'], ('', '', []))
		check(['.', '.', 'b'], ('', '', ['b']))
		check(['a', '.', 'b'], ('', '', ['a', 'b']))
		check(['a', '.', '.'], ('', '', ['a']))
		# The first part is anchored.
		check(['/a/b'], ('', sep, [sep, 'a', 'b']))
		check(['/a', 'b'], ('', sep, [sep, 'a', 'b']))
		check(['/a/', 'b'], ('', sep, [sep, 'a', 'b']))
		# Ignoring parts before an anchored part.
		check(['a', '/b', 'c'], ('', sep, [sep, 'b', 'c']))
		check(['a', '/b', '/c'], ('', sep, [sep, 'c']))


class PosixFlavourTest(_BaseFlavourTest, unittest.TestCase):
	flavour = pathlib._posix_flavour  # type: ignore

	def test_parse_parts(self):
		check = self._check_parse_parts
		# Collapsing of excess leading slashes, except for the double-slash
		# special case.
		check(['//a', 'b'], ('', '//', ['//', 'a', 'b']))
		check(['///a', 'b'], ('', '/', ['/', 'a', 'b']))
		check(['////a', 'b'], ('', '/', ['/', 'a', 'b']))
		# Paths which look like NT paths aren't treated specially.
		check(['c:a'], ('', '', ['c:a']))
		check(['c:\\a'], ('', '', ['c:\\a']))
		check(['\\a'], ('', '', ['\\a']))

	def test_splitroot(self):
		f = self.flavour.splitroot
		self.assertEqual(f(''), ('', '', ''))
		self.assertEqual(f('a'), ('', '', 'a'))
		self.assertEqual(f('a/b'), ('', '', 'a/b'))
		self.assertEqual(f('a/b/'), ('', '', 'a/b/'))
		self.assertEqual(f('/a'), ('', '/', 'a'))
		self.assertEqual(f('/a/b'), ('', '/', 'a/b'))
		self.assertEqual(f('/a/b/'), ('', '/', 'a/b/'))
		# The root is collapsed when there are redundant slashes
		# except when there are exactly two leading slashes, which
		# is a special case in POSIX.
		self.assertEqual(f('//a'), ('', '//', 'a'))
		self.assertEqual(f('///a'), ('', '/', 'a'))
		self.assertEqual(f('///a/b'), ('', '/', 'a/b'))
		# Paths which look like NT paths aren't treated specially.
		self.assertEqual(f('c:/a/b'), ('', '', 'c:/a/b'))
		self.assertEqual(f('\\/a/b'), ('', '', '\\/a/b'))
		self.assertEqual(f('\\a\\b'), ('', '', '\\a\\b'))


class NTFlavourTest(_BaseFlavourTest, unittest.TestCase):
	flavour = pathlib._windows_flavour  # type: ignore

	def test_parse_parts(self):
		check = self._check_parse_parts
		# First part is anchored.
		check(['c:'], ('c:', '', ['c:']))
		check(['c:/'], ('c:', '\\', ['c:\\']))
		check(['/'], ('', '\\', ['\\']))
		check(['c:a'], ('c:', '', ['c:', 'a']))
		check(['c:/a'], ('c:', '\\', ['c:\\', 'a']))
		check(['/a'], ('', '\\', ['\\', 'a']))
		# UNC paths.
		check(['//a/b'], ('\\\\a\\b', '\\', ['\\\\a\\b\\']))
		check(['//a/b/'], ('\\\\a\\b', '\\', ['\\\\a\\b\\']))
		check(['//a/b/c'], ('\\\\a\\b', '\\', ['\\\\a\\b\\', 'c']))
		# Second part is anchored, so that the first part is ignored.
		check(['a', 'Z:b', 'c'], ('Z:', '', ['Z:', 'b', 'c']))
		check(['a', 'Z:/b', 'c'], ('Z:', '\\', ['Z:\\', 'b', 'c']))
		# UNC paths.
		check(['a', '//b/c', 'd'], ('\\\\b\\c', '\\', ['\\\\b\\c\\', 'd']))
		# Collapsing and stripping excess slashes.
		check(['a', 'Z://b//c/', 'd/'], ('Z:', '\\', ['Z:\\', 'b', 'c', 'd']))
		# UNC paths.
		check(['a', '//b/c//', 'd'], ('\\\\b\\c', '\\', ['\\\\b\\c\\', 'd']))
		# Extended paths.
		check(['//?/c:/'], ('\\\\?\\c:', '\\', ['\\\\?\\c:\\']))
		check(['//?/c:/a'], ('\\\\?\\c:', '\\', ['\\\\?\\c:\\', 'a']))
		check(['//?/c:/a', '/b'], ('\\\\?\\c:', '\\', ['\\\\?\\c:\\', 'b']))
		# Extended UNC paths (format is "\\?\UNC\server\share").
		check(['//?/UNC/b/c'], ('\\\\?\\UNC\\b\\c', '\\', ['\\\\?\\UNC\\b\\c\\']))
		check(['//?/UNC/b/c/d'], ('\\\\?\\UNC\\b\\c', '\\', ['\\\\?\\UNC\\b\\c\\', 'd']))
		# Second part has a root but not drive.
		check(['a', '/b', 'c'], ('', '\\', ['\\', 'b', 'c']))
		check(['Z:/a', '/b', 'c'], ('Z:', '\\', ['Z:\\', 'b', 'c']))
		check(['//?/Z:/a', '/b', 'c'], ('\\\\?\\Z:', '\\', ['\\\\?\\Z:\\', 'b', 'c']))

	def test_splitroot(self):
		f = self.flavour.splitroot
		self.assertEqual(f(''), ('', '', ''))
		self.assertEqual(f('a'), ('', '', 'a'))
		self.assertEqual(f('a\\b'), ('', '', 'a\\b'))
		self.assertEqual(f('\\a'), ('', '\\', 'a'))
		self.assertEqual(f('\\a\\b'), ('', '\\', 'a\\b'))
		self.assertEqual(f('c:a\\b'), ('c:', '', 'a\\b'))
		self.assertEqual(f('c:\\a\\b'), ('c:', '\\', 'a\\b'))
		# Redundant slashes in the root are collapsed.
		self.assertEqual(f('\\\\a'), ('', '\\', 'a'))
		self.assertEqual(f('\\\\\\a/b'), ('', '\\', 'a/b'))
		self.assertEqual(f('c:\\\\a'), ('c:', '\\', 'a'))
		self.assertEqual(f('c:\\\\\\a/b'), ('c:', '\\', 'a/b'))
		# Valid UNC paths.
		self.assertEqual(f('\\\\a\\b'), ('\\\\a\\b', '\\', ''))
		self.assertEqual(f('\\\\a\\b\\'), ('\\\\a\\b', '\\', ''))
		self.assertEqual(f('\\\\a\\b\\c\\d'), ('\\\\a\\b', '\\', 'c\\d'))
		# These are non-UNC paths (according to ntpath.py and test_ntpath).
		# However, command.com says such paths are invalid, so it's
		# difficult to know what the right semantics are.
		self.assertEqual(f('\\\\\\a\\b'), ('', '\\', 'a\\b'))
		self.assertEqual(f('\\\\a'), ('', '\\', 'a'))


#
# Tests for the concrete classes.
#

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
only_nt = unittest.skipIf(os.name != 'nt', 'test requires a Windows-compatible system')
only_posix = unittest.skipIf(os.name == 'nt', 'test requires a POSIX-compatible system')
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

	def test_home(self):
		p = PathPlus.home()
		self._test_home(p)

	def test_samefile(self):
		fileA_path = os.path.join(BASE, 'fileA')
		fileB_path = os.path.join(BASE, 'dirB', 'fileB')
		p = PathPlus(fileA_path)
		pp = PathPlus(fileA_path)
		q = PathPlus(fileB_path)
		self.assertTrue(p.samefile(fileA_path))
		self.assertTrue(p.samefile(pp))
		self.assertFalse(p.samefile(fileB_path))
		self.assertFalse(p.samefile(q))
		# Test the non-existent file case
		non_existent = os.path.join(BASE, 'foo')
		r = PathPlus(non_existent)
		self.assertRaises(FileNotFoundError, p.samefile, r)
		self.assertRaises(FileNotFoundError, p.samefile, non_existent)
		self.assertRaises(FileNotFoundError, r.samefile, p)
		self.assertRaises(FileNotFoundError, r.samefile, non_existent)
		self.assertRaises(FileNotFoundError, r.samefile, r)
		self.assertRaises(FileNotFoundError, r.samefile, non_existent)

	def test_empty_path(self):
		# The empty path points to '.'
		p = PathPlus('')
		self.assertEqual(p.stat(), os.stat('.'))

	def test_expanduser_common(self):
		P = PathPlus
		p = P('~')
		self.assertEqual(p.expanduser(), P(os.path.expanduser('~')))
		p = P('foo')
		self.assertEqual(p.expanduser(), p)
		p = P('/~')
		self.assertEqual(p.expanduser(), p)
		p = P('../~')
		self.assertEqual(p.expanduser(), p)
		p = P(P('').absolute().anchor) / '~'
		self.assertEqual(p.expanduser(), p)

	def test_exists(self):
		P = PathPlus
		p = P(BASE)
		self.assertIs(True, p.exists())
		self.assertIs(True, (p / 'dirA').exists())
		self.assertIs(True, (p / 'fileA').exists())
		self.assertIs(False, (p / 'fileA' / 'bah').exists())
		if not symlink_skip_reason:
			self.assertIs(True, (p / 'linkA').exists())
			self.assertIs(True, (p / 'linkB').exists())
			self.assertIs(True, (p / 'linkB' / 'fileB').exists())
			self.assertIs(False, (p / 'linkA' / 'bah').exists())
		self.assertIs(False, (p / 'foo').exists())
		self.assertIs(False, P('/xyzzy').exists())

	def test_open_common(self):
		p = PathPlus(BASE)
		with (p / 'fileA').open('r') as f:
			self.assertIsInstance(f, io.TextIOBase)
			self.assertEqual(f.read(), "this is file A\n")
		with (p / 'fileA').open('rb') as f:
			self.assertIsInstance(f, io.BufferedIOBase)
			self.assertEqual(f.read().strip(), b"this is file A")
		with (p / 'fileA').open('rb', buffering=0) as f:
			self.assertIsInstance(f, io.RawIOBase)
			self.assertEqual(f.read().strip(), b"this is file A")

	def test_read_write_bytes(self):
		p = PathPlus(BASE)
		(p / 'fileA').write_bytes(b'abcdefg')
		self.assertEqual((p / 'fileA').read_bytes(), b'abcdefg')
		# Check that trying to write str does not truncate the file.
		self.assertRaises(TypeError, (p / 'fileA').write_bytes, 'somestr')
		self.assertEqual((p / 'fileA').read_bytes(), b'abcdefg')

	def test_read_write_text(self):
		p = PathPlus(BASE)
		(p / 'fileA').write_text('äbcdefg', encoding='latin-1')
		self.assertEqual((p / 'fileA').read_text(encoding='utf-8', errors='ignore'), 'bcdefg')
		# Check that trying to write bytes does not truncate the file.
		self.assertRaises(TypeError, (p / 'fileA').write_text, b'somebytes')
		self.assertEqual((p / 'fileA').read_text(encoding='latin-1'), 'äbcdefg')

	def test_iterdir(self):
		P = PathPlus
		p = P(BASE)
		it = p.iterdir()
		paths = set(it)
		expected = ['dirA', 'dirB', 'dirC', 'dirE', 'fileA']
		if not symlink_skip_reason:
			expected += ['linkA', 'linkB', 'brokenLink']
		self.assertEqual(paths, {P(BASE, q) for q in expected})

	@with_symlinks
	def test_iterdir_symlink(self):
		# __iter__ on a symlink to a directory.
		P = PathPlus
		p = P(BASE, 'linkB')
		paths = set(p.iterdir())
		expected = {P(BASE, 'linkB', q) for q in ['fileB', 'linkD']}
		self.assertEqual(paths, expected)

	def test_iterdir_nodir(self):
		# __iter__ on something that is not a directory.
		p = PathPlus(BASE, 'fileA')
		with self.assertRaises(OSError) as cm:
			next(p.iterdir())
		# ENOENT or EINVAL under Windows, ENOTDIR otherwise
		# (see issue #12802).
		self.assertIn(cm.exception.errno, (errno.ENOTDIR, errno.ENOENT, errno.EINVAL))

	def test_glob_common(self):

		def _check(glob, expected):
			self.assertEqual(set(glob), {P(BASE, q) for q in expected})

		P = PathPlus
		p = P(BASE)
		it = p.glob("fileA")
		self.assertIsInstance(it, collections.abc.Iterator)
		_check(it, ["fileA"])
		_check(p.glob("fileB"), [])
		_check(p.glob("dir*/file*"), ["dirB/fileB", "dirC/fileC"])
		if symlink_skip_reason:
			_check(p.glob("*A"), ['dirA', 'fileA'])
		else:
			_check(p.glob("*A"), ['dirA', 'fileA', 'linkA'])
		if symlink_skip_reason:
			_check(p.glob("*B/*"), ['dirB/fileB'])
		else:
			_check(p.glob("*B/*"), ['dirB/fileB', 'dirB/linkD', 'linkB/fileB', 'linkB/linkD'])
		if symlink_skip_reason:
			_check(p.glob("*/fileB"), ['dirB/fileB'])
		else:
			_check(p.glob("*/fileB"), ['dirB/fileB', 'linkB/fileB'])

	def test_rglob_common(self):

		def _check(glob, expected):
			self.assertEqual(set(glob), {P(BASE, q) for q in expected})

		P = PathPlus
		p = P(BASE)
		it = p.rglob("fileA")
		self.assertIsInstance(it, collections.abc.Iterator)
		_check(it, ["fileA"])
		_check(p.rglob("fileB"), ["dirB/fileB"])
		_check(p.rglob("*/fileA"), [])
		if symlink_skip_reason:
			_check(p.rglob("*/fileB"), ["dirB/fileB"])
		else:
			_check(p.rglob("*/fileB"), ["dirB/fileB", "dirB/linkD/fileB", "linkB/fileB", "dirA/linkC/fileB"])
		_check(p.rglob("file*"), ["fileA", "dirB/fileB", "dirC/fileC", "dirC/dirD/fileD"])
		p = P(BASE, "dirC")
		_check(p.rglob("file*"), ["dirC/fileC", "dirC/dirD/fileD"])
		_check(p.rglob("*/*"), ["dirC/dirD/fileD"])

	@with_symlinks
	def test_rglob_symlink_loop(self):
		# Don't get fooled by symlink loops (Issue #26012).
		P = PathPlus
		p = P(BASE)
		given = set(p.rglob('*'))
		expect = {
				'brokenLink',
				'dirA',
				'dirA/linkC',
				'dirB',
				'dirB/fileB',
				'dirB/linkD',
				'dirC',
				'dirC/dirD',
				'dirC/dirD/fileD',
				'dirC/fileC',
				'dirE',
				'fileA',
				'linkA',
				'linkB',
				}
		self.assertEqual(given, {p / x for x in expect})

	def test_glob_dotdot(self):
		# ".." is not special in globs.
		P = PathPlus
		p = P(BASE)
		self.assertEqual(set(p.glob("..")), {P(BASE, "..")})
		self.assertEqual(set(p.glob("dirA/../file*")), {P(BASE, "dirA/../fileA")})
		self.assertEqual(set(p.glob("../xyzzy")), set())

	def _check_resolve(self, p, expected, strict=True):
		q = p.resolve(strict)
		self.assertEqual(q, expected)

	# This can be used to check both relative and absolute resolutions.
	_check_resolve_relative = _check_resolve_absolute = _check_resolve

	@with_symlinks
	def test_resolve_common(self):
		P = PathPlus
		p = P(BASE, 'foo')
		with self.assertRaises(OSError) as cm:
			p.resolve(strict=True)
		self.assertEqual(cm.exception.errno, errno.ENOENT)
		# Non-strict
		self.assertEqual(str(p.resolve(strict=False)), os.path.join(BASE, 'foo'))
		p = P(BASE, 'foo', 'in', 'spam')
		self.assertEqual(str(p.resolve(strict=False)), os.path.join(BASE, 'foo', 'in', 'spam'))
		p = P(BASE, '..', 'foo', 'in', 'spam')
		self.assertEqual(str(p.resolve(strict=False)), os.path.abspath(os.path.join('foo', 'in', 'spam')))
		# These are all relative symlinks
		p = P(BASE, 'dirB', 'fileB')
		self._check_resolve_relative(p, p)
		p = P(BASE, 'linkA')
		self._check_resolve_relative(p, P(BASE, 'fileA'))
		p = P(BASE, 'dirA', 'linkC', 'fileB')
		self._check_resolve_relative(p, P(BASE, 'dirB', 'fileB'))
		p = P(BASE, 'dirB', 'linkD', 'fileB')
		self._check_resolve_relative(p, P(BASE, 'dirB', 'fileB'))
		# Non-strict
		p = P(BASE, 'dirA', 'linkC', 'fileB', 'foo', 'in', 'spam')
		self._check_resolve_relative(p, P(BASE, 'dirB', 'fileB', 'foo', 'in', 'spam'), False)
		p = P(BASE, 'dirA', 'linkC', '..', 'foo', 'in', 'spam')
		if os.name == 'nt':
			# In Windows, if linkY points to dirB, 'dirA\linkY\..'
			# resolves to 'dirA' without resolving linkY first.
			self._check_resolve_relative(p, P(BASE, 'dirA', 'foo', 'in', 'spam'), False)
		else:
			# In Posix, if linkY points to dirB, 'dirA/linkY/..'
			# resolves to 'dirB/..' first before resolving to parent of dirB.
			self._check_resolve_relative(p, P(BASE, 'foo', 'in', 'spam'), False)
		# Now create absolute symlinks.
		d = support._longpath(tempfile.mkdtemp(suffix='-dirD', dir=os.getcwd()))
		self.addCleanup(support.rmtree, d)
		os.symlink(os.path.join(d), join('dirA', 'linkX'))
		os.symlink(join('dirB'), os.path.join(d, 'linkY'))
		p = P(BASE, 'dirA', 'linkX', 'linkY', 'fileB')
		self._check_resolve_absolute(p, P(BASE, 'dirB', 'fileB'))
		# Non-strict
		p = P(BASE, 'dirA', 'linkX', 'linkY', 'foo', 'in', 'spam')
		self._check_resolve_relative(p, P(BASE, 'dirB', 'foo', 'in', 'spam'), False)
		p = P(BASE, 'dirA', 'linkX', 'linkY', '..', 'foo', 'in', 'spam')
		if os.name == 'nt':
			# In Windows, if linkY points to dirB, 'dirA\linkY\..'
			# resolves to 'dirA' without resolving linkY first.
			self._check_resolve_relative(p, P(d, 'foo', 'in', 'spam'), False)
		else:
			# In Posix, if linkY points to dirB, 'dirA/linkY/..'
			# resolves to 'dirB/..' first before resolving to parent of dirB.
			self._check_resolve_relative(p, P(BASE, 'foo', 'in', 'spam'), False)

	@with_symlinks
	def test_resolve_dot(self):
		# See https://bitbucket.org/pitrou/pathlib/issue/9/pathresolve-fails-on-complex-symlinks
		p = PathPlus(BASE)
		self.dirlink('.', join('0'))
		self.dirlink(os.path.join('0', '0'), join('1'))
		self.dirlink(os.path.join('1', '1'), join('2'))
		q = p / '2'
		self.assertEqual(q.resolve(strict=True), p)
		r = q / '3' / '4'
		self.assertRaises(FileNotFoundError, r.resolve, strict=True)
		# Non-strict
		self.assertEqual(r.resolve(strict=False), p / '3' / '4')

	def test_with(self):
		p = PathPlus(BASE)
		it = p.iterdir()
		it2 = p.iterdir()
		next(it2)
		with p:
			pass
		# I/O operation on closed path
		self.assertRaises(ValueError, next, it)
		self.assertRaises(ValueError, next, it2)
		self.assertRaises(ValueError, p.open)
		self.assertRaises(ValueError, p.resolve)
		self.assertRaises(ValueError, p.absolute)
		self.assertRaises(ValueError, p.__enter__)

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

	def test_rmdir(self):
		p = PathPlus(BASE) / 'dirA'
		for q in p.iterdir():
			q.unlink()
		p.rmdir()
		self.assertFileNotFound(p.stat)
		self.assertFileNotFound(p.unlink)

	def test_rename(self):
		P = PathPlus(BASE)
		p = P / 'fileA'
		size = p.stat().st_size
		# Renaming to another path.
		q = P / 'dirA' / 'fileAA'
		p.rename(q)
		self.assertEqual(q.stat().st_size, size)
		self.assertFileNotFound(p.stat)
		# Renaming to a str of a relative path.
		r = rel_join('fileAAA')
		q.rename(r)
		self.assertEqual(os.stat(r).st_size, size)
		self.assertFileNotFound(q.stat)

	def test_replace(self):
		P = PathPlus(BASE)
		p = P / 'fileA'
		size = p.stat().st_size
		# Replacing a non-existing path.
		q = P / 'dirA' / 'fileAA'
		p.replace(q)
		self.assertEqual(q.stat().st_size, size)
		self.assertFileNotFound(p.stat)
		# Replacing another (existing) path.
		r = rel_join('dirB', 'fileB')
		q.replace(r)
		self.assertEqual(os.stat(r).st_size, size)
		self.assertFileNotFound(q.stat)

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
			self.assertFalse((P / 'brokenLink').is_dir())

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

	def test_parts_interning(self):
		P = PathPlus
		p = P('/usr/bin/foo')
		q = P('/usr/local/bin')
		# 'usr'
		self.assertIs(p.parts[1], q.parts[1])
		# 'bin'
		self.assertIs(p.parts[2], q.parts[3])

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


if __name__ == "__main__":  # pragma: no cover
	unittest.main()
