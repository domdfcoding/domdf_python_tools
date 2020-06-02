# -*- coding: utf-8 -*-
"""
test_pagesizes
~~~~~~~~~~~~~~~

Test functions in pagesizes.py

"""

# 3rd party
import pytest  # type: ignore

# this package
from domdf_python_tools.pagesizes import A4, BaseSize, inch, mm, parse_measurement, sizes


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
	assert parse_measurement("12mm") == 12 * mm
	assert parse_measurement("12 mm") == 12 * mm
	assert parse_measurement("12.34 mm") == 12.34 * mm
	assert parse_measurement("5inch") == 5 * inch
	assert parse_measurement("5in") == 5 * inch


@pytest.mark.parametrize(
		"size, expected",
		[
				(sizes.A0, (841, 1189)),
				(sizes.A1, (594, 841)),
				(sizes.A2, (420, 594)),
				(sizes.A3, (297, 420)),
				(sizes.A4, (210, 297)),
				(sizes.A5, (148, 210)),
				(sizes.A6, (105, 148)),
				(sizes.A7, (74, 105)),
				(sizes.A8, (52, 74)),
				(sizes.A9, (37, 52)),
				(sizes.A10, (26, 37)),
				]
		)
def test_sizes(size, expected):
	assert size.mm == expected


# TODO: tests for Unit
