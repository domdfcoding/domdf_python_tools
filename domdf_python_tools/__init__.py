#  Compiled 2018-2019 by Dominic Davis-Foster <dominic@davis-foster.co.uk>


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

__all__ = ["paths", "terminal", "utils"]

__author__ = "Dominic Davis-Foster"
__copyright__ = "2014-2019 Dominic Davis-Foster"

__license__ = "LGPL"
__version__ = "0.1.12"
__email__ = "dominic@davis-foster.co.uk"


import sys

from . import paths
from . import terminal
from . import utils
from domdf_python_tools.utils import *

pyversion = int(sys.version[0])  # Python Version
