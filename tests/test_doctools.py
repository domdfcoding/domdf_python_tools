"""
test_doctools
~~~~~~~~~~~~~~~

Test functions in doctools.py

"""

# stdlib
import math
import sys
from typing import Iterable, NamedTuple, get_type_hints

# 3rd party
import pytest
from coincidence import PEP_563, max_version

# this package
from domdf_python_tools import doctools
from domdf_python_tools.bases import Dictable
from domdf_python_tools.compat import PYPY
from domdf_python_tools.doctools import (
		base_int_docstrings,
		base_new_docstrings,
		container_docstrings,
		operator_docstrings,
		prettify_docstrings
		)

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
		"""I will not buy this record, it is scratched.
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
def undocumented_function(a: float, b: float, c: float, d: int) -> float:
	return d * c * b * a


@doctools.append_docstring_from(documented_function)
def partially_documented_function(a: float, b: float, c: float, d: float) -> None:
	"""
	This function works like ``documented_function`` except it returns the result telepathically.
	"""

	d * c * b * a  # pylint: disable=pointless-statement


class DummyClass:

	@doctools.is_documented_by(documented_function)
	def function_in_class_with_same_args(self, a, b, c, d):
		return


@pytest.mark.parametrize(
		"docstring, expects",
		[
				("\t\t\t   ", ''),
				("\t\t\t   Spam", "Spam"),
				("\t\t\t   Spam   \t\t\t", "Spam   \t\t\t"),
				("\t\t\t   Spam\n   \t\t\t", "Spam\n"),
				("   \t\t\t", ''),
				("   \t\t\tSpam", "Spam"),
				("   \t\t\tSpam\t\t\t   ", "Spam\t\t\t   "),
				("   \t\t\tSpam\n\t\t\t   ", "Spam\n"),
				('', ''),
				(None, ''),
				(False, ''),
				(0, ''),
				([], ''),
				]
		)
def test_deindent_string(docstring, expects):
	assert doctools.deindent_string(docstring) == expects


@pytest.mark.xfail(PEP_563, reason="The future of PEP 563 is unclear at this time.")
def test_decorators():
	# Check the ``SpamCafe`` class has has its docstrings modified appropriately.

	# menu and opening_hours should have been copied from menu of the superclass
	assert SpamCafe.menu.__doc__ == Cafe.menu.__doc__
	assert SpamCafe.opening_hours.__doc__ == Cafe.opening_hours.__doc__

	# set_opening_hours and ceil should have extra text at the beginning
	assert SpamCafe.set_opening_hours.__doc__.startswith(  # type: ignore
		"I will not buy this record, it is scratched."
		)
	assert (doctools.deindent_string(SpamCafe.set_opening_hours.__doc__
										)).endswith(doctools.deindent_string(Cafe.set_opening_hours.__doc__))
	# Dedented both strings to be sure of equivalence
	assert SpamCafe.ceil.__doc__.startswith(  # type: ignore
		"I don't know why the cafe has a ceil function, but we'd better document it properly.",
		)
	assert doctools.deindent_string(SpamCafe.ceil.__doc__
									).rstrip().endswith(doctools.deindent_string(math.ceil.__doc__).rstrip())
	# Dedented both strings to be sure of equivalence

	# Functions
	assert undocumented_function.__doc__ == documented_function.__doc__
	assert undocumented_function.__name__ == "undocumented_function"

	if PEP_563:
		assert undocumented_function.__annotations__ == {
				'a': "float", 'b': "float", 'c': "float", 'd': "int", "return": "float"
				}
	else:
		assert undocumented_function.__annotations__ == {
				'a': float, 'b': float, 'c': float, 'd': int, "return": float
				}

	assert partially_documented_function.__doc__.startswith(  # type: ignore
		"This function works like ``documented_function`` except it returns the result telepathically.",
		)
	assert (doctools.deindent_string(partially_documented_function.__doc__
										)).endswith(doctools.deindent_string(documented_function.__doc__))
	# Dedented both strings to be sure of equivalence
	assert DummyClass.function_in_class_with_same_args.__doc__ == documented_function.__doc__
	assert DummyClass.function_in_class_with_same_args.__name__ == "function_in_class_with_same_args"


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
		"Hello"  # noqa: Q002

	def funC():
		"World"  # noqa: Q002

	def funD():
		pass

	assert funB.__doc__ == "Hello"
	assert funC.__doc__ == "World"

	doctools.append_doctring_from_another(funB, funC)
	assert funB.__doc__ == "Hello\n\nWorld\n"

	doctools.append_doctring_from_another(funD, funB)
	assert funD.__doc__ == "Hello\n\nWorld\n"


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
			"pate, brandy and with a fried egg on top and spam.",
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


def test_make_sphinx_links():

	original = """
		This is a docstring that contains references to ``str``, ``int``, ``float`` and ``None``,
		but lacks proper references to them when rendered in Sphinx.

		:return: pi
		:rtype: float
		"""

	sphinx = """
		This is a docstring that contains references to :class:`str`, :class:`int`, :class:`float` and :py:obj:`None`,
		but lacks proper references to them when rendered in Sphinx.

		:return: pi
		:rtype: float
		"""

	assert doctools.make_sphinx_links(original) == sphinx


def test_sphinxify_docstring():

	@doctools.sphinxify_docstring()
	def demo_function():
		"""
		This is a docstring that contains references to ``str``, ``int``, and ``float``
		but lacks proper references to them when rendered in Sphinx.

		:return: pi
		:rtype: float
		"""  # noqa: SXL001

		return math.pi

	if sys.version_info >= (3, 13):
		assert demo_function.__doc__ == """
This is a docstring that contains references to :class:`str`, :class:`int`, and :class:`float`
but lacks proper references to them when rendered in Sphinx.

:return: pi
:rtype: float
"""
	else:
		assert demo_function.__doc__ == """
		This is a docstring that contains references to :class:`str`, :class:`int`, and :class:`float`
		but lacks proper references to them when rendered in Sphinx.

		:return: pi
		:rtype: float
		"""


@prettify_docstrings
class Klasse:

	def __delattr__(self, item): ...

	def __dir__(self): ...

	def __eq__(self, other): ...

	def __getattribute__(self, item): ...

	def __ge__(self, other): ...

	def __gt__(self, other): ...

	def __hash__(self): ...

	def __lt__(self, other): ...

	def __le__(self, other): ...

	def __ne__(self, other): ...

	def __setattr__(self, item, value): ...

	def __sizeof__(self): ...

	def __str__(self): ...

	def __contains__(self, item): ...

	def __getitem__(self, item): ...

	def __setitem__(self, item, value): ...

	def __delitem__(self, item): ...

	def __and__(self): ...

	def __add__(self, other): ...

	def __abs__(self): ...

	def __divmod__(self, other): ...

	def __floordiv__(self, other): ...

	def __invert__(self): ...

	def __lshift__(self, other): ...

	def __mod__(self, other): ...

	def __mul__(self, other): ...

	def __neg__(self): ...

	def __or__(self, other): ...

	def __pos__(self): ...

	def __pow__(self, other): ...

	def __radd__(self, other): ...

	def __rand__(self, other): ...

	def __rdivmod__(self, other): ...

	def __rfloordiv__(self, other): ...

	def __rlshift__(self, other): ...

	def __rmod__(self, other): ...

	def __rmul__(self, other): ...

	def __ror__(self, other): ...

	def __rpow__(self, other): ...

	def __rrshift__(self, other): ...

	def __rshift__(self, other): ...

	def __rsub__(self, other): ...

	def __rtruediv__(self, other): ...

	def __rxor__(self, other): ...

	def __sub__(self, other): ...

	def __truediv__(self, other): ...

	def __xor__(self, other): ...

	def __float__(self): ...

	def __int__(self): ...

	def __repr__(self): ...

	def __bool__(self): ...


def test_prettify_docstrings():

	all_docstrings = {
			**base_new_docstrings,
			**container_docstrings,
			**operator_docstrings,
			**base_int_docstrings,
			}

	for attr_name, docstring in all_docstrings.items():
		if PYPY and attr_name in {"__delattr__", "__dir__"}:
			continue
		assert getattr(Klasse, attr_name).__doc__ == docstring

	assert get_type_hints(Klasse.__eq__)["return"] is bool
	assert get_type_hints(Klasse.__ge__)["return"] is bool
	assert get_type_hints(Klasse.__gt__)["return"] is bool
	assert get_type_hints(Klasse.__lt__)["return"] is bool
	assert get_type_hints(Klasse.__le__)["return"] is bool
	assert get_type_hints(Klasse.__ne__)["return"] is bool
	assert get_type_hints(Klasse.__repr__)["return"] is str
	assert get_type_hints(Klasse.__str__)["return"] is str
	assert get_type_hints(Klasse.__int__)["return"] is int
	assert get_type_hints(Klasse.__float__)["return"] is float
	assert get_type_hints(Klasse.__bool__)["return"] is bool

	assert Klasse.__repr__.__doc__ == "Return a string representation of the :class:`~tests.test_doctools.Klasse`."


@max_version("3.7")
def test_prettify_with_method():

	class F(Iterable):
		pass

	assert prettify_docstrings(F).__getitem__.__doc__ != "Return ``self[key]``."  # type: ignore

	class G(Dictable):
		pass

	assert prettify_docstrings(G).__getitem__.__doc__ != "Return ``self[key]``."  # type: ignore


def test_prettify_namedtuple():

	@prettify_docstrings
	class T(NamedTuple):
		a: str
		b: float

	assert T.__repr__.__doc__ == "Return a string representation of the :class:`~tests.test_doctools.T`."
