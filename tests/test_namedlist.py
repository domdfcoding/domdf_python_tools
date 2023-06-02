#  From https://raw.githubusercontent.com/python/cpython/master/Lib/test/test_userlist.py
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.

# Check every path through every method of UserList

# stdlib
import sys
from typing import Callable, Type, Union

# this package
from domdf_python_tools.bases import NamedList, UserList, namedlist
from domdf_python_tools.utils import printr, printt
from tests.test_userlist import TestList


class TestNamedList(TestList):
	type2test: Type[NamedList] = NamedList

	def test_add_specials(self):
		u = NamedList("spam")
		u2 = u + "eggs"
		assert u2 == list("spameggs")

	def test_radd_specials(self):
		u = NamedList("eggs")
		u2 = "spam" + u
		assert u2 == list("spameggs")
		u2 = u.__radd__(NamedList("spam"))
		assert u2 == list("spameggs")

	def test_repr(self):
		a0 = self.type2test([])
		a1 = self.type2test([0, 1, 2])

		assert str(a0) == "NamedList[]"
		assert repr(a0) == "[]"

		assert str(a1) == "NamedList[0, 1, 2]"
		assert repr(a1) == "[0, 1, 2]"

		a1.append(a1)
		a1.append(3)
		assert str(a1) == "NamedList[0, 1, 2, [0, 1, 2, [...], 3], 3]"
		assert repr(a1) == "[0, 1, 2, [...], 3]"


class ShoppingList(NamedList):
	pass


class TestShoppingList(TestNamedList):
	"""
	Test a subclass of NamedList.
	"""

	type2test: Type[ShoppingList] = ShoppingList

	def test_repr(self):
		a0 = self.type2test([])
		a1 = self.type2test([0, 1, 2])

		assert str(a0) == "ShoppingList[]"
		assert repr(a0) == "[]"

		assert str(a1) == "ShoppingList[0, 1, 2]"
		assert repr(a1) == "[0, 1, 2]"

		a1.append(a1)
		a1.append(3)
		assert str(a1) == "ShoppingList[0, 1, 2, [0, 1, 2, [...], 3], 3]"
		assert repr(a1) == "[0, 1, 2, [...], 3]"


class NamedListTest:
	shopping_list: Union[NamedList[str], Callable]

	repr_out = "['egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam']"
	str_out = "ShoppingList['egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam']"
	cls_str: str

	def test_(self, capsys):
		assert isinstance(self.shopping_list, UserList)
		assert self.shopping_list[0] == "egg and bacon"

		printt(self.shopping_list)
		printr(self.shopping_list)
		print(self.shopping_list)

		captured = capsys.readouterr()
		stdout = captured.out.split('\n')

		assert stdout[0] == self.cls_str
		assert str(type(self.shopping_list)) == self.cls_str

		assert stdout[1] == self.repr_out
		assert stdout[2] == self.str_out

		assert repr(self.shopping_list) == self.repr_out
		assert str(self.shopping_list) == self.str_out


class TestNamedListFunction(NamedListTest):
	if sys.version_info[:2] == (3, 6):
		cls_str = "domdf_python_tools.bases.namedlist.<locals>.cls"
	else:
		cls_str = "<class 'domdf_python_tools.bases.namedlist.<locals>.cls'>"

	repr_out = "['egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam']"
	str_out = "ShoppingList['egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam']"

	mylist = namedlist()
	assert isinstance(mylist(), UserList)

	ShoppingList = namedlist("ShoppingList")
	shopping_list = ShoppingList(["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"])


class TestNamedlistSubclassFunction:

	class ShoppingList(namedlist()):  # type: ignore
		pass

	shopping_list = ShoppingList(["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"])

	if sys.version_info[:2] == (3, 6):
		cls_str = "tests.test_bases.test_namedlist_subclass_function.<locals>.ShoppingList"
	else:
		cls_str = "<class 'tests.test_bases.test_namedlist_subclass_function.<locals>.ShoppingList'>"

	repr_out = "['egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam']"
	str_out = "ShoppingList['egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam']"


class TestNamedlistSubclassClass:

	class ShoppingList(NamedList):
		pass

	shopping_list = ShoppingList(["egg and bacon", "egg sausage and bacon", "egg and spam", "egg bacon and spam"])

	if sys.version_info[:2] == (3, 6):
		cls_str = "tests.test_bases.test_namedlist_subclass_class.<locals>.ShoppingList"
	else:
		cls_str = "<class 'tests.test_bases.test_namedlist_subclass_class.<locals>.ShoppingList'>"

	repr_out = "['egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam']"
	str_out = "ShoppingList['egg and bacon', 'egg sausage and bacon', 'egg and spam', 'egg bacon and spam']"
