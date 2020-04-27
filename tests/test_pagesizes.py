# -*- coding: utf-8 -*-
"""
test_pagesizes
~~~~~~~~~~~~~~~

Test functions in pagesizes.py

"""

import types
import pathlib
import decimal

import pytest

from domdf_python_tools.utils import str2tuple, tuple2str, chunks, list2str, list2string, bdict, pyversion
from domdf_python_tools.pagesizes import *


def test_orientation():
	assert is_portrait(A4)
	assert is_portrait(portrait(A4))
	assert is_portrait(portrait(landscape(A4)))
	assert is_landscape(landscape(A4))
	assert is_landscape((10, 5))
	assert landscape((10, 5)) == (10, 5)
	assert portrait((5, 10)) == (5, 10)
	
	
def test_parse_measurement():
	assert parse_measurement("12mm") == 12*mm
	assert parse_measurement("12 mm") == 12*mm
	assert parse_measurement("12.34 mm") == 12.34*mm
	assert parse_measurement("5inch") == 5*inch
	assert parse_measurement("5in") == 5*inch
