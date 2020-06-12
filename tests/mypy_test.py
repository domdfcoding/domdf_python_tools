# stdlib
from typing import Any, Dict

# this package
from domdf_python_tools.bases import Dictable


class MyDictable(Dictable):

	def __init__(self, foo: str, bar: int):
		super().__init__()

		self.foo: str = foo
		self.bar: float = float(bar)

	@property
	def __dict__(self):
		return dict(foo=self.foo, bar=self.bar)


def myfunc() -> Dict[str, Any]:
	a = MyDictable("foo", 12)
	return dict(a)


myfunc()
