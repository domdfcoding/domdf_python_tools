#  From https://raw.githubusercontent.com/python/cpython/master/Lib/test/list_tests.py

#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
"""
Tests common to list and UserList.UserList
"""

# stdlib
import sys
from functools import cmp_to_key
from typing import List, no_type_check

# 3rd party
import pytest
from coincidence.selectors import not_pypy

# this package
from tests import seq_tests
from tests.seq_tests import ALWAYS_EQ, NEVER_EQ


class CommonTest(seq_tests.CommonTest):

	def test_init(self):
		# Iterable arg is optional
		assert self.type2test([]) == self.type2test()

		# Init clears previous values
		a = self.type2test([1, 2, 3])
		a.__init__()
		assert a == self.type2test([])

		# Init overwrites previous values
		a = self.type2test([1, 2, 3])
		a.__init__([4, 5, 6])
		assert a == self.type2test([4, 5, 6])

		# Mutables always return a new object
		b = self.type2test(a)
		assert id(a) != id(b)
		assert a == b

	@no_type_check
	def test_getitem_error(self):
		a = []
		with pytest.raises(TypeError, match="list indices must be integers or slices"):
			a['a']  # pylint: disable=pointless-statement

	@no_type_check
	def test_setitem_error(self):
		a = []
		with pytest.raises(TypeError, match="list indices must be integers or slices"):
			a['a'] = "python"

	def test_repr(self):
		l0: List = []
		l2 = [0, 1, 2]
		a0 = self.type2test(l0)
		a2 = self.type2test(l2)

		assert str(a0) == str(l0)
		assert repr(a0) == repr(l0)
		assert repr(a2) == repr(l2)
		assert str(a2) == "[0, 1, 2]"
		assert repr(a2) == "[0, 1, 2]"

		a2.append(a2)
		a2.append(3)
		assert str(a2) == "[0, 1, 2, [...], 3]"
		assert repr(a2) == "[0, 1, 2, [...], 3]"

	@not_pypy()
	@pytest.mark.skipif(sys.version_info >= (3, 12), reason="Doesn't error on newer Pythons")
	def test_repr_deep(self):
		a = self.type2test([])
		for i in range(1500 + 1):  # sys.getrecursionlimit() + 100
			a = self.type2test([a])
		with pytest.raises(RecursionError):
			repr(a)

	def test_set_subscript(self):
		a = self.type2test(range(20))
		with pytest.raises(ValueError):
			a.__setitem__(slice(0, 10, 0), [1, 2, 3])
		with pytest.raises(TypeError):
			a.__setitem__(slice(0, 10), 1)
		with pytest.raises(ValueError):
			a.__setitem__(slice(0, 10, 2), [1, 2])
		with pytest.raises(TypeError):
			a.__getitem__('x', 1)
		a[slice(2, 10, 3)] = [1, 2, 3]
		assert a == self.type2test([0, 1, 1, 3, 4, 2, 6, 7, 3, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19])

	def test_reversed(self):
		a = self.type2test(range(20))
		r = reversed(a)
		assert list(r) == self.type2test(range(19, -1, -1))
		with pytest.raises(StopIteration):
			next(r)
		assert list(reversed(self.type2test())) == self.type2test()
		# Bug 3689: make sure list-reversed-iterator doesn't have __len__
		with pytest.raises(TypeError):
			len(reversed([1, 2, 3]))  # type: ignore

	def test_setitem(self):
		a = self.type2test([0, 1])
		a[0] = 0
		a[1] = 100
		assert a == self.type2test([0, 100])
		a[-1] = 200
		assert a == self.type2test([0, 200])
		a[-2] = 100
		assert a == self.type2test([100, 200])
		with pytest.raises(IndexError):
			a.__setitem__(-3, 200)
		with pytest.raises(IndexError):
			a.__setitem__(2, 200)

		a = self.type2test([])
		with pytest.raises(IndexError):
			a.__setitem__(0, 200)
		with pytest.raises(IndexError):
			a.__setitem__(-1, 200)
		with pytest.raises(TypeError):
			a.__setitem__()

		a = self.type2test([0, 1, 2, 3, 4])
		a[0] = 1
		a[1] = 2
		a[2] = 3
		assert a == self.type2test([1, 2, 3, 3, 4])
		a[0] = 5
		a[1] = 6
		a[2] = 7
		assert a == self.type2test([5, 6, 7, 3, 4])
		a[-2] = 88
		a[-1] = 99
		assert a == self.type2test([5, 6, 7, 88, 99])
		a[-2] = 8
		a[-1] = 9
		assert a == self.type2test([5, 6, 7, 8, 9])

		with pytest.raises(TypeError, match="list indices must be integers or slices"):
			a['a'] = "python"

	def test_delitem(self):
		a = self.type2test([0, 1])
		del a[1]
		assert a == [0]
		del a[0]
		assert a == []

		a = self.type2test([0, 1])
		del a[-2]
		assert a == [1]
		del a[-1]
		assert a == []

		a = self.type2test([0, 1])
		with pytest.raises(IndexError):
			a.__delitem__(-3)
		with pytest.raises(IndexError):
			a.__delitem__(2)

		a = self.type2test([])
		with pytest.raises(IndexError):
			a.__delitem__(0)

		with pytest.raises(TypeError):
			a.__delitem__()

	def test_setslice(self):
		l = [0, 1]
		a = self.type2test(l)

		for i in range(-3, 4):
			a[:i] = l[:i]
			assert a == l
			a2 = a[:]
			a2[:i] = a[:i]
			assert a2 == a
			a[i:] = l[i:]
			assert a == l
			a2 = a[:]
			a2[i:] = a[i:]
			assert a2 == a
			for j in range(-3, 4):
				a[i:j] = l[i:j]
				assert a == l
				a2 = a[:]
				a2[i:j] = a[i:j]
				assert a2 == a

		aa2 = a2[:]
		aa2[:0] = [-2, -1]
		assert aa2 == [-2, -1, 0, 1]
		aa2[0:] = []
		assert aa2 == []

		a = self.type2test([1, 2, 3, 4, 5])
		a[:-1] = a
		assert a == self.type2test([1, 2, 3, 4, 5, 5])
		a = self.type2test([1, 2, 3, 4, 5])
		a[1:] = a
		assert a == self.type2test([1, 1, 2, 3, 4, 5])
		a = self.type2test([1, 2, 3, 4, 5])
		a[1:-1] = a
		assert a == self.type2test([1, 1, 2, 3, 4, 5, 5])

		a = self.type2test([])
		a[:] = tuple(range(10))
		assert a == self.type2test(range(10))

		with pytest.raises(TypeError):
			a.__setitem__(slice(0, 1, 5))

		with pytest.raises(TypeError):
			a.__setitem__()

	def test_delslice(self):
		a = self.type2test([0, 1])
		del a[1:2]
		del a[0:1]
		assert a == self.type2test([])

		a = self.type2test([0, 1])
		del a[1:2]
		del a[0:1]
		assert a == self.type2test([])

		a = self.type2test([0, 1])
		del a[-2:-1]
		assert a == self.type2test([1])

		a = self.type2test([0, 1])
		del a[-2:-1]
		assert a == self.type2test([1])

		a = self.type2test([0, 1])
		del a[1:]
		del a[:1]
		assert a == self.type2test([])

		a = self.type2test([0, 1])
		del a[1:]
		del a[:1]
		assert a == self.type2test([])

		a = self.type2test([0, 1])
		del a[-1:]
		assert a == self.type2test([0])

		a = self.type2test([0, 1])
		del a[-1:]
		assert a == self.type2test([0])

		a = self.type2test([0, 1])
		del a[:]
		assert a == self.type2test([])

	def test_append(self):
		a = self.type2test([])
		a.append(0)
		a.append(1)
		a.append(2)
		assert a == self.type2test([0, 1, 2])

		with pytest.raises(TypeError):
			a.append()

	def test_extend(self):
		a1 = self.type2test([0])
		a2 = self.type2test((0, 1))
		a = a1[:]
		a.extend(a2)
		assert a == a1 + a2

		a.extend(self.type2test([]))
		assert a == a1 + a2

		a.extend(a)
		assert a == self.type2test([0, 0, 1, 0, 0, 1])

		a = self.type2test("spam")
		a.extend("eggs")
		assert a == list("spameggs")

		with pytest.raises(TypeError):
			a.extend(None)
		with pytest.raises(TypeError):
			a.extend()

		# overflow test. issue1621
		class CustomIter:

			def __iter__(self):  # noqa: MAN002
				return self

			def __next__(self):  # noqa: MAN002
				raise StopIteration

			def __length_hint__(self):  # noqa: MAN002
				return sys.maxsize

		a = self.type2test([1, 2, 3, 4])
		a.extend(CustomIter())
		assert a == [1, 2, 3, 4]

	def test_insert(self):
		a = self.type2test([0, 1, 2])
		a.insert(0, -2)
		a.insert(1, -1)
		a.insert(2, 0)
		assert a == [-2, -1, 0, 0, 1, 2]

		b = a[:]
		b.insert(-2, "foo")
		b.insert(-200, "left")
		b.insert(200, "right")
		assert b == self.type2test(["left", -2, -1, 0, 0, "foo", 1, 2, "right"])

		with pytest.raises(TypeError):
			a.insert()

	def test_pop(self):
		a = self.type2test([-1, 0, 1])
		a.pop()
		assert a == [-1, 0]
		a.pop(0)
		assert a == [0]
		with pytest.raises(IndexError):
			a.pop(5)
		a.pop(0)
		assert a == []
		with pytest.raises(IndexError):
			a.pop()
		with pytest.raises(TypeError):
			a.pop(42, 42)
		a = self.type2test([0, 10, 20, 30, 40])

	@not_pypy("Doesn't work on PyPy")
	def test_remove(self):
		a = self.type2test([0, 0, 1])
		a.remove(1)
		assert a == [0, 0]
		a.remove(0)
		assert a == [0]
		a.remove(0)
		assert a == []

		with pytest.raises(ValueError):
			a.remove(0)

		with pytest.raises(TypeError):
			a.remove()

		a = self.type2test([1, 2])
		with pytest.raises(ValueError):
			a.remove(NEVER_EQ)
		assert a == [1, 2]
		a.remove(ALWAYS_EQ)
		assert a == [2]
		a = self.type2test([ALWAYS_EQ])
		a.remove(1)
		assert a == []
		a = self.type2test([ALWAYS_EQ])
		a.remove(NEVER_EQ)
		assert a == []
		a = self.type2test([NEVER_EQ])
		with pytest.raises(ValueError):
			a.remove(ALWAYS_EQ)

		class BadExc(Exception):
			pass

		class BadCmp:

			def __eq__(self, other):  # noqa: MAN001,MAN002
				if other == 2:
					raise BadExc()
				return False

		a = self.type2test([0, 1, 2, 3])
		with pytest.raises(BadExc):
			a.remove(BadCmp())

		class BadCmp2:

			def __eq__(self, other):  # noqa: MAN001,MAN002
				raise BadExc()

		d = self.type2test("abcdefghcij")
		d.remove('c')
		assert d == self.type2test("abdefghcij")
		d.remove('c')
		assert d == self.type2test("abdefghij")
		with pytest.raises(ValueError):
			d.remove('c')
		assert d == self.type2test("abdefghij")

		# Handle comparison errors
		d = self.type2test(['a', 'b', BadCmp2(), 'c'])
		e = self.type2test(d)
		with pytest.raises(BadExc):
			d.remove('c')
		for x, y in zip(d, e):
			# verify that original order and values are retained.
			assert x is y

	@not_pypy("Doesn't work on PyPy")
	def test_index(self):
		super().test_index()
		a = self.type2test([-2, -1, 0, 0, 1, 2])
		a.remove(0)
		with pytest.raises(ValueError):
			a.index(2, 0, 4)
		assert a == self.type2test([-2, -1, 0, 1, 2])

		# Test modifying the list during index's iteration
		class EvilCmp:

			def __init__(self, victim):  # noqa: MAN001
				self.victim = victim

			def __eq__(self, other):  # noqa: MAN001,MAN002
				del self.victim[:]
				return False

		a = self.type2test()
		a[:] = [EvilCmp(a) for _ in range(100)]
		# This used to seg fault before patch #1005778
		with pytest.raises(ValueError):
			a.index(None)

	def test_reverse(self):
		u = self.type2test([-2, -1, 0, 1, 2])
		u2 = u[:]
		u.reverse()
		assert u == [2, 1, 0, -1, -2]
		u.reverse()
		assert u == u2

		with pytest.raises(TypeError):
			u.reverse(42)

	def test_clear(self):
		u = self.type2test([2, 3, 4])
		u.clear()
		assert u == []

		u = self.type2test([])
		u.clear()
		assert u == []

		u = self.type2test([])
		u.append(1)
		u.clear()
		u.append(2)
		assert u == [2]

		with pytest.raises(TypeError):
			u.clear(None)

	def test_copy(self):
		u = self.type2test([1, 2, 3])
		v = u.copy()
		assert v == [1, 2, 3]

		u = self.type2test([])
		v = u.copy()
		assert v == []

		# test that it's indeed a copy and not a reference
		u = self.type2test(['a', 'b'])
		v = u.copy()
		v.append('i')
		assert u == ['a', 'b']
		assert v == u + ['i']

		# test that it's a shallow, not a deep copy
		u = self.type2test([1, 2, [3, 4], 5])
		v = u.copy()
		assert u == v
		assert v[3] is u[3]

		with pytest.raises(TypeError):
			u.copy(None)

	def test_sort(self):
		u = self.type2test([1, 0])
		u.sort()
		assert u == [0, 1]

		u = self.type2test([2, 1, 0, -1, -2])
		u.sort()
		assert u == self.type2test([-2, -1, 0, 1, 2])

		with pytest.raises(TypeError):
			u.sort(42, 42)

		def revcmp(a, b):  # noqa: MAN001,MAN002
			if a == b:
				return 0
			elif a < b:
				return 1
			else:  # a > b
				return -1

		u.sort(key=cmp_to_key(revcmp))
		assert u == self.type2test([2, 1, 0, -1, -2])

		# The following dumps core in unpatched Python 1.5:
		def myComparison(x, y):
			xmod, ymod = x % 3, y % 7
			if xmod == ymod:
				return 0
			elif xmod < ymod:
				return -1
			else:  # xmod > ymod
				return 1

		z = self.type2test(range(12))
		z.sort(key=cmp_to_key(myComparison))

		with pytest.raises(TypeError):
			z.sort(2)

		with pytest.raises(TypeError):
			z.sort(42, 42, 42, 42)

	def test_slice(self):
		u = self.type2test("spam")
		u[:2] = 'h'
		assert u == list("ham")

	def test_iadd(self):
		super().test_iadd()
		u = self.type2test([0, 1])
		u2 = u
		u += [2, 3]
		assert u is u2

		u = self.type2test("spam")
		u += "eggs"
		assert u == self.type2test("spameggs")

		with pytest.raises(TypeError):
			u.__iadd__(None)

	def test_imul(self):
		super().test_imul()
		s = self.type2test([])
		oldid = id(s)
		s *= 10
		assert id(s) == oldid

	def test_extendedslicing(self):
		#  subscript
		a = self.type2test([0, 1, 2, 3, 4])

		#  deletion
		del a[::2]
		assert a == self.type2test([1, 3])
		a = self.type2test(range(5))
		del a[1::2]
		assert a == self.type2test([0, 2, 4])
		a = self.type2test(range(5))
		del a[1::-2]
		assert a == self.type2test([0, 2, 3, 4])
		a = self.type2test(range(10))
		del a[::1000]
		assert a == self.type2test([1, 2, 3, 4, 5, 6, 7, 8, 9])
		#  assignment
		a = self.type2test(range(10))
		a[::2] = [-1] * 5
		assert a == self.type2test([-1, 1, -1, 3, -1, 5, -1, 7, -1, 9])
		a = self.type2test(range(10))
		a[::-4] = [10] * 3
		assert a == self.type2test([0, 10, 2, 3, 4, 10, 6, 7, 8, 10])
		a = self.type2test(range(4))
		a[::-1] = a
		assert a == self.type2test([3, 2, 1, 0])
		a = self.type2test(range(10))
		b = a[:]
		c = a[:]
		a[2:3] = self.type2test(["two", "elements"])
		b[slice(2, 3)] = self.type2test(["two", "elements"])
		c[2:3:] = self.type2test(["two", "elements"])
		assert a == b
		assert a == c
		a = self.type2test(range(10))
		a[::2] = tuple(range(5))
		assert a == self.type2test([0, 1, 1, 3, 2, 5, 3, 7, 4, 9])
		# test issue7788
		a = self.type2test(range(10))
		del a[9::1 << 333]

	def test_constructor_exception_handling(self):
		# Bug #1242657
		class F:

			def __iter__(self):  # noqa: MAN002
				raise KeyboardInterrupt

		with pytest.raises(KeyboardInterrupt):
			list(F())

	def test_exhausted_iterator(self):
		a = self.type2test([1, 2, 3])
		exhit = iter(a)
		empit = iter(a)
		for x in exhit:  # exhaust the iterator
			next(empit)  # not exhausted
		a.append(9)
		assert list(exhit) == []
		assert list(empit) == [9]
		assert a == self.type2test([1, 2, 3, 9])
