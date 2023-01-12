#  Adapted from https://github.com/python/cpython/blob/master/Lib/test/test_operator.py
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#

# stdlib
import pickle
from typing import Any

# 3rd party
import pytest
from funcy.funcs import rpartial  # type: ignore

# this package
import domdf_python_tools
from domdf_python_tools.getters import attrgetter, itemgetter, methodcaller

evaluate = rpartial(eval, {"domdf_python_tools": domdf_python_tools}, {"domdf_python_tools": domdf_python_tools})


class TestAttrgetter:

	def test_attrgetter(self):

		class A:
			pass

		a = A()
		a.name = "john"  # type: ignore

		b = A()
		b.name = "graham"  # type: ignore

		f = attrgetter(0, "name")
		assert f([a, b]) == "john"

		f = attrgetter(1, "name")
		assert f([a, b]) == "graham"

		with pytest.raises(TypeError, match=r"__call__\(\) missing 1 required positional argument: 'obj'"):
			f()  # type: ignore

		with pytest.raises(TypeError, match=r"__call__\(\) takes 2 positional arguments but 3 were given"):
			f(a, "cleese")  # type: ignore

		with pytest.raises(TypeError, match=r"__call__\(\) got an unexpected keyword argument 'surname'"):
			f(a, surname="cleese")  # type: ignore

		f = attrgetter(0, "rank")

		with pytest.raises(AttributeError, match="'A' object has no attribute 'rank'"):
			f([a, b])

		with pytest.raises(TypeError, match="attribute name must be a string"):
			attrgetter(0, 2)  # type: ignore[arg-type]

		with pytest.raises(TypeError, match="'idx' must be an integer"):
			attrgetter("hello", 0)  # type: ignore[arg-type]

		with pytest.raises(TypeError, match=r"__init__\(\) missing 1 required positional argument: 'attr'"):
			attrgetter(0)  # type: ignore[call-arg]

		f = attrgetter(1, "name")

		with pytest.raises(IndexError, match="list index out of range"):
			f([])

		class C:

			def __getattr__(self, name):
				raise SyntaxError

		with pytest.raises(SyntaxError, match="None"):
			attrgetter(0, "foo")([C()])

		# recursive gets
		a = A()
		a.name = "john"  # type: ignore
		a.child = A()  # type: ignore
		a.child.name = "thomas"  # type: ignore
		f = attrgetter(3, "child.name")

		assert f([1, 2, 3, a]) == "thomas"

		with pytest.raises(AttributeError, match="'A' object has no attribute 'child'"):
			f([1, 2, 3, a.child])  # type: ignore

		f = attrgetter(1, "child.name")

		assert f([1, a]) == "thomas"

		f = attrgetter(2, "child.child.name")

		with pytest.raises(AttributeError, match="'A' object has no attribute 'child'"):
			f([1, 2, a])

		f = attrgetter(0, "child.")
		with pytest.raises(AttributeError, match="'A' object has no attribute ''"):
			f([a])

		f = attrgetter(0, ".child")
		with pytest.raises(AttributeError, match="'A' object has no attribute ''"):
			f([a])

		a.child.child = A()  # type: ignore
		a.child.child.name = "johnson"  # type: ignore

		f = attrgetter(0, "child.child.name")
		assert f([a]) == "johnson"

	@pytest.mark.parametrize("proto", range(pickle.HIGHEST_PROTOCOL + 1))
	def test_pickle(self, proto: int):

		class A:
			pass

		a = A()
		a.x = 'X'  # type: ignore
		a.y = 'Y'  # type: ignore
		a.z = 'Z'  # type: ignore
		a.t = A()  # type: ignore
		a.t.u = A()  # type: ignore
		a.t.u.v = 'V'  # type: ignore

		f = attrgetter(0, 'x')
		f2 = copy(f, proto)
		assert repr(f2) == repr(f)
		assert f2([a]) == f([a])

	def test_repr(self):
		assert repr(attrgetter(0, "name")) == "domdf_python_tools.getters.attrgetter(idx=0, attr='name')"
		assert repr(attrgetter(1, "value")) == "domdf_python_tools.getters.attrgetter(idx=1, attr='value')"

		evaluate(repr(attrgetter(0, "name")))
		evaluate(repr(attrgetter(1, "value")))


class TestItemgetter:

	def test_itemgetter(self):

		a = "ABCDE"
		f = itemgetter(0, 2)
		assert f([a]) == 'C'

		f = itemgetter(2, 2)
		assert f([1, 2, a]) == 'C'

		with pytest.raises(TypeError, match=r"__call__\(\) missing 1 required positional argument: 'obj'"):
			f()  # type: ignore

		with pytest.raises(TypeError, match=r"__call__\(\) takes 2 positional arguments but 3 were given"):
			f(a, 3)  # type: ignore

		with pytest.raises(TypeError, match=r"__call__\(\) got an unexpected keyword argument 'size'"):
			f(a, size=3)  # type: ignore

		f = itemgetter(1, 10)

		with pytest.raises(IndexError, match="list index out of range"):
			f([])

		with pytest.raises(IndexError, match="list index out of range"):
			f([1])

		with pytest.raises(IndexError, match="string index out of range"):
			f([(), a])

		class C:

			def __getitem__(self, name):
				raise SyntaxError

		with pytest.raises(SyntaxError, match="None"):
			itemgetter(2, 42)([1, (), C()])

		f = itemgetter(0, "name")

		with pytest.raises(TypeError, match="string( index)? indices must be integers( or slices, not str)?"):
			f([a])

		with pytest.raises(
				TypeError,
				match=r"__init__\(\) missing 2 required positional arguments: 'idx' and 'item'",
				):
			itemgetter()  # type: ignore

		with pytest.raises(TypeError, match=r"__init__\(\) missing 1 required positional argument: 'item'"):
			itemgetter(1)  # type: ignore

		with pytest.raises(TypeError, match=r"__init__\(\) missing 1 required positional argument: 'item'"):
			itemgetter("abc")  # type: ignore

		with pytest.raises(TypeError, match="'idx' must be an integer"):
			itemgetter("abc", 2)  # type: ignore

		d = dict(key="val")

		f = itemgetter(1, "key")
		assert f([{}, d]) == "val"

		f = itemgetter(1, "nonkey")
		with pytest.raises(KeyError, match="nonkey"):
			f([{}, d])

		inventory = [("apple", 3), ("pear", 5), ("banana", 2), ("orange", 1)]
		getcount = itemgetter(0, 1)
		assert list(map(getcount, inventory)) == ['p', 'e', 'a', 'r']
		assert sorted(inventory, key=getcount) == [("banana", 2), ("pear", 5), ("apple", 3), ("orange", 1)]

		# interesting indices
		t = tuple("abcde")
		assert itemgetter(-1, -1)([1, 2, t]) == 'e'
		assert itemgetter(1, slice(2, 4))([1, t]) == ('c', 'd')

		# interesting sequences
		class T(tuple):
			"""
			Tuple subclass
			"""

		assert itemgetter(2, 0)([T("abc"), T("def"), T("ghi")]) == 'g'
		assert itemgetter(2, 0)([range(100, 200), range(200, 300), range(300, 400)]) == 300

	@pytest.mark.parametrize("proto", range(pickle.HIGHEST_PROTOCOL + 1))
	def test_pickle(self, proto: int):
		a = "ABCDE"

		f = itemgetter(0, 2)
		f2 = copy(f, proto)
		assert repr(f2) == repr(f)
		assert f2([a]) == f([a])

	def test_repr(self):
		assert repr(itemgetter(0, 1)) == "domdf_python_tools.getters.itemgetter(idx=0, item=1)"
		assert repr(itemgetter(1, 2)) == "domdf_python_tools.getters.itemgetter(idx=1, item=2)"

		evaluate(repr(itemgetter(0, 1)))
		evaluate(repr(itemgetter(1, 2)))


class TestMethodcaller:

	def test_methodcaller(self):

		with pytest.raises(
				TypeError,
				match=r"__init__\(\) missing 2 required positional arguments: '_idx' and '_name'",
				):
			methodcaller()  # type: ignore

		with pytest.raises(TypeError, match=r"__init__\(\) missing 1 required positional argument: '_name'"):
			methodcaller(12)  # type: ignore

		with pytest.raises(TypeError, match=r"__init__\(\) missing 1 required positional argument: '_name'"):
			methodcaller("name")  # type: ignore

		with pytest.raises(TypeError, match="'_idx' must be an integer"):
			methodcaller("name", 12)  # type: ignore

		with pytest.raises(TypeError, match="method name must be a string"):
			methodcaller(0, 12)  # type: ignore

		f = methodcaller(1, "foo")

		with pytest.raises(IndexError, match="list index out of range"):
			f([])

		with pytest.raises(IndexError, match="list index out of range"):
			f([1])

		class A:

			def foo(self, *args, **kwds):
				return args[0] + args[1]

			def bar(self, f=42):  # noqa: MAN001,MAN002
				return f

			def baz(*args, **kwds):  # noqa: MAN002
				return kwds["name"], kwds["self"]

		a = A()
		f = methodcaller(2, "foo")

		with pytest.raises(IndexError, match="tuple index out of range"):
			f(["abc", 123, a])

		f = methodcaller(1, "foo", 1, 2)
		assert f([1, a]) == 3

		with pytest.raises(TypeError, match=r"__call__\(\) missing 1 required positional argument: 'obj'"):
			f()  # type: ignore

		with pytest.raises(TypeError, match=r"__call__\(\) takes 2 positional arguments but 3 were given"):
			f(a, 3)  # type: ignore

		with pytest.raises(TypeError, match=r"__call__\(\) got an unexpected keyword argument 'spam'"):
			f(a, spam=3)  # type: ignore

		f = methodcaller(0, "bar")
		assert f([a]) == 42

		with pytest.raises(TypeError, match=r"__call__\(\) takes 2 positional arguments but 3 were given"):
			f([a], [a])  # type: ignore

		f = methodcaller(0, "bar", f=5)
		assert f([a]) == 5

		f = methodcaller(0, "baz", name="spam", self="eggs")
		assert f([a]) == ("spam", "eggs")

	@pytest.mark.parametrize("proto", range(pickle.HIGHEST_PROTOCOL + 1))
	def test_pickle(self, proto: int):

		class A:

			def foo(self, *args, **kwds):
				return args[0] + args[1]

			def bar(self, f=42):
				return f

			def baz(*args, **kwds):
				return kwds["name"], kwds["self"]

		a = A()

		f = methodcaller(0, "bar")
		f2 = copy(f, proto)
		assert repr(f2) == repr(f)
		assert f2([a]) == f([a])

		# positional args
		f = methodcaller(0, "foo", 1, 2)
		f2 = copy(f, proto)
		assert repr(f2) == repr(f)
		assert f2([a]) == f([a])

		# keyword args
		f = methodcaller(0, "bar", f=5)
		f2 = copy(f, proto)
		assert repr(f2) == repr(f)
		assert f2([a]) == f([a])
		f = methodcaller(0, "baz", self="eggs", name="spam")
		f2 = copy(f, proto)

		# Can't test repr consistently with multiple keyword args
		assert f2([a]) == f([a])

	def test_repr(self):
		assert repr(methodcaller(0, "lower")) == "domdf_python_tools.getters.methodcaller(0, 'lower')"
		assert repr(methodcaller(1, "__iter__")) == "domdf_python_tools.getters.methodcaller(1, '__iter__')"
		assert repr(
				methodcaller(1, "__iter__", "arg1")
				) == "domdf_python_tools.getters.methodcaller(1, '__iter__', 'arg1')"
		assert repr(
				methodcaller(1, "__iter__", kw1="kwarg1")
				) == "domdf_python_tools.getters.methodcaller(1, '__iter__', kw1='kwarg1')"
		assert repr(
				methodcaller(1, "__iter__", "arg1", "arg2", kw1="kwarg1", kw2="kwarg2")
				) == "domdf_python_tools.getters.methodcaller(1, '__iter__', 'arg1', 'arg2', kw1='kwarg1', kw2='kwarg2')"

		evaluate(repr(methodcaller(0, "lower")))
		evaluate(repr(methodcaller(1, "__iter__")))
		evaluate(repr(methodcaller(1, "__iter__", "arg1")))
		evaluate(repr(methodcaller(1, "__iter__", kw1="kwarg1")))
		evaluate(repr(methodcaller(1, "__iter__", "arg1", "arg2", kw1="kwarg1", kw2="kwarg2")))


def copy(obj: Any, proto: int):
	pickled = pickle.dumps(obj, proto)
	return pickle.loads(pickled)  # nosec: B301
