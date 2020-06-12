"""
test_doctools
~~~~~~~~~~~~~~~

Test functions in doctools.py

"""

# stdlib
import math

# this package
from domdf_python_tools import doctools

# TODO: test sphinxification of docstrings


class Cafe:
	"""
	Generic class for a Cafe
	"""

	def __init__(self):
		self._dish1 = "egg and bacon"
		self._dish2 = "egg sausage and bacon"
		self._dish3 = "egg and spam"
		self._dish4 = "egg bacon and spam"
		self._opens_at = 7
		self._closes_at = 6

	@property
	def menu(self):
		"""
		Returns the menu of the cafe

		:return:
		:rtype:
		"""
		return [self._dish1, self._dish2, self._dish3, self._dish4]

	@property
	def opening_hours(self):
		"""
		Returns the opening hours of the Cafe

		:rtype: str
		"""

		return f"Open every day {self._opens_at}am - {self._closes_at}pm"

	def set_opening_hours(self, opens_at, closes_at):
		"""
		Sets the opening hours of the Cafe

		:param opens_at:
		:type opens_at:
		:param closes_at:
		:type closes_at:
		:return:
		:rtype:
		"""
		self._opens_at = opens_at
		self._closes_at = closes_at

	@property
	def owner(self):
		"""
		Returns the owner of the Cafe

		:rtype: str
		"""

		return "Unknown"

	@property
	def serves_spam(self):
		"""
		Returns whether the Cafe serves spam

		:rtype: bool
		"""

		return True


class SpamCafe(Cafe):
	"""
	Cafe that serves Spam to Vikings
	"""

	def __init__(self):
		super().__init__()
		self._todays_special = (
				"Lobster Thermidor au Crevette with a Mornay "
				"sauce served in a Provencale manner with "
				"shallots and aubergines garnished with truffle "
				"pate, brandy and with a fried egg on top and spam."
				)

	@doctools.is_documented_by(Cafe.menu)  # type: ignore
	@property
	def menu(self):
		return super().menu + [self._todays_special]

	@doctools.is_documented_by(Cafe.opening_hours)  # type: ignore
	@property
	def opening_hours(self):
		return f"""Open Monday-Saturday {self._opens_at}am - {self._closes_at}pm
Please note our opening hours may vary due to COVID-19"""

	@doctools.append_docstring_from(Cafe.set_opening_hours)
	def set_opening_hours(self, opens_at, closes_at):
		"""
		I will not buy this record, it is scratched.
		"""

		self._opens_at = opens_at
		self._closes_at = closes_at

	@doctools.append_docstring_from(math.ceil)
	def ceil(self, x):
		"""
		I don't know why the cafe has a ceil function, but we'd better document it properly.
		"""

		return math.ceil(x)

	@property
	def owner(self):
		return "Terry Jones"


def documented_function(a: float, b: float, c: float, d: float) -> float:
	"""
	This function is documented. It multiplies the four values `a`, `b`, `c`, and `d` together.

	:type a: float
	:type b: float
	:type c: float
	:type d: float
	"""

	return a * b * c * d


@doctools.is_documented_by(documented_function)
def undocumented_function(a: float, b: float, c: float, d: float) -> float:
	return d * c * b * a


@doctools.append_docstring_from(documented_function)
def partially_documented_function(a: float, b: float, c: float, d: float) -> None:
	"""
	This function works like ``documented_function`` except it returns the result telepathically.
	"""

	d * c * b * a


class DummyClass:

	@doctools.is_documented_by(documented_function)
	def function_in_class_with_same_args(self, a, b, c, d):
		return


def test_deindent_string():
	assert doctools.deindent_string("\t\t\t   ") == ''
	assert doctools.deindent_string("\t\t\t   Spam") == 'Spam'
	assert doctools.deindent_string("\t\t\t   Spam   \t\t\t") == 'Spam   \t\t\t'
	assert doctools.deindent_string("\t\t\t   Spam\n   \t\t\t") == 'Spam\n'
	assert doctools.deindent_string("   \t\t\t") == ''
	assert doctools.deindent_string("   \t\t\tSpam") == 'Spam'
	assert doctools.deindent_string("   \t\t\tSpam\t\t\t   ") == 'Spam\t\t\t   '
	assert doctools.deindent_string("   \t\t\tSpam\n\t\t\t   ") == 'Spam\n'


def test_decorators():
	# Check the ``SpamCafe`` class has has its docstrings modified appropriately.

	# menu and opening_hours should have been copied from menu of the superclass
	assert SpamCafe.menu.__doc__ == Cafe.menu.__doc__
	assert SpamCafe.opening_hours.__doc__ == Cafe.opening_hours.__doc__

	# set_opening_hours and ceil should have extra text at the beginning
	assert SpamCafe.set_opening_hours.__doc__.startswith("\nI will not buy this record, it is scratched.")
	assert doctools.deindent_string(SpamCafe.set_opening_hours.__doc__
									).endswith(doctools.deindent_string(Cafe.set_opening_hours.__doc__))
	# Deindented both strings to be sure of equivalence
	assert SpamCafe.ceil.__doc__.startswith(
			"\nI don't know why the cafe has a ceil function, but we'd better document it properly."
			)
	assert doctools.deindent_string(SpamCafe.ceil.__doc__).endswith(doctools.deindent_string(math.ceil.__doc__))
	# Deindented both strings to be sure of equivalence

	# Functions
	assert undocumented_function.__doc__ == documented_function.__doc__
	assert partially_documented_function.__doc__.startswith(
			"\nThis function works like ``documented_function`` except it returns the result telepathically."
			)
	assert doctools.deindent_string(partially_documented_function.__doc__
									).endswith(doctools.deindent_string(documented_function.__doc__))
	# Deindented both strings to be sure of equivalence
	assert DummyClass.function_in_class_with_same_args.__doc__ == documented_function.__doc__


def test_document_object_from_another():

	def funA():
		pass

	doctools.document_object_from_another(funA, str)
	assert funA.__doc__ == str.__doc__
	doctools.document_object_from_another(funA, int)
	assert funA.__doc__ == int.__doc__
	doctools.document_object_from_another(funA, math.ceil)
	assert funA.__doc__ == math.ceil.__doc__


def test_append_doctring_from_another():

	def funB():
		"""Hello"""

	def funC():
		"""World"""

	assert funB.__doc__ == "Hello"
	assert funC.__doc__ == "World"

	doctools.append_doctring_from_another(funB, funC)
	assert funB.__doc__ == "Hello\nWorld"


def test_still_callable():
	cafe = Cafe()
	assert cafe.menu == [
			"egg and bacon",
			"egg sausage and bacon",
			"egg and spam",
			"egg bacon and spam",
			]
	assert cafe.opening_hours == "Open every day 7am - 6pm"

	cafe.set_opening_hours(9, 5)
	assert cafe.opening_hours == "Open every day 9am - 5pm"
	assert cafe.owner == "Unknown"
	assert cafe.serves_spam is True

	spam_cafe = SpamCafe()
	assert spam_cafe.menu == [
			"egg and bacon",
			"egg sausage and bacon",
			"egg and spam",
			"egg bacon and spam",
			"Lobster Thermidor au Crevette with a Mornay "
			"sauce served in a Provencale manner with "
			"shallots and aubergines garnished with truffle "
			"pate, brandy and with a fried egg on top and spam."
			]
	assert spam_cafe.opening_hours == """Open Monday-Saturday 7am - 6pm
Please note our opening hours may vary due to COVID-19"""
	spam_cafe.set_opening_hours(9, 5)
	assert spam_cafe.opening_hours == """Open Monday-Saturday 9am - 5pm
Please note our opening hours may vary due to COVID-19"""
	assert spam_cafe.owner == "Terry Jones"
	assert spam_cafe.serves_spam is True
	assert spam_cafe.ceil(5.5) == 6

	assert documented_function(1, 2, 3, 4) == 24
	assert undocumented_function(1, 2, 3, 4) == 24
	assert partially_documented_function(1, 2, 3, 4) is None
