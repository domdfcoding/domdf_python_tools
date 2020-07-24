# stdlib
import re
from operator import floordiv, truediv

# 3rd party
import pytest

# this package
from domdf_python_tools.pagesizes.units import Unit, Unitcm, UnitInch, Unitmm, Unitpc, Unitpt, Unitum


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
def test_repr(unit):
	assert re.match(r"<Unit '12\.000 .*': .*pt", repr(unit))


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
def test_str(unit):
	assert re.match(r"<Unit '12\.000\u205F.*': .*pt", str(unit))


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", (Unit(x) for x in range(0, 1000, 10)))
def test_mul_errors(unit, obj):
	with pytest.raises(NotImplementedError, match="Multiplying a unit by another unit is not allowed."):
		Unit(17) * obj


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", range(0, 1000, 10))
def test_mul(unit, obj: int):
	assert obj * Unit(17) == obj * 17
	assert obj * Unit(17 / 2) == obj * (17 / 2)


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", (Unit(x) for x in range(0, 1000, 10)))
def test_rmul_errors(unit, obj):
	with pytest.raises(NotImplementedError, match="Multiplying a unit by another unit is not allowed."):
		obj * Unit(17)


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", range(1, 1000, 10))
def test_truediv(unit, obj: int):
	assert truediv(Unit(17), obj) == 17 / obj
	assert truediv(Unit(17 / 2), obj) == (17 / 2) / obj


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", (Unit(x) for x in range(0, 1000, 10)))
def test_truediv_errors(unit, obj):
	with pytest.raises(NotImplementedError, match="Dividing a unit by another unit is not allowed."):
		truediv(Unit(17), obj)
	with pytest.raises(NotImplementedError, match="Dividing a unit by another unit is not allowed."):
		truediv(obj, Unit(17))


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", range(1, 1000, 10))
def test_floordiv(unit, obj: int):
	assert floordiv(Unit(17), obj) == 17 // obj
	assert floordiv(Unit(17 / 2), obj) == (17 / 2) // obj


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", (Unit(x) for x in range(0, 1000, 10)))
def test_floordiv_errors(unit, obj):
	with pytest.raises(NotImplementedError, match="Dividing a unit by another unit is not allowed."):
		floordiv(Unit(17), obj)
	with pytest.raises(NotImplementedError, match="Dividing a unit by another unit is not allowed."):
		floordiv(obj, Unit(17))


# TODO eq


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", (Unit(x) for x in range(0, 1000, 10)))
def test_modulo_errors(unit, obj):
	with pytest.raises(NotImplementedError, match="Modulo division of a unit by another unit is not allowed."):
		Unit(17) % obj
	with pytest.raises(NotImplementedError, match="Modulo division of a unit by another unit is not allowed."):
		obj % Unit(17)


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", range(1, 1000, 10))
def test_modulo(unit, obj: int):
	assert Unit(17) % obj == 17 % obj


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", [Unit(x) for x in range(0, 1000, 10)] + list(range(0, 1000, 10)))
def test_pow_errors(unit, obj):
	with pytest.raises(NotImplementedError, match="Powers are not supported for units."):
		Unit(17)**obj

	if isinstance(obj, Unit):
		with pytest.raises(NotImplementedError, match="Powers are not supported for units."):
			obj**Unit(17)


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", (range(0, 1000, 10)))
def test_rtruediv_errors(unit, obj):
	with pytest.raises(NotImplementedError, match="Dividing by a unit is not allowed."):
		truediv(obj, Unit(17))


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", range(0, 1000, 10))
def test_add_unit(unit, obj: int):
	assert isinstance(unit + Unit(obj), Unit)
	assert (unit + Unit(obj)).name == unit.name
	assert (unit + Unit(obj)).as_pt() == unit.as_pt() + obj


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", range(0, 1000, 10))
def test_radd_unit(unit, obj: int):
	assert isinstance(Unit(obj) + unit, Unit)
	assert (Unit(obj) + unit).name == "pt"
	assert (Unit(obj) + unit).as_pt() == unit.as_pt() + obj


@pytest.mark.parametrize("obj", range(0, 1000, 10))
def test_add_number(obj: int):

	assert isinstance(Unit(12) + obj, Unit)
	assert (Unit(12) + obj).name == "pt"
	assert (Unit(12) + obj).as_pt() == 12 + obj

	assert isinstance(UnitInch(1) + obj, Unit)
	assert (UnitInch(1) + obj).name == "inch"
	assert (UnitInch(1) + obj) == UnitInch.from_pt(72) + obj


@pytest.mark.parametrize("obj", range(0, 1000, 10))
def test_radd_number(obj: int):
	assert isinstance(obj + Unit(12), Unit)
	assert (obj + Unit(12)).name == "pt"
	assert (obj + Unit(12)).as_pt() == 12 + obj

	assert isinstance(obj + UnitInch(1), Unit)
	assert (obj + UnitInch(1)).name == "inch"
	assert (obj + UnitInch(1)) == UnitInch.from_pt(72) + obj


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", range(0, 1000, 10))
def test_sub_unit(unit, obj: int):
	assert isinstance(unit + Unit(obj), Unit)
	assert (unit - Unit(obj)).name == unit.name
	assert (unit - Unit(obj)).as_pt() == unit.as_pt() - obj


@pytest.mark.parametrize(
		"unit", [Unit(12), UnitInch(12), Unitcm(12), Unitmm(12), Unitpc(12), Unitpt(12), Unitum(12)]
		)
@pytest.mark.parametrize("obj", range(0, 1000, 10))
def test_rsub_unit(unit, obj: int):
	assert isinstance(Unit(obj) - unit, Unit)
	assert (Unit(obj) - unit).name == "pt"
	assert (Unit(obj) - unit).as_pt() == obj - unit.as_pt()


@pytest.mark.parametrize("obj", range(0, 1000, 10))
def test_sub_number(obj: int):

	assert isinstance(Unit(12) - obj, Unit)
	assert (Unit(12) - obj).name == "pt"
	assert (Unit(12) - obj).as_pt() == 12 - obj

	assert isinstance(UnitInch(1) - obj, Unit)
	assert (UnitInch(1) - obj).name == "inch"
	assert (UnitInch(1) - obj) == UnitInch.from_pt(72) - obj


@pytest.mark.parametrize("obj", range(0, 1000, 10))
def test_rsub_number(obj: int):
	assert isinstance(obj + Unit(12), Unit)
	assert (obj - Unit(12)).name == "pt"
	assert (obj - Unit(12)).as_pt() == obj - 12

	assert isinstance(obj - UnitInch(1), Unit)
	assert (obj - UnitInch(1)).name == "inch"
	assert (obj - UnitInch(1)) == obj - UnitInch.from_pt(72)
