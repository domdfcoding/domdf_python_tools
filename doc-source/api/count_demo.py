# stdlib
import itertools

# this package
import domdf_python_tools.iterative

print(domdf_python_tools.iterative.count(14.5, 0.1))

for val in zip(domdf_python_tools.iterative.count(14.5, 0.1), itertools.count(14.5, 0.1)):
	print(val)
	print(val[0] % 0.1, val[1] % 0.1)
	input(">>>")
