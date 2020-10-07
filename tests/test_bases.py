"""
test_bases
~~~~~~~~~~~~~~~

Test functions in bases.py

"""

# stdlib
import copy
import pickle  # nosec: B101
import sys

# 3rd party
import pytest

# this package
from domdf_python_tools.bases import Dictable, NamedList, UserList, namedlist
from domdf_python_tools.utils import printr, printt


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

	def test_str(self, alice):
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
