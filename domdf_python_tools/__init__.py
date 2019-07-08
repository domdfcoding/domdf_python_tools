#  Compiled 2018-2019 by Dominic Davis-Foster <dominic@davis-foster.co.uk>

#  check_dependencies based on https://stackoverflow.com/a/29044693/3092681
#  		Copyright 2015 TehTechGuy
#		Licensed under CC-BY-SA
#
#  as_text from https://stackoverflow.com/a/40935194
#		Copyright 2016 User3759685
#		Available under the MIT License
#
#  chunks from https://stackoverflow.com/a/312464/3092681
#		Copytight 2008 Ned Batchelder
#		Licensed under CC-BY-SA
#
#
#  terminal.py
#  		Copyright 2014-2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  		get_terminal_size, _get_terminal_size_windows, _get_terminal_size_tput and _get_terminal_size_linux
#			from https://gist.github.com/jtriley/1108174
#  			Copyright 2011 jtriley
#
#  paths.py
#		Copyright 2018-2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  		copytree based on https://stackoverflow.com/a/12514470/3092681
#			Copyright 2012 atzz
#			Licensed under CC-BY-SA
#

__all__ = ["paths", "terminal"]

__author__ = "Dominic Davis-Foster"
__copyright__ = "Copyright 2014-2019 Dominic Davis-Foster"

__license__ = "LGPL"
__version__ = "0.1.1"
__email__ = "dominic@davis-foster.co.uk"


import sys

from . import paths
from . import terminal

pyversion = int(sys.version[0])  # Python Version


def as_text(value):
	if value is None:
		return ""
	return str(value)


def str2tuple(input_string, sep=","):
	"""
	Convert a comma-seperated string of integers into a tuple
	
	:param input_string: The string to be converted into a tuple
	:type input_string: str
	:param sep: The separator in the string, default ","
	:type sep: str
	
	:rtype: tuple
	"""
	
	return tuple(int(x) for x in input_string.split(sep))


def tuple2str(input_tuple, sep=","):
	"""
	Convert a tuple into a comma-seperated string

	:param input_tuple: The tuple to be joined into a string
	:type input_tuple: tuple
	:param sep: The separator in the string, default ","
	:type sep: str

	:rtype: str
	"""
	
	return sep.join([str(x) for x in input_tuple])


def chunks(l, n):
	"""
	Yield successive n-sized chunks from l.
	
	:param l:
	:param n:
	:return:
	"""
	
	for i in range(0, len(l), n):
		yield l[i:i + n]


def check_dependencies(dependencies, prt=True):
	from pkgutil import iter_modules
	modules = set(x[1] for x in iter_modules())
	
	missing_modules = []
	for requirement in dependencies:
		if not requirement in modules:
			missing_modules.append(requirement)
	
	if prt:
		if len(missing_modules) == 0:
			print("All modules installed")
		else:
			print("""\rThe following modules are missing.
	Please check the documentation.""")
			print(missing_modules)
		print("")
	
	else:
		return missing_modules


def list2string(the_list, sep=","):
	return list2str(the_list, sep)


def list2str(the_list, sep=","):
	return sep.join([str(x) for x in the_list])