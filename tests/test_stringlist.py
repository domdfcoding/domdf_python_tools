# stdlib
from textwrap import dedent

# 3rd party
import pytest

# this package
from domdf_python_tools.stringlist import Indent, StringList


class TestStringList:

	def test_creation(self):
		assert not StringList()
		assert not StringList([])
		assert not StringList(())

		assert StringList([1]) == ["1"]
		assert StringList(["1"]) == ["1"]
		assert StringList("1") == ["1"]
		assert StringList("1\n") == ["1", '']

		with pytest.raises(TypeError, match="'int' object is not iterable"):
			StringList(1)  # type: ignore

	def test_append(self):
		sl = StringList()

		sl.append("")
		assert sl == [""]

		sl.append("")
		assert sl == ["", '']

		sl.append("hello")
		assert sl == ["", '', "hello"]

		sl.append("world\n\n\n")
		assert sl == ["", '', "hello", "world", '', '', '']

		sl.append("1234")
		assert sl == ["", '', "hello", "world", '', '', '', "1234"]

	def test_insert(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])

		sl.insert(0, "foo")
		assert sl == ["foo", '', '', "hello", "world", '', '', '', "1234"]

		sl.insert(1, "bar")
		assert sl == ["foo", "bar", '', '', "hello", "world", '', '', '', "1234"]

		sl.insert(0, "1234")
		assert sl == ["1234", "foo", "bar", '', '', "hello", "world", '', '', '', "1234"]

		sl.insert(11, "baz")
		assert sl == ["1234", "foo", "bar", '', '', "hello", "world", '', '', '', "1234", "baz"]

		sl.insert(3, "\na line\n")
		assert sl == ["1234", "foo", "bar", '', "a line", '', '', '', "hello", "world", '', '', '', "1234", "baz"]

		sl.insert(100, "end")
		assert sl == [
				"1234", "foo", "bar", '', "a line", '', '', '', "hello", "world", '', '', '', "1234", "baz", "end"
				]

	def test_setitem(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])

		sl[0] = "foo"
		assert sl == ["foo", '', "hello", "world", '', '', '', "1234"]

		sl[1] = "bar"
		assert sl == ["foo", "bar", "hello", "world", '', '', '', "1234"]

		sl[2] = "\nhello\nworld\n"
		assert sl == ["foo", "bar", '', "hello", "world", '', "world", '', '', '', "1234"]

		sl[3:4] = "\nfoo\nbar\n", "baz"
		assert sl == ["foo", "bar", '', '', "foo", "bar", '', "baz", '', "world", '', '', '', "1234"]

	def test_blankline(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])

		sl.blankline()
		assert sl == ["", '', "hello", "world", '', '', '', "1234", '']

		sl.blankline()
		assert sl == ["", '', "hello", "world", '', '', '', "1234", '', '']

		sl.blankline(ensure_single=True)
		assert sl == ["", '', "hello", "world", '', '', '', "1234", '']

		sl.blankline(ensure_single=True)
		assert sl == ["", '', "hello", "world", '', '', '', "1234", '']

		sl.append("\t")
		sl.blankline(ensure_single=True)
		assert sl == ["", '', "hello", "world", '', '', '', "1234", '']

		sl.append("    ")
		sl.blankline(ensure_single=True)

		assert sl == ["", '', "hello", "world", '', '', '', "1234", '']

		sl.append("    ")
		sl.blankline(ensure_single=True)
		sl.blankline()
		assert sl == ["", '', "hello", "world", '', '', '', "1234", '', '']

	def test_slicing(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		assert sl[:-3] == ["", '', "hello", "world", '']
		assert sl[-3:] == ['', '', "1234"]

	def test_start_of_line_indents(self):
		assert StringList("Hello\n    World") == ["Hello", "    World"]
		assert StringList("Hello\n    World", convert_indents=True) == ["Hello", "\tWorld"]

	def test_indent_size(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])

		assert sl.indent_size == 0

		sl.indent_size = 7
		assert sl.indent_size == 7

		sl.set_indent_size()
		assert sl.indent_size == 0

		sl.set_indent_size(2)
		assert sl.indent_size == 2

		sl.indent_size += 1
		assert sl.indent_size == 3

		sl.indent_size -= 2
		assert sl.indent_size == 1

	def test_indent_type(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])

		assert sl.indent_type == "\t"

		with pytest.raises(ValueError, match="'type' cannot an empty string."):
			sl.indent_type = ""

		assert sl.indent_type == "\t"

		sl.indent_type = " "
		assert sl.indent_type == " "

		sl.set_indent_type("\t")
		assert sl.indent_type == "\t"

		sl.set_indent_type(" ")
		assert sl.indent_type == " "

		with pytest.raises(ValueError, match="'type' cannot an empty string."):
			sl.set_indent_type("")

		assert sl.indent_type == " "

		sl.set_indent_type()
		assert sl.indent_type == "\t"

	def test_indent(self):
		sl = StringList()
		sl.set_indent_size(1)

		sl.append("Indented")

		assert sl == ["\tIndented"]

		sl.set_indent_type("    ")

		sl.append("Indented")

		assert sl == ["\tIndented", "    Indented"]

		expected_list = [
				"class Foo:",
				'',
				"	def bar(self, listicle: List[Item]):",
				"		...",
				'',
				"	def __repr__(self) -> str:",
				'		return "Foo()"',
				'',
				]

		expected_string = dedent(
				"""\
		class Foo:

			def bar(self, listicle: List[Item]):
				...

			def __repr__(self) -> str:
				return "Foo()"
		"""
				)

		sl = StringList()
		sl.append("class Foo:")
		sl.blankline(True)
		sl.set_indent_size(1)
		sl.append("def bar(self, listicle: List[Item]):")
		sl.indent_size += 1
		sl.append("...")
		sl.indent_size -= 1
		sl.blankline(True)
		sl.append("def __repr__(self) -> str:")
		sl.indent_size += 1
		sl.append('return "Foo()"')
		sl.indent_size -= 1
		sl.blankline(True)
		sl.set_indent_size(0)

		assert sl == expected_list
		assert str(sl) == expected_string
		assert sl == expected_string

		sl = StringList()
		sl.append("class Foo:")
		sl.blankline(True)

		with sl.with_indent("\t", 1):
			sl.append("def bar(self, listicle: List[Item]):")
			with sl.with_indent("\t", 2):
				sl.append("...")
			sl.blankline(True)
			sl.append("def __repr__(self) -> str:")
			with sl.with_indent("\t", 2):
				sl.append('return "Foo()"')
			sl.blankline(True)

		assert sl.indent_size == 0

		assert sl == expected_list
		assert str(sl) == expected_string
		assert sl == expected_string

		sl = StringList()
		sl.append("class Foo:")
		sl.blankline(True)

		with sl.with_indent_size(1):
			sl.append("def bar(self, listicle: List[Item]):")
			with sl.with_indent_size(2):
				sl.append("...")
			sl.blankline(True)
			sl.append("def __repr__(self) -> str:")
			with sl.with_indent_size(2):
				sl.append('return "Foo()"')
			sl.blankline(True)

		assert sl.indent_size == 0

		assert sl == expected_list
		assert str(sl) == expected_string
		assert sl == expected_string

		sl = StringList()
		sl.append("class Foo:")
		sl.set_indent(Indent(0, "    "))
		sl.blankline(True)

		with sl.with_indent_size(1):
			sl.append("def bar(self, listicle: List[Item]):")
			with sl.with_indent_size(2):
				sl.append("...")
			sl.blankline(True)
			sl.append("def __repr__(self) -> str:")
			with sl.with_indent_size(2):
				sl.append('return "Foo()"')
			sl.blankline(True)

		assert sl.indent_size == 0

		assert sl == [x.expandtabs(4) for x in expected_list]
		assert str(sl) == expected_string.expandtabs(4)
		assert sl == expected_string.expandtabs(4)

		sl = StringList()
		sl.append("class Foo:")
		sl.set_indent("    ", 0)
		sl.blankline(True)

		with sl.with_indent_size(1):
			sl.append("def bar(self, listicle: List[Item]):")
			with sl.with_indent_size(2):
				sl.append("...")
			sl.blankline(True)
			sl.append("def __repr__(self) -> str:")
			with sl.with_indent_size(2):
				sl.append('return "Foo()"')
			sl.blankline(True)

		assert sl.indent_size == 0

		assert sl == [x.expandtabs(4) for x in expected_list]
		assert str(sl) == expected_string.expandtabs(4)
		assert sl == expected_string.expandtabs(4)

		sl = StringList()
		sl.append("class Foo:")
		sl.blankline(True)

		with sl.with_indent_size(1):
			sl.append("def bar(self, listicle: List[Item]):")
			with sl.with_indent_size(2):
				sl.append("...")
			sl.blankline(True)
			sl.append("def __repr__(self) -> str:")
			with sl.with_indent_size(2):
				with sl.with_indent_type("    "):
					sl.append('return "Foo()"')
			sl.blankline(True)

		assert sl.indent_size == 0

		expected_list[-2] = '        return "Foo()"'
		assert sl == expected_list
		assert str(sl) == expected_string.replace('\t\treturn "Foo()"', '        return "Foo()"')
		assert sl == expected_string.replace('\t\treturn "Foo()"', '        return "Foo()"')

	def test_convert_indents(self):
		sl = StringList(convert_indents=True)

		sl.append("    Indented")

		assert sl == ["\tIndented"]

	def test_set_indent_error(self):
		sl = StringList()
		with pytest.raises(TypeError, match="'size' argument cannot be used when providing an 'Indent' object."):
			sl.set_indent(Indent(0, "    "), 5)


class TestIndent:

	def test_creation(self):
		indent = Indent()
		assert indent.size == 0
		assert indent.type == "\t"

		indent = Indent(3, "    ")
		assert indent.size == 3
		assert indent.type == "    "

	def test_iter(self):
		indent = Indent(3, "    ")
		assert tuple(indent) == (3, "    ")
		assert list(iter(indent)) == [3, "    "]

	def test_size(self):
		indent = Indent()

		indent.size = 1
		assert indent.size == 1

		indent.size = "2"  # type: ignore
		assert indent.size == 2

		indent.size = 3.0  # type: ignore
		assert indent.size == 3

	def test_type(self):
		indent = Indent()

		indent.type = "    "
		assert indent.type == "    "

		indent.type = " "
		assert indent.type == " "

		indent.type = 1  # type: ignore
		assert indent.type == "1"

		indent.type = ">>> "
		assert indent.type == ">>> "

		with pytest.raises(ValueError, match="'type' cannot an empty string."):
			indent.type = ''

	def test_str(self):
		assert str(Indent()) == ""
		assert str(Indent(1)) == "\t"
		assert str(Indent(5)) == "\t\t\t\t\t"
		assert str(Indent(type="    ")) == ""
		assert str(Indent(1, type="    ")) == "    "
		assert str(Indent(5, type="    ")) == "    " * 5
		assert str(Indent(type=">>> ")) == ""
		assert str(Indent(1, type=">>> ")) == ">>> "

	def test_repr(self):
		assert repr(Indent()) == "Indent(size=0, type='\\t')"
		assert repr(Indent(1)) == "Indent(size=1, type='\\t')"
		assert repr(Indent(5)) == "Indent(size=5, type='\\t')"
		assert repr(Indent(type="    ")) == "Indent(size=0, type='    ')"
		assert repr(Indent(1, type="    ")) == "Indent(size=1, type='    ')"
		assert repr(Indent(5, type="    ")) == "Indent(size=5, type='    ')"
		assert repr(Indent(type=">>> ")) == "Indent(size=0, type='>>> ')"
		assert repr(Indent(1, type=">>> ")) == "Indent(size=1, type='>>> ')"

	def test_eq(self):
		assert Indent() == Indent()
		assert Indent() == (0, "\t")
		assert Indent() == ''

		assert Indent(1, "    ") == Indent(1, "    ")
		assert Indent(1, "    ") == (1, "    ")
		assert Indent(1, "    ") == '    '

		assert Indent(2, "\t") == Indent(2, "\t")
		assert Indent(2, "\t") == (2, "\t")
		assert Indent(2, "\t") == '\t\t'

		assert not Indent() == 1

	def test_extend(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		sl.extend(["\nfoo\nbar\n    baz"])

		assert sl == ["", '', "hello", "world", '', '', '', "1234", '', "foo", "bar", "    baz"]

	def test_clear(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		sl.clear()

		assert sl == []

	def test_copy(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		sl2 = sl.copy()

		assert sl == sl2
		assert sl2 == ["", '', "hello", "world", '', '', '', "1234"]
		assert isinstance(sl2, StringList)

	def test_count(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		assert sl.count("hello") == 1

	def test_count_blanklines(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		assert sl.count_blanklines() == 5

	def test_index(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		assert sl.index("hello") == 2

	def test_pop(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		assert sl.pop(2) == "hello"
		assert sl == ["", '', "world", '', '', '', "1234"]
		assert isinstance(sl, StringList)

	def test_remove(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		sl.remove("hello")
		assert sl == ["", '', "world", '', '', '', "1234"]
		assert isinstance(sl, StringList)

	def test_reverse(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		sl.reverse()
		assert sl == ["1234", '', '', '', "world", "hello", '', '']
		assert isinstance(sl, StringList)

	def test_sort(self):
		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		sl.sort()
		assert sl == ['', '', '', '', '', "1234", "hello", "world"]
		assert isinstance(sl, StringList)

		sl = StringList(["", '', "hello", "world", '', '', '', "1234"])
		sl.sort(reverse=True)
		assert sl == ["world", "hello", "1234", '', '', '', '', '']
		assert isinstance(sl, StringList)
