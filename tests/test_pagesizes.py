# -*- coding: utf-8 -*-
"""
test_pagesizes
~~~~~~~~~~~~~~~

Test functions in pagesizes.py

"""

from domdf_python_tools.pagesizes import A4, BaseSize, inch, mm, parse_measurement


def test_orientation():
	assert A4.is_portrait()
	assert A4.portrait().is_portrait()
	assert A4.landscape().portrait().is_portrait()
	assert A4.landscape().portrait() == A4
	assert A4.landscape().is_landscape()
	assert BaseSize(10, 5) == (10, 5)
	assert BaseSize(10, 5).landscape() == (10, 5)
	assert BaseSize(10, 5).portrait() == (5, 10)
	
	
def test_parse_measurement():
	assert parse_measurement("12mm") == 12*mm
	assert parse_measurement("12 mm") == 12*mm
	assert parse_measurement("12.34 mm") == 12.34*mm
	assert parse_measurement("5inch") == 5*inch
	assert parse_measurement("5in") == 5*inch
