"""
test_pagesizes
~~~~~~~~~~~~~~~

Test functions in pagesizes.py

"""

# stdlib
from math import isclose
from typing import List, Tuple, Type

# 3rd party
import pytest

# this package
from domdf_python_tools.pagesizes import (
		A0,
		A1,
		A2,
		A3,
		A4,
		A5,
		A6,
		BaseSize,
		PageSize,
		Size_cm,
		Size_inch,
		Size_mm,
		Size_pica,
		Size_um,
		Unit,
		cm,
		convert_from,
		inch,
		mm,
		parse_measurement,
		pc,
		pt,
		um
		)
from domdf_python_tools.pagesizes.utils import _measurement_re


@pytest.mark.parametrize(
		"obj, expects",
		[
				(
						Size_inch(12, 34),
						"Size_inch(width=<Unit '12.000 inch': 864.000pt>, height=<Unit '34.000 inch': 2448.000pt>)",
						),
				(
						Size_cm(12, 34),
						"Size_cm(width=<Unit '12.000 cm': 340.157pt>, height=<Unit '34.000 cm': 963.780pt>)",
						),
				(
						Size_mm(12, 34),
						"Size_mm(width=<Unit '12.000 mm': 34.016pt>, height=<Unit '34.000 mm': 96.378pt>)",
						),
				(
						Size_um(12, 34),
						"Size_um(width=<Unit '12.000 µm': 0.034pt>, height=<Unit '34.000 µm': 0.096pt>)",
						),
				(
						Size_pica(12, 34),
						"Size_pica(width=<Unit '12.000 pc': 144.000pt>, height=<Unit '34.000 pc': 408.000pt>)",
						),
				],
		)
def test_repr(obj: Unit, expects: str):
	assert repr(obj) == expects


@pytest.mark.parametrize(
		"obj, expects",
		[
				(Size_mm(12, 34), "Size_mm(width=12, height=34)"),
				(Size_cm(12, 34), "Size_cm(width=12, height=34)"),
				(Size_um(12, 34), "Size_um(width=12, height=34)"),
				(Size_pica(12, 34), "Size_pica(width=12, height=34)"),
				],
		)
def test_str(obj: Unit, expects: str):
	assert str(obj) == expects


@pytest.mark.parametrize("size", [A6, A5, A4, A3, A2, A1, A0])
def test_orientation(size: BaseSize):
	assert size.is_portrait()
	assert size.portrait().is_portrait()
	assert size.landscape().portrait().is_portrait()
	assert size.landscape().portrait() == size
	assert size.landscape().is_landscape()


def test_base_size():
	assert BaseSize(10, 5) == (10, 5)
	assert BaseSize(10, 5).landscape() == (10, 5)
	assert BaseSize(10, 5).portrait() == (5, 10)


def test_is_square():
	assert BaseSize(10, 10).is_square()
	assert BaseSize(5, 5).is_square()
	assert Size_mm(5, 5).is_square()
	assert Size_um(5, 5).is_square()
	assert Size_inch(5, 5).is_square()


@pytest.mark.parametrize("unit", [pt, inch, cm, mm, um, pc])
def test_convert_size(unit: Unit):
	size = PageSize(12, 34, unit)
	unit_str = unit.name
	if unit_str == "µm":
		unit_str = "um"
	assert isclose(getattr(size, unit_str)[0], 12, abs_tol=1e-8)
	assert isclose(getattr(size, unit_str)[1], 34, abs_tol=1e-8)


#
# @pytest.mark.parametrize(
# 		"size, expected",
# 		[
# 				(sizes.A0, (841, 1189)),
# 				(sizes.A1, (594, 841)),
# 				(sizes.A2, (420, 594)),
# 				(sizes.A3, (297, 420)),
# 				(sizes.A4, (210, 297)),
# 				(sizes.A5, (148, 210)),
# 				(sizes.A6, (105, 148)),
# 				(sizes.A7, (74, 105)),
# 				(sizes.A8, (52, 74)),
# 				(sizes.A9, (37, 52)),
# 				(sizes.A10, (26, 37)),
# 				]
# 		)
# def test_sizes(size, expected):
# 	assert size.mm == expected
#
#
# # TODO: tests for Unit
#


@pytest.mark.parametrize(
		"value, unit, expects",
		[
				(1, pt, 1),
				(1, inch, 72),
				(1, cm, 28.3464566929),
				(1, mm, 2.83464566929),
				(1, um, 0.00283464566929),
				(1, pc, 12),
				(5, pt, 1 * 5),
				(5, inch, 72 * 5),
				(5, cm, 28.3464566929 * 5),
				(5, mm, 2.83464566929 * 5),
				(5, um, 0.00283464566929 * 5),
				(5, pc, 12 * 5),
				([1], pt, (1, )),
				([1], inch, (72, )),
				([1], cm, (28.3464566929, )),
				([1], mm, (2.83464566929, )),
				([1], um, (0.00283464566929, )),
				([1], pc, (12, )),
				([5], pt, (1 * 5, )),
				([5], inch, (72 * 5, )),
				([5], cm, (28.3464566929 * 5, )),
				([5], mm, (2.83464566929 * 5, )),
				([5], um, (0.00283464566929 * 5, )),
				([5], pc, (12 * 5, )),
				([1, 5], pt, (1, 1 * 5)),
				([1, 5], inch, (72, 72 * 5)),
				([1, 5], cm, (28.3464566929, 28.3464566929 * 5)),
				([1, 5], mm, (2.83464566929, 2.83464566929 * 5)),
				([1, 5], um, (0.00283464566929, 0.00283464566929 * 5)),
				([1, 5], pc, (12, 12 * 5)),
				pytest.param(2, 5, 10, id="not isinstance(from_, Unit)"),
				],
		)
def test_convert_from(value: List[int], unit, expects: Tuple[float, ...]):
	assert convert_from(value, unit) == expects


@pytest.mark.parametrize(
		"size, expected, class_",
		[
				((12, 34), PageSize(12, 34), PageSize),
				((12, 34), Size_mm(12, 34), Size_mm),
				],
		)
def test_from_size(size: Tuple[int, int], expected: Unit, class_: Type[BaseSize]):
	print(class_.from_size(size))
	assert class_.from_size(size) == expected


@pytest.mark.parametrize(
		"string, expects",
		[
				("12.34mm", [("12.34", "mm")]),
				("12.34 mm", [("12.34", "mm")]),
				(".34 mm", [(".34", "mm")]),
				("12.34in", [("12.34", "in")]),
				("12.34 in", [("12.34", "in")]),
				(".34 in", [(".34", "in")]),
				('12.34"', [("12.34", '"')]),
				('12.34 "', [("12.34", '"')]),
				('.34 "', [(".34", '"')]),
				('12.34mm .34"', [("12.34", "mm"), (".34", '"')]),
				("12", [("12", '')]),
				('', []),
				("10μm", [("10", "μm")]),
				],
		)
def test_measurement_re(string: str, expects: Unit):
	assert _measurement_re.findall(string) == expects


def test_parse_measurement_errors():
	with pytest.raises(ValueError, match="Too many measurements"):
		parse_measurement('12.34mm .34"')
	with pytest.raises(ValueError, match="Unable to parse measurement"):
		parse_measurement('')
	with pytest.raises(ValueError, match="Unable to parse measurement"):
		parse_measurement("bananas")
	with pytest.raises(ValueError, match="Unable to parse measurement"):
		parse_measurement('')
	with pytest.raises(ValueError, match="Unable to parse measurement"):
		parse_measurement("12")
	with pytest.raises(ValueError, match="Unable to parse measurement"):
		parse_measurement("mm")
	with pytest.raises(ValueError, match="Unknown unit"):
		parse_measurement("12'")


@pytest.mark.parametrize(
		"string, expects",
		[
				("12mm", mm(12)),
				("12 mm", mm(12)),
				("12.34 mm", mm(12.34)),
				("12 um", um(12)),
				("12um", um(12)),
				("12 μm", um(12)),
				("12μm", um(12)),
				("12 µm", um(12)),
				("12µm", um(12)),
				("12 in", inch(12)),
				("12 inch", inch(12)),
				('12"', inch(12)),
				("12 cm", cm(12)),
				("12cm", cm(12)),
				("12 pc", pc(12)),
				("12pc", pc(12)),
				("12 pica", pc(12)),
				("12pica", pc(12)),
				("12 pt", pt(12)),
				("12pt", pt(12)),
				("12mm", 12 * mm),
				("12 mm", 12 * mm),
				("12.34 mm", 12.34 * mm),
				("5inch", 5 * inch),
				("5in", 5 * inch),
				],
		)
def test_parse_measurement(string: str, expects: Unit):
	assert parse_measurement(string) == expects
