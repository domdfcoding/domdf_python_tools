# stdlib
from textwrap import dedent

# 3rd party
import pytest

# this package
from domdf_python_tools.stringlist import StringList


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
