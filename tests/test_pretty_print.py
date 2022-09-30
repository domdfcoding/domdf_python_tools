#  Based on CPython.
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.
#

# stdlib
import collections
import io
import itertools
import random
import types
from textwrap import dedent
from typing import no_type_check

# 3rd party
import pytest
from coincidence.regressions import AdvancedFileRegressionFixture

# this package
from domdf_python_tools.pretty_print import FancyPrinter, simple_repr
from domdf_python_tools.stringlist import StringList

# list, tuple and dict subclasses that do or don't overwrite __repr__


class list2(list):
	pass


class list3(list):

	def __repr__(self):
		return list.__repr__(self)


class list_custom_repr(list):

	def __repr__(self):
		return '*' * len(list.__repr__(self))


class tuple2(tuple):
	__slots__ = ()


class tuple3(tuple):
	__slots__ = ()

	def __repr__(self):
		return tuple.__repr__(self)


class tuple_custom_repr(tuple):
	__slots__ = ()

	def __repr__(self):
		return '*' * len(tuple.__repr__(self))


class set2(set):
	pass


class set3(set):

	def __repr__(self):
		return set.__repr__(self)


class set_custom_repr(set):

	def __repr__(self):
		return '*' * len(set.__repr__(self))


class frozenset2(frozenset):
	pass


class frozenset3(frozenset):

	def __repr__(self):
		return frozenset.__repr__(self)


class frozenset_custom_repr(frozenset):

	def __repr__(self):
		return '*' * len(frozenset.__repr__(self))


class dict2(dict):
	pass


class dict3(dict):

	def __repr__(self):
		return dict.__repr__(self)


class dict_custom_repr(dict):

	def __repr__(self):
		return '*' * len(dict.__repr__(self))


class Unorderable:

	def __repr__(self):
		return str(id(self))


# Class Orderable is orderable with any type
class Orderable:

	def __init__(self, hash):  # noqa: A002  # pylint: disable=redefined-builtin
		self._hash = hash

	def __lt__(self, other):
		return False

	def __gt__(self, other):
		return self != other

	def __le__(self, other):
		return self == other

	def __ge__(self, other):
		return True

	def __eq__(self, other):
		return self is other

	def __ne__(self, other):
		return self is not other

	def __hash__(self):
		return self._hash


fruit = [
		"apple",
		"orange",
		"pear",
		"lemon",
		"grape",
		"strawberry",
		"banana",
		"plum",
		"tomato",
		"cherry",
		"blackcurrant",
		]


class TestFancyPrinter:

	def test_list(self):
		assert FancyPrinter().pformat([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) == "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
		assert FancyPrinter().pformat(fruit) == dedent(
				"""\
		[
		 'apple',
		 'orange',
		 'pear',
		 'lemon',
		 'grape',
		 'strawberry',
		 'banana',
		 'plum',
		 'tomato',
		 'cherry',
		 'blackcurrant',
		 ]"""
				)

	@no_type_check
	def test_init(self):
		FancyPrinter()
		FancyPrinter(indent=4, width=40, depth=5, stream=io.StringIO(), compact=True)
		FancyPrinter(4, 40, 5, io.StringIO())
		with pytest.raises(TypeError):
			FancyPrinter(4, 40, 5, io.StringIO(), True)
		with pytest.raises(ValueError):
			FancyPrinter(indent=-1)
		with pytest.raises(ValueError):
			FancyPrinter(depth=0)
		with pytest.raises(ValueError):
			FancyPrinter(depth=-1)
		with pytest.raises(ValueError):
			FancyPrinter(width=0)

	@pytest.mark.parametrize(
			"safe",
			[
					2,
					2.0,
					2j,
					"abc",
					[3],
					(2, 2),
					{3: 3},
					b"def",
					bytearray(b"ghi"),
					True,
					False,
					None,
					...,
					list(range(100)),
					list(range(200)),
					]
			)
	def test_basic(self, safe):
		# Verify .isrecursive() and .isreadable() w/o recursion
		pp = FancyPrinter()
		# PrettyPrinter methods
		assert not pp.isrecursive(safe), f"expected not isrecursive for {safe!r}"
		assert pp.isreadable(safe), f"expected isreadable for {safe!r}"

	@no_type_check
	def test_knotted(self):
		a = list(range(100))
		b = list(range(200))
		a[-12] = b

		# Verify .isrecursive() and .isreadable() w/ recursion
		# Tie a knot.
		b[67] = a
		# Messy dict.
		d = {}
		d[0] = d[1] = d[2] = d

		pp = FancyPrinter()

		for icky in a, b, d, (d, d):
			assert pp.isrecursive(icky), "expected isrecursive"
			assert not pp.isreadable(icky), "expected not isreadable"

		# Break the cycles.
		d.clear()
		del a[:]
		del b[:]

		for safe in a, b, d, (d, d):
			# module-level convenience functions
			# PrettyPrinter methods
			assert not pp.isrecursive(safe), f"expected not isrecursive for {safe!r}"
			assert pp.isreadable(safe), f"expected isreadable for {safe!r}"

	#
	# def test_unreadable(self):
	# 	# Not recursive but not readable anyway
	# 	pp = FancyPrinter()
	# 	for unreadable in type(3), pprint, pprint.isrecursive:
	# 		# PrettyPrinter methods
	# 		assert not pp.isrecursive(unreadable), "expected not isrecursive for %r" % (unreadable,)
	# 		assert not pp.isreadable(unreadable), "expected not isreadable for %r" % (unreadable,)
	#
	# def test_same_as_repr(self):
	# 	# Simple objects, small containers and classes that override __repr__
	# 	# to directly call super's __repr__.
	# 	# For those the result should be the same as repr().
	# 	# Ahem.  The docs don't say anything about that -- this appears to
	# 	# be testing an implementation quirk.  Starting in Python 2.5, it's
	# 	# not true for dicts:  pprint always sorts dicts by key now; before,
	# 	# it sorted a dict display if and only if the display required
	# 	# multiple lines.  For that reason, dicts with more than one element
	# 	# aren't tested here.
	# 	for simple in (0, 0, 0 + 0j, 0.0, "", b"", bytearray(),
	# 				   (), tuple2(), tuple3(),
	# 				   [], list2(), list3(),
	# 				   set(), set2(), set3(),
	# 				   frozenset(), frozenset2(), frozenset3(),
	# 				   {}, dict2(), dict3(),
	# 				   self.assertTrue, pprint,
	# 				   -6, -6, -6 - 6j, -1.5, "x", b"x", bytearray(b"x"),
	# 				   (3,), [3], {3: 6},
	# 				   (1, 2), [3, 4], {5: 6},
	# 				   tuple2((1, 2)), tuple3((1, 2)), tuple3(range(100)),
	# 				   [3, 4], list2([3, 4]), list3([3, 4]), list3(range(100)),
	# 				   set({7}), set2({7}), set3({7}),
	# 				   frozenset({8}), frozenset2({8}), frozenset3({8}),
	# 				   dict2({5: 6}), dict3({5: 6}),
	# 				   range(10, -11, -1),
	# 				   True, False, None, ...,
	# 				   ):
	# 		native = repr(simple)
	# 		self.assertEqual(FancyPrinter().pformat(simple), native)
	# 		self.assertEqual(FancyPrinter(width=1, indent=0).pformat(simple)
	# 						 .replace('\n', ' '), native)
	#
	# def test_container_repr_override_called(self):
	# 	N = 1000
	# 	# Ensure that __repr__ override is called for subclasses of containers
	#
	# 	for cont in (list_custom_repr(),
	# 				 list_custom_repr([1, 2, 3]),
	# 				 list_custom_repr(range(N)),
	# 				 tuple_custom_repr(),
	# 				 tuple_custom_repr([1, 2, 3]),
	# 				 tuple_custom_repr(range(N)),
	# 				 set_custom_repr(),
	# 				 set_custom_repr([1, 2, 3]),
	# 				 set_custom_repr(range(N)),
	# 				 frozenset_custom_repr(),
	# 				 frozenset_custom_repr([1, 2, 3]),
	# 				 frozenset_custom_repr(range(N)),
	# 				 dict_custom_repr(),
	# 				 dict_custom_repr({5: 6}),
	# 				 dict_custom_repr(zip(range(N), range(N))),
	# 				 ):
	# 		native = repr(cont)
	# 		expected = '*' * len(native)
	# 		self.assertEqual(FancyPrinter().pformat(cont), expected)
	# 		self.assertEqual(FancyPrinter(width=1, indent=0).pformat(cont), expected)

	@no_type_check
	def test_basic_line_wrap(self):
		# verify basic line-wrapping operation
		o = {
				"RPM_cal": 0,
				"RPM_cal2": 48059,
				"Speed_cal": 0,
				"controldesk_runtime_us": 0,
				"main_code_runtime_us": 0,
				"read_io_runtime_us": 0,
				"write_io_runtime_us": 43690
				}
		exp = """\
{
 'RPM_cal': 0,
 'RPM_cal2': 48059,
 'Speed_cal': 0,
 'controldesk_runtime_us': 0,
 'main_code_runtime_us': 0,
 'read_io_runtime_us': 0,
 'write_io_runtime_us': 43690,
 }"""
		for t in [dict, dict2]:
			assert FancyPrinter().pformat(t(o)) == exp

		o = range(100)
		exp = "[\n %s,\n ]" % ",\n ".join(map(str, o))
		for t in [list, list2]:
			assert FancyPrinter().pformat(t(o)) == exp

		o = tuple(range(100))
		exp = "(\n %s,\n )" % ",\n ".join(map(str, o))
		for t in [tuple, tuple2]:
			assert FancyPrinter().pformat(t(o)) == exp

		# indent parameter
		o = range(100)
		exp = "[\n    %s,\n    ]" % ",\n    ".join(map(str, o))
		for t in [list, list2]:
			assert FancyPrinter(indent=4).pformat(t(o)) == exp

	def test_nested_indentations(self):
		o1 = list(range(10))
		o2 = dict(first=1, second=2, third=3)
		o = [o1, o2]
		expected = """\
[
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    {'first': 1, 'second': 2, 'third': 3},
    ]"""
		assert FancyPrinter(indent=4, width=42).pformat(o) == expected
		expected = """\
[
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    {
        'first': 1,
        'second': 2,
        'third': 3,
        },
    ]"""
		assert FancyPrinter(indent=4, width=41).pformat(o) == expected

	def test_width(self):
		expected = """\
[
 [
  [
   [
    [
     [1, 2, 3],
     '1 2',
     ],
    ],
   ],
  ],
 {
  1: [1, 2, 3],
  2: [12, 34],
  },
 'abc def ghi',
 ('ab cd ef',),
 set2({1, 23}),
 [
  [
   [
    [
     [1, 2, 3],
     '1 2',
     ],
    ],
   ],
  ],
 ]"""
		eval_ = eval
		o = eval_(expected)
		assert FancyPrinter(width=15).pformat(o) == expected
		assert FancyPrinter(width=16).pformat(o) == expected
		assert FancyPrinter(width=25).pformat(o) == expected
		assert FancyPrinter(width=14).pformat(
				o
				) == """\
[
 [
  [
   [
    [
     [
      1,
      2,
      3,
      ],
     '1 '
     '2',
     ],
    ],
   ],
  ],
 {
  1: [
      1,
      2,
      3,
      ],
  2: [
      12,
      34,
      ],
  },
 'abc def '
 'ghi',
 (
  'ab cd '
  'ef',),
 set2({
       1,
       23,
       }),
 [
  [
   [
    [
     [
      1,
      2,
      3,
      ],
     '1 '
     '2',
     ],
    ],
   ],
  ],
 ]"""

	def test_sorted_dict(self):
		# Starting in Python 2.5, pprint sorts dict displays by key regardless
		# of how small the dictionary may be.
		# Before the change, on 32-bit Windows pformat() gave order
		# 'a', 'c', 'b' here, so this test failed.
		d = {'a': 1, 'b': 1, 'c': 1}
		assert FancyPrinter().pformat(d) == "{'a': 1, 'b': 1, 'c': 1}"
		assert FancyPrinter().pformat([d, d]) == "[{'a': 1, 'b': 1, 'c': 1}, {'a': 1, 'b': 1, 'c': 1}]"

		# The next one is kind of goofy.  The sorted order depends on the
		# alphabetic order of type names:  "int" < "str" < "tuple".  Before
		# Python 2.5, this was in the test_same_as_repr() test.  It's worth
		# keeping around for now because it's one of few tests of pprint
		# against a crazy mix of types.
		assert FancyPrinter().pformat({
				"xy\tab\n": (3, ),
				5: [[]],
				(): {},
				}) == r"{5: [[]], 'xy\tab\n': (3,), (): {}}"

	def test_ordered_dict(self, advanced_file_regression: AdvancedFileRegressionFixture):
		d: collections.OrderedDict = collections.OrderedDict()
		assert FancyPrinter(width=1).pformat(d) == "OrderedDict()"
		d = collections.OrderedDict([])
		assert FancyPrinter(width=1).pformat(d) == "OrderedDict()"
		words = "the quick brown fox jumped over a lazy dog".split()
		d = collections.OrderedDict(zip(words, itertools.count()))
		advanced_file_regression.check(FancyPrinter().pformat(d))

	def test_mapping_proxy(self):
		words = "the quick brown fox jumped over a lazy dog".split()
		d = dict(zip(words, itertools.count()))
		m = types.MappingProxyType(d)
		assert FancyPrinter().pformat(
				m
				) == """\
mappingproxy({
              'the': 0,
              'quick': 1,
              'brown': 2,
              'fox': 3,
              'jumped': 4,
              'over': 5,
              'a': 6,
              'lazy': 7,
              'dog': 8,
              })"""
		d = collections.OrderedDict(zip(words, itertools.count()))
		m = types.MappingProxyType(d)
		assert FancyPrinter().pformat(
				m
				) == """\
mappingproxy(OrderedDict([
                          ('the', 0),
                          ('quick', 1),
                          ('brown', 2),
                          ('fox', 3),
                          ('jumped', 4),
                          ('over', 5),
                          ('a', 6),
                          ('lazy', 7),
                          ('dog', 8),
                          ]))"""

	def test_empty_simple_namespace(self):
		ns = types.SimpleNamespace()
		formatted = FancyPrinter().pformat(ns)
		assert formatted == "namespace()"

	def test_small_simple_namespace(self):
		ns = types.SimpleNamespace(a=1, b=2)
		formatted = FancyPrinter().pformat(ns)
		assert formatted == "namespace(a=1, b=2)"

	def test_subclassing(self, advanced_file_regression: AdvancedFileRegressionFixture):
		o = {"names with spaces": "should be presented using repr()", "others.should.not.be": "like.this"}
		advanced_file_regression.check(DottedPrettyPrinter().pformat(o))

	@pytest.mark.parametrize(
			"value, width",
			[
					pytest.param(set(range(7)), 20, id="case_1"),
					pytest.param(set2(range(7)), 20, id="case_2"),
					pytest.param(set3(range(7)), 20, id="case_3"),
					]
			)
	def test_set_reprs(self, value, width, advanced_file_regression: AdvancedFileRegressionFixture):
		assert FancyPrinter().pformat(set()) == "set()"
		assert FancyPrinter().pformat(set(range(3))) == "{0, 1, 2}"
		advanced_file_regression.check(FancyPrinter(width=width).pformat(value))

	@pytest.mark.parametrize(
			"value, width",
			[
					pytest.param(frozenset(range(7)), 20, id="case_1"),
					pytest.param(frozenset2(range(7)), 20, id="case_2"),
					pytest.param(frozenset3(range(7)), 20, id="case_3"),
					]
			)
	def test_frozenset_reprs(self, value, width, advanced_file_regression: AdvancedFileRegressionFixture):
		assert FancyPrinter().pformat(frozenset()) == "frozenset()"
		assert FancyPrinter().pformat(frozenset(range(3))) == "frozenset({0, 1, 2})"
		advanced_file_regression.check(FancyPrinter(width=width).pformat(value))

	def test_depth(self):
		nested_tuple = (1, (2, (3, (4, (5, 6)))))
		nested_dict = {1: {2: {3: {4: {5: {6: 6}}}}}}
		nested_list = [1, [2, [3, [4, [5, [6, []]]]]]]
		assert FancyPrinter().pformat(nested_tuple) == repr(nested_tuple)
		assert FancyPrinter().pformat(nested_dict) == repr(nested_dict)
		assert FancyPrinter().pformat(nested_list) == repr(nested_list)

		lv1_tuple = "(1, (...))"
		lv1_dict = "{1: {...}}"
		lv1_list = "[1, [...]]"
		assert FancyPrinter(depth=1).pformat(nested_tuple) == lv1_tuple
		assert FancyPrinter(depth=1).pformat(nested_dict) == lv1_dict
		assert FancyPrinter(depth=1).pformat(nested_list) == lv1_list

	def test_sort_unorderable_values(self):
		# Issue 3976:  sorted pprints fail for unorderable values.
		n = 20
		keys = [Unorderable() for i in range(n)]
		random.shuffle(keys)
		skeys = sorted(keys, key=id)
		clean = lambda s: s.replace(' ', '').replace('\n', '')

		assert clean(FancyPrinter().pformat(set(keys))) == '{' + ','.join(map(repr, skeys)) + ",}"
		assert clean(FancyPrinter().pformat(frozenset(keys))) == "frozenset({" + ','.join(map(repr, skeys)) + ",})"
		assert clean(FancyPrinter().pformat(dict.fromkeys(keys))
						) == '{' + ','.join("%r:None" % k for k in keys) + ",}"

		# Issue 10017: TypeError on user-defined types as dict keys.
		assert FancyPrinter().pformat({Unorderable: 0, 1: 0}) == "{1: 0, " + repr(Unorderable) + ": 0}"

		# Issue 14998: TypeError on tuples with NoneTypes as dict keys.
		keys = [(1, ), (None, )]  # type: ignore
		assert FancyPrinter().pformat(dict.fromkeys(keys, 0)) == "{%r: 0, %r: 0}" % tuple(sorted(keys, key=id))

	def test_sort_orderable_and_unorderable_values(self):
		# Issue 22721:  sorted pprints is not stable
		a = Unorderable()
		b = Orderable(hash(a))  # should have the same hash value
		# self-test
		assert a < b
		assert str(type(b)) < str(type(a))
		assert sorted([b, a]) == [a, b]  # type: ignore
		assert sorted([a, b]) == [a, b]  # type: ignore
		# set
		assert FancyPrinter(width=1).pformat({b, a}) == f"{{\n {a!r},\n {b!r},\n }}"
		assert FancyPrinter(width=1).pformat({a, b}) == f"{{\n {a!r},\n {b!r},\n }}"
		# dict
		assert FancyPrinter(width=1).pformat(dict.fromkeys([b, a])) == f"{{\n {b!r}: None,\n {a!r}: None,\n }}"
		assert FancyPrinter(width=1).pformat(dict.fromkeys([a, b])) == f"{{\n {a!r}: None,\n {b!r}: None,\n }}"

	def test_str_wrap(self):
		# pprint tries to wrap strings intelligently
		fox = "the quick brown fox jumped over a lazy dog"
		assert FancyPrinter(width=19
							).pformat(fox) == """\
('the quick brown '
 'fox jumped over '
 'a lazy dog')"""
		assert FancyPrinter(width=25).pformat({'a': 1, 'b': fox, 'c': 2}) == """\
{
 'a': 1,
 'b': 'the quick brown '
      'fox jumped over '
      'a lazy dog',
 'c': 2,
 }"""
		# With some special characters
		# - \n always triggers a new line in the pprint
		# - \t and \n are escaped
		# - non-ASCII is allowed
		# - an apostrophe doesn't disrupt the pprint
		special = "Portons dix bons \"whiskys\"\nà l'avocat goujat\t qui fumait au zoo"
		assert FancyPrinter(width=68).pformat(special) == repr(special)
		assert FancyPrinter(width=31).pformat(
				special
				) == """\
('Portons dix bons "whiskys"\\n'
 "à l'avocat goujat\\t qui "
 'fumait au zoo')"""
		assert FancyPrinter(width=20).pformat(
				special
				) == """\
('Portons dix bons '
 '"whiskys"\\n'
 "à l'avocat "
 'goujat\\t qui '
 'fumait au zoo')"""
		assert FancyPrinter(width=35).pformat([[[[[special]]]]]) == """\
[
 [
  [
   [
    [
     'Portons dix bons "whiskys"\\n'
     "à l'avocat goujat\\t qui "
     'fumait au zoo',
     ],
    ],
   ],
  ],
 ]"""
		assert FancyPrinter(width=25).pformat([[[[[special]]]]]) == """\
[
 [
  [
   [
    [
     'Portons dix bons '
     '"whiskys"\\n'
     "à l'avocat "
     'goujat\\t qui '
     'fumait au zoo',
     ],
    ],
   ],
  ],
 ]"""
		assert FancyPrinter(width=23).pformat([[[[[special]]]]]) == """\
[
 [
  [
   [
    [
     'Portons dix '
     'bons "whiskys"\\n'
     "à l'avocat "
     'goujat\\t qui '
     'fumait au '
     'zoo',
     ],
    ],
   ],
  ],
 ]"""
		# An unwrappable string is formatted as its repr
		unwrappable = 'x' * 100
		assert FancyPrinter(width=80).pformat(unwrappable) == repr(unwrappable)
		assert FancyPrinter().pformat('') == "''"
		# Check that the pprint is a usable repr
		special *= 10
		eval_ = eval
		for width in range(3, 40):
			assert eval_(FancyPrinter(width=width).pformat(special)) == special
			assert eval_(FancyPrinter(width=width).pformat([special] * 2)) == [special] * 2

	def test_compact(self):
		o = ([list(range(i * i)) for i in range(5)] + [list(range(i)) for i in range(6)])
		expected = """\
[[], [0], [0, 1, 2, 3],
 [0, 1, 2, 3, 4, 5, 6, 7, 8],
 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
  14, 15],
 [], [0], [0, 1], [0, 1, 2], [0, 1, 2, 3],
 [0, 1, 2, 3, 4]]"""
		assert FancyPrinter(width=47, compact=True).pformat(o, ) == expected

	def test_compact_width(self):
		levels = 20
		number = 10
		o = [0] * number
		for i in range(levels - 1):
			o = [o]  # type: ignore
		for w in range(levels * 2 + 1, levels + 3 * number - 1):
			lines = FancyPrinter(width=w, compact=True).pformat(o, ).splitlines()
			maxwidth = max(map(len, lines))
			assert maxwidth <= w
			maxwidth > w - 3  # pylint: disable=pointless-statement

	def test_bytes_wrap(self):
		assert FancyPrinter(width=1).pformat(b'') == "b''"
		assert FancyPrinter(width=1).pformat(b"abcd") == "b'abcd'"
		letters = b"abcdefghijklmnopqrstuvwxyz"
		assert FancyPrinter(width=29).pformat(letters) == repr(letters)
		assert FancyPrinter(width=19).pformat(letters) == """\
(b'abcdefghijkl'
 b'mnopqrstuvwxyz')"""
		assert FancyPrinter(width=18).pformat(letters) == """\
(b'abcdefghijkl'
 b'mnopqrstuvwx'
 b'yz')"""
		assert FancyPrinter(width=16).pformat(letters) == """\
(b'abcdefghijkl'
 b'mnopqrstuvwx'
 b'yz')"""
		special = bytes(range(16))
		assert FancyPrinter(width=61).pformat(special) == repr(special)
		assert FancyPrinter(width=48).pformat(
				special
				) == """\
(b'\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07\\x08\\t\\n\\x0b'
 b'\\x0c\\r\\x0e\\x0f')"""
		assert FancyPrinter(width=32).pformat(
				special
				) == """\
(b'\\x00\\x01\\x02\\x03'
 b'\\x04\\x05\\x06\\x07\\x08\\t\\n\\x0b'
 b'\\x0c\\r\\x0e\\x0f')"""
		assert FancyPrinter(width=1).pformat(
				special
				) == """\
(b'\\x00\\x01\\x02\\x03'
 b'\\x04\\x05\\x06\\x07'
 b'\\x08\\t\\n\\x0b'
 b'\\x0c\\r\\x0e\\x0f')"""
		assert FancyPrinter(width=21).pformat({'a': 1, 'b': letters, 'c': 2} == """\
{
 'a': 1,
 'b': b'abcdefghijkl'
      b'mnopqrstuvwx'
      b'yz',
 'c': 2,
 }""")
		assert FancyPrinter(width=20).pformat({'a': 1, 'b': letters, 'c': 2}) == """\
{
 'a': 1,
 'b': b'abcdefgh'
      b'ijklmnop'
      b'qrstuvwxyz',
 'c': 2,
 }"""
		assert FancyPrinter(width=25).pformat([[[[[[letters]]]]]]) == """\
[
 [
  [
   [
    [
     [
      b'abcdefghijklmnop'
      b'qrstuvwxyz',
      ],
     ],
    ],
   ],
  ],
 ]"""
		assert FancyPrinter(width=41).pformat([[[[[[special]]]]]]) == """\
[
 [
  [
   [
    [
     [
      b'\\x00\\x01\\x02\\x03\\x04\\x05\\x06\\x07'
      b'\\x08\\t\\n\\x0b\\x0c\\r\\x0e\\x0f',
      ],
     ],
    ],
   ],
  ],
 ]"""
		# Check that the pprint is a usable repr
		eval_ = eval
		for width in range(1, 64):
			assert eval_(FancyPrinter(width=width).pformat(special)) == special
			assert eval_(FancyPrinter(width=width).pformat([special] * 2)) == [special] * 2

	@pytest.mark.parametrize(
			"value, width",
			[
					pytest.param(bytearray(), 1, id="case_1"),
					pytest.param(bytearray(b"abcdefghijklmnopqrstuvwxyz"), 40, id="case_2"),
					pytest.param(bytearray(b"abcdefghijklmnopqrstuvwxyz"), 28, id="case_3"),
					pytest.param(bytearray(b"abcdefghijklmnopqrstuvwxyz"), 27, id="case_4"),
					pytest.param(bytearray(b"abcdefghijklmnopqrstuvwxyz"), 25, id="case_5"),
					pytest.param(bytearray(range(16)), 72, id="case_6"),
					pytest.param(bytearray(range(16)), 57, id="case_7"),
					pytest.param(bytearray(range(16)), 41, id="case_8"),
					pytest.param(bytearray(range(16)), 1, id="case_9"),
					pytest.param(
							{'a': 1, 'b': bytearray(b"abcdefghijklmnopqrstuvwxyz"), 'c': 2},
							31,
							id="case_10",
							),
					pytest.param([[[[[bytearray(b"abcdefghijklmnopqrstuvwxyz")]]]]], 37, id="case_11"),
					pytest.param([[[[[bytearray(range(16))]]]]], 50, id="case_12"),
					]
			)
	def test_bytearray_wrap(self, value, width, advanced_file_regression: AdvancedFileRegressionFixture):
		advanced_file_regression.check(FancyPrinter(width=width).pformat(value))

	def test_default_dict(self, advanced_file_regression: AdvancedFileRegressionFixture):
		d: collections.defaultdict = collections.defaultdict(int)
		assert FancyPrinter(width=1).pformat(d) == "defaultdict(<class 'int'>, {})"
		words = "the quick brown fox jumped over a lazy dog".split()
		d = collections.defaultdict(int, zip(words, itertools.count()))
		advanced_file_regression.check(FancyPrinter().pformat(d))

	def test_counter(self, advanced_file_regression: AdvancedFileRegressionFixture):
		d: collections.Counter = collections.Counter()
		assert FancyPrinter(width=1).pformat(d) == "Counter()"
		d = collections.Counter("senselessness")
		advanced_file_regression.check(FancyPrinter(width=40).pformat(d))

	def test_chainmap(self, advanced_file_regression: AdvancedFileRegressionFixture):
		d: collections.ChainMap = collections.ChainMap()
		assert FancyPrinter(width=1).pformat(d) == "ChainMap({})"
		words = "the quick brown fox jumped over a lazy dog".split()
		items = list(zip(words, itertools.count()))
		d = collections.ChainMap(dict(items))
		advanced_file_regression.check(FancyPrinter().pformat(d))

	def test_chainmap_nested(self, advanced_file_regression: AdvancedFileRegressionFixture):
		words = "the quick brown fox jumped over a lazy dog".split()
		items = list(zip(words, itertools.count()))
		d = collections.ChainMap(dict(items), collections.OrderedDict(items))
		advanced_file_regression.check(FancyPrinter().pformat(d))

	def test_deque(self):
		d: collections.deque = collections.deque()
		assert FancyPrinter(width=1).pformat(d) == "deque([])"
		d = collections.deque(maxlen=7)
		assert FancyPrinter(width=1).pformat(d) == "deque([], maxlen=7)"
		words = "the quick brown fox jumped over a lazy dog".split()
		d = collections.deque(zip(words, itertools.count()))
		assert FancyPrinter().pformat(
				d
				) == """\
deque([('the', 0),
       ('quick', 1),
       ('brown', 2),
       ('fox', 3),
       ('jumped', 4),
       ('over', 5),
       ('a', 6),
       ('lazy', 7),
       ('dog', 8)])"""
		d = collections.deque(zip(words, itertools.count()), maxlen=7)
		assert FancyPrinter().pformat(
				d
				) == """\
deque([('brown', 2),
       ('fox', 3),
       ('jumped', 4),
       ('over', 5),
       ('a', 6),
       ('lazy', 7),
       ('dog', 8)],
      maxlen=7)"""

	def test_user_dict(self, advanced_file_regression: AdvancedFileRegressionFixture):
		d: collections.UserDict = collections.UserDict()
		assert FancyPrinter(width=1).pformat(d) == "{}"
		words = "the quick brown fox jumped over a lazy dog".split()
		d = collections.UserDict(zip(words, itertools.count()))
		advanced_file_regression.check(FancyPrinter().pformat(d))

	def test_user_list(self, advanced_file_regression: AdvancedFileRegressionFixture):
		d: collections.UserList = collections.UserList()
		assert FancyPrinter(width=1).pformat(d) == "[]"
		words = "the quick brown fox jumped over a lazy dog".split()
		d = collections.UserList(zip(words, itertools.count()))
		advanced_file_regression.check(FancyPrinter().pformat(d))

	@pytest.mark.parametrize(
			"value, width, expects",
			[
					(collections.UserString(''), 1, "''"),
					(
							collections.UserString("the quick brown fox jumped over a lazy dog"),
							20,
							str(StringList([
									"('the quick brown '",
									" 'fox jumped over '",
									" 'a lazy dog')",
									]))
							),
					({1: collections.UserString("the quick brown fox jumped over a lazy dog")},
						20,
						str(
								StringList([
										'{',
										" 1: 'the quick '",
										"    'brown fox '",
										"    'jumped over a '",
										"    'lazy dog',",
										" }"
										])
								)),
					]
			)
	def test_user_string(self, value, width, expects):
		assert FancyPrinter(width=width).pformat(value) == expects


class DottedPrettyPrinter(FancyPrinter):

	def format(self, object, context, maxlevels, level):  # noqa: A002,A003  # pylint: disable=redefined-builtin
		if isinstance(object, str):
			if ' ' in object:
				return repr(object), 1, 0
			else:
				return object, 0, 0
		else:
			return FancyPrinter.format(self, object, context, maxlevels, level)


def test_simple_repr(advanced_file_regression: AdvancedFileRegressionFixture):

	@simple_repr('a', 'b', 'c', 'd', width=10)
	class F:
		a = "apple"
		b = "banana"
		c = "cherry"
		d = list(range(100))

	advanced_file_regression.check(repr(F()))
