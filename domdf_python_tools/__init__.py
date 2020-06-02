#  Compiled 2018-2020 by Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  terminal.py
#  		Copyright © 2014-2019 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  		get_terminal_size, _get_terminal_size_windows, _get_terminal_size_tput and _get_terminal_size_linux
# 			from https://gist.github.com/jtriley/1108174
#  			Copyright © 2011 jtriley
#
#  paths.py
# 		Copyright © 2018-2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  		copytree based on https://stackoverflow.com/a/12514470/3092681
# 			Copyright © 2012 atzz
# 			Licensed under CC-BY-SA
#
#  pagesizes.py
# 		Based on reportlab.lib.pagesizes and reportlab.lib.units
# 		    www.reportlab.co.uk
# 		    Copyright ReportLab Europe Ltd. 2000-2017
# 		    Copyright (c) 2000-2018, ReportLab Inc.
# 		    All rights reserved.
# 		    Licensed under the BSD License
#
# 		Includes data from en.wikipedia.org.
# 		Licensed under the Creative Commons Attribution-ShareAlike License
#
#  Parts of the docstrings based on the Python 3.8.2 Documentation
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com . All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives . All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum . All rights reserved.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# this package
from domdf_python_tools import doctools, pagesizes, paths, terminal, utils
from domdf_python_tools.utils import *

__all__ = ["paths", "terminal", "utils", "dates"]

__author__ = "Dominic Davis-Foster"
__copyright__ = "2014-2020 Dominic Davis-Foster"

__license__ = "LGPLv3+"
__version__ = "0.3.4"
__email__ = "dominic@davis-foster.co.uk"
