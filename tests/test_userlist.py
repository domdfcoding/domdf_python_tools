#  From https://raw.githubusercontent.com/python/cpython/master/Lib/test/test_userlist.py

#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.

# Check every path through every method of UserList

# stdlib
from typing import Sequence, Type, no_type_check

# 3rd party
from coincidence.selectors import not_pypy

# this package
from domdf_python_tools.bases import Lineup, UserList
from tests import list_tests


class TestList(list_tests.CommonTest):
	type2test: Type[Sequence] = list

	def test_getslice(self):
		super().test_getslice()
		l = [0, 1, 2, 3, 4]
		u = self.type2test(l)  # type: ignore
		for i in range(-3, 6):
			assert u[:i] == l[:i]
			assert u[i:] == l[i:]
			for j in range(-3, 6):
				assert u[i:j] == l[i:j]

	def test_slice_type(self):
		l = [0, 1, 2, 3, 4]
		u = self.type2test(l)  # type: ignore
		assert u[:] != u.__class__
		assert u[:] == u

	@not_pypy("Doesn't work on PyPy")
	def test_iadd(self):
		super().test_iadd()
		u = [0, 1]
		u += self.type2test([0, 1])  # type: ignore
		assert u == [0, 1, 0, 1]

	@no_type_check
	def test_mixedcmp(self):
		u = self.type2test([0, 1])
		assert u == [0, 1]
		assert u != [0]
		assert u != [0, 2]

	@no_type_check
	def test_mixedadd(self):
		u = self.type2test([0, 1])
		assert u + [] == u
		assert u + [2] == [0, 1, 2]

	@no_type_check
	def test_userlist_copy(self):
		u = self.type2test([6, 8, 1, 9, 1])
		v = u.copy()
		assert u == v
		assert type(u) == type(v)  # pylint: disable=unidiomatic-typecheck


class TestUserList(TestList):
	type2test: Type[UserList] = UserList

	def test_add_specials(self):
		u = UserList("spam")
		u2 = u + "eggs"
		assert u2 == list("spameggs")

	def test_radd_specials(self):
		u = UserList("eggs")
		u2 = "spam" + u
		assert u2 == list("spameggs")
		u2 = u.__radd__(UserList("spam"))
		assert u2 == list("spameggs")


class TestLineup(TestList):
	type2test: Type[Lineup] = Lineup

	def test_replace(self):
		u = self.type2test([-2, -1, 0, 1, 2])

		u.replace(2, 3)
		assert u[-1] == 3

	def test_fluent(self):
		u = self.type2test([2, 1, 0, -1, -2])

		assert u.sort() is u
		assert u == [-2, -1, 0, 1, 2]

		assert u.replace(2, 3) is u
		assert u == [-2, -1, 0, 1, 3]

		assert u.reverse() is u
		assert u == [3, 1, 0, -1, -2]

		assert u.append(4) is u
		assert u == [3, 1, 0, -1, -2, 4]

		assert u.insert(0, -3) is u
		assert u == [-3, 3, 1, 0, -1, -2, 4]
