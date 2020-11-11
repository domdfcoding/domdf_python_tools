# stdlib
import inspect
from typing import Any, get_type_hints

# this package
from domdf_python_tools.delegators import delegate_kwargs, delegates


def f(a: int = 1, b: float = 1.1, c: int = 2, d: list = [], e: tuple = (), f: str = '', g: bytes = b'') -> int:
	pass


def test_delegate_kwargs():

	@delegate_kwargs(f)
	def g(b: int, a: int = 7, **kwargs: Any):
		pass

	@delegate_kwargs(f)
	def h(a: int, b: int):
		pass

	sig = inspect.signature(g)
	assert list(sig.parameters.keys()) == ['b', 'a', 'c', 'd', 'e', 'f', 'g']
	assert sig.parameters['a'].default == 7
	assert sig.parameters['b'].default is inspect.Parameter.empty
	assert sig.parameters['c'].default == 2
	assert sig.parameters['d'].default == []
	assert sig.parameters['e'].default == ()
	assert sig.parameters['f'].default == ''
	assert sig.parameters['g'].default == b''
	assert sig.return_annotation is inspect.Parameter.empty  # TODO
	assert get_type_hints(g) == {
			'b': int,
			'a': int,
			'c': int,
			'd': list,
			'e': tuple,
			'f': str,
			'g': bytes,
			"return": int,
			}

	assert list(inspect.signature(h).parameters.keys()) == ['a', 'b']


def test_delegates():

	@delegates(f)
	def g(*args, **kwargs):
		pass

	@delegates(f)
	def h(a: int, b: int):
		pass

	sig = inspect.signature(g)
	assert list(sig.parameters.keys()) == ['a', 'b', 'c', 'd', 'e', 'f', 'g']
	assert sig.parameters['a'].default == 1
	assert sig.parameters['b'].default == 1.1
	assert sig.parameters['c'].default == 2
	assert sig.parameters['d'].default == []
	assert sig.parameters['e'].default == ()
	assert sig.parameters['f'].default == ''
	assert sig.parameters['g'].default == b''
	assert sig.return_annotation == int
	assert get_type_hints(g) == {
			'a': int,
			'b': float,
			'c': int,
			'd': list,
			'e': tuple,
			'f': str,
			'g': bytes,
			"return": int,
			}

	assert list(inspect.signature(h).parameters.keys()) == ['a', 'b']


def test_delegates_method():

	class F:

		@delegates(f)
		def g(self, *args, **kwargs) -> str:
			pass

	sig = inspect.signature(F.g)
	assert list(sig.parameters.keys()) == ["self", 'a', 'b', 'c', 'd', 'e', 'f', 'g']
	assert sig.parameters['a'].default == 1
	assert sig.parameters['b'].default == 1.1
	assert sig.parameters['c'].default == 2
	assert sig.parameters['d'].default == []
	assert sig.parameters['e'].default == ()
	assert sig.parameters['f'].default == ''
	assert sig.parameters['g'].default == b''
	assert sig.return_annotation == str
	assert get_type_hints(F.g) == {
			'a': int,
			'b': float,
			'c': int,
			'd': list,
			'e': tuple,
			'f': str,
			'g': bytes,
			"return": str,
			}
