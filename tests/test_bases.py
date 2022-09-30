"""
test_bases
~~~~~~~~~~~~~~~

Test functions in bases.py

"""

# stdlib
import copy
import pickle  # nosec: B101
from numbers import Number, Real
from typing import no_type_check

# 3rd party
import pytest

# this package
from domdf_python_tools._is_match import is_match_with
from domdf_python_tools.bases import Dictable, UserFloat


class Person(Dictable):

	def __init__(self, name, age, occupation=None):
		super().__init__()

		self.name = str(name)
		self.age = int(age)
		self.occupation = occupation

	@property
	def __dict__(self):
		return dict(
				name=self.name,
				age=self.age,
				occupation=self.occupation,
				)


class Child(Person):

	def __init__(self, name, age, school):
		super().__init__(name, age, "Student")

		self.school = "school"

	@property
	def __dict__(self):
		class_dict = super().__dict__
		class_dict["School"] = self.school
		return class_dict


@pytest.fixture()
def alice():
	return Person("Alice", 20, "IRC Lurker")


class TestDictable:

	def test_creation(self, alice):
		assert alice.name == "Alice"
		assert alice.age == 20
		assert alice.occupation == "IRC Lurker"

	def test_str(self, alice: object):
		assert str(alice).startswith("<tests.test_bases.Person")

	def test_equality(self):
		dolly = Person("Dolly", 6, "Sheep")
		clone = Person("Dolly", 6, "Sheep")

		assert dolly == clone

	def test_iter(self, alice):
		for key, value in alice:
			assert key == "name"
			assert value == "Alice"
			return

	def test_copy(self, alice):
		assert copy.copy(alice) == alice
		assert copy.deepcopy(alice) == alice
		assert copy.copy(alice) == copy.copy(alice)

	def test_pickle(self, alice):
		assert pickle.loads(pickle.dumps(alice)) == alice  # nosec: B101

	def test_vars(self, alice):
		assert vars(alice) == dict(alice)

	def test_subclass(self):
		person = Person("Bob", 12, "Student")
		child = Child("Bob", 12, "Big School")
		assert person == child
		assert "School" not in person.__dict__


seven = UserFloat(7)


class TestUserFloat:

	def test_creation(self):
		assert isinstance(seven, Real)
		assert isinstance(seven, Number)

		assert seven == 7
		assert seven == 7.0

	def test_as_integer_ratio(self):
		assert seven.as_integer_ratio() == (7, 1)
		assert seven.as_integer_ratio() == 7.0.as_integer_ratio()

	def test_hex(self):
		assert seven.hex() == "0x1.c000000000000p+2"
		assert seven.hex() == 7.0.hex()

	def test_is_integer(self):
		assert seven.is_integer()
		assert seven.is_integer() == 7.0.is_integer()

	def test_add(self):
		assert isinstance(seven + 7, UserFloat)
		assert seven + 7 == UserFloat(14)
		assert seven + 7 == 14
		assert seven + 7 == 14.0

	def test_radd(self):
		assert isinstance(7 + seven, UserFloat)
		assert 7 + seven == UserFloat(14)
		assert 7 + seven == 14
		assert 7 + seven == 14.0

	def test_sub(self):
		assert isinstance(seven - 3, UserFloat)
		assert seven - 3 == UserFloat(4)
		assert seven - 3 == 4
		assert seven - 3 == 4.0

	def test_rsub(self):
		assert isinstance(3 - seven, UserFloat)
		assert 3 - seven == UserFloat(-4)
		assert 3 - seven == -UserFloat(4)
		assert 3 - seven == -4
		assert 3 - seven == -4.0

	def test_mul(self):
		assert isinstance(seven * 3, UserFloat)
		assert seven * 3 == UserFloat(21)
		assert seven * 3 == 21
		assert seven * 3 == 21.0

	def test_rmul(self):
		assert isinstance(3 * seven, UserFloat)
		assert 3 * seven == UserFloat(21)
		assert 3 * seven == UserFloat(21)
		assert 3 * seven == 21
		assert 3 * seven == 21.0

	def test_div(self):
		assert isinstance(seven / 3, UserFloat)
		assert seven / 3 == UserFloat(7 / 3)
		assert seven / 3 == 7 / 3

	def test_rdiv(self):
		assert isinstance(3 / seven, UserFloat)
		assert 3 / seven == UserFloat(3 / 7)
		assert 3 / seven == UserFloat(3 / 7)
		assert 3 / seven == 3 / 7

	def test_floordiv(self):
		assert isinstance(seven // 3, UserFloat)
		assert seven // 3 == UserFloat(2)
		assert seven // 3 == 2
		assert seven // 3 == 2.0

	def test_rfloordiv(self):
		assert isinstance(21 // seven, UserFloat)
		assert 21 // seven == UserFloat(3)
		assert 21 // seven == 3

	def test_mod(self):
		assert isinstance(seven % 3, UserFloat)
		assert seven % 3 == UserFloat(1)
		assert seven % 3 == 1.0
		assert seven % 3 == 1

	def test_rmod(self):
		assert isinstance(20 % seven, UserFloat)
		assert 20 % seven == UserFloat(6)
		assert 20 % seven == 6.0
		assert 20 % seven == 6

	def test_pow(self):
		assert isinstance(seven**3, UserFloat)
		assert seven**3 == UserFloat(343)
		assert seven**3 == 343.0
		assert seven**3 == 343

	def test_rpow(self):
		assert isinstance(3**seven, UserFloat)
		assert 3**seven == UserFloat(2187)
		assert 3**seven == 2187.0
		assert 3**seven == 2187

	@no_type_check
	def test_round(self):
		assert isinstance(round(seven), int)
		assert round(seven) == 7
		assert isinstance(round(UserFloat(7.5)), int)
		assert round(UserFloat(7.5)) == 8

	def test_repr_str_int(self):
		assert repr(seven) == "7.0"
		assert str(seven) == "7.0"
		assert int(seven) == 7
		assert isinstance(int(seven), int)

	def test_lt(self):
		assert seven < 8
		assert seven < 8.0
		assert seven < UserFloat(8)

	def test_le(self):
		assert seven <= 8
		assert seven <= 8.0
		assert seven <= UserFloat(8)
		assert seven <= 7
		assert seven <= 7.0
		assert seven <= UserFloat(7)

	def test_gt(self):
		assert seven > 6
		assert seven > 6.0
		assert seven > UserFloat(6)

	def test_ge(self):
		assert seven >= 6
		assert seven >= 6.0
		assert seven >= UserFloat(6)
		assert seven >= 7
		assert seven >= 7.0
		assert seven >= UserFloat(7)

	def test_pos(self):
		assert isinstance(+seven, UserFloat)
		assert +seven == seven
		assert +seven == 7
		assert +seven == 7.0

	def test_neg(self):
		assert isinstance(-seven, UserFloat)
		assert -seven == UserFloat(-7)
		assert -seven == -7
		assert -seven == -7.0

	def test_abs(self):
		assert isinstance(abs(+seven), UserFloat)
		assert abs(+seven) == seven
		assert abs(+seven) == 7
		assert abs(+seven) == 7.0

		assert isinstance(abs(-seven), UserFloat)
		assert abs(-seven) == UserFloat(7)
		assert abs(-seven) == 7
		assert abs(-seven) == 7.0

	def test_ne(self):
		assert seven != UserFloat(8)
		assert seven != 8
		assert seven != 8.0

	def test_hash(self):
		assert hash(seven) == hash(UserFloat(7))
		assert hash(seven) != hash(UserFloat(8))
		assert hash(seven) == hash(7)
		assert hash(seven) != hash(8)

	def test_isinstance(self):
		assert isinstance(seven, UserFloat)
		assert not isinstance(seven, float)
		assert not isinstance(7, UserFloat)


# From https://github.com/dgilland/pydash/blob/develop/tests/test_predicates.py
# MIT Licensed


@pytest.mark.parametrize(
		"case,expected",
		[
				(({"name": "fred", "age": 40}, {"age": 40}), True),
				(({"name": "fred", "age": 40}, {"age": 40, "active": True}), False),
				(([1, 2, 3], [1, 2]), True),
				(([1, 2, 3], [1, 2, 3, 4]), False),
				(({}, {}), True),
				(({'a': 1}, {}), True),
				(([], []), True),
				(([1], []), True),
				(([1, 2], [2, 4]), False),
				(([0, 1], [0, 1]), True),
				],
		)
def test_is_match_with(case, expected):
	assert is_match_with(*case) == expected
