from functools import wraps
from types import FunctionType
from typing import Callable, List, NamedTuple


class Factory(NamedTuple):
	func: Callable

	def __call__(self):
		return self.func()

	def __repr__(self) -> str:
		return f"{type(self).__name__}({self.func!r})"


def mutdef(func: FunctionType) -> Callable:

	@wraps(func)
	def wrapper(*args, **kwargs):
		print(func.__defaults__)
		defaults = func.__defaults__ or ()
		func.__defaults__ = tuple(d() if isinstance(d, Factory) else d for d in defaults)

		return func(*args, **kwargs)

	return wrapper


@mutdef  # type: ignore
def foo(name: str, occupations: List[str] = Factory(list)):
	print(f"name={name}")
	print(f"occupations={occupations}")


if __name__ == '__main__':
	foo("Wendy")
	foo("Bob", ["Builder"])
