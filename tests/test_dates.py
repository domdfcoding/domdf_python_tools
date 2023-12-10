"""
test_dates
~~~~~~~~~~~~~~~

Test functions in dates.py

"""

# stdlib
import re
from datetime import date, datetime, timedelta
from typing import Union

# 3rd party
import pytest
from coincidence.params import count

# this package
from domdf_python_tools import dates

# TODO: test get_timezone

try:
	# 3rd party
	import pytz

	test_date = datetime(1996, 10, 13, 2, 20).replace(tzinfo=pytz.utc)
	today = datetime.now(pytz.utc)  # make sure UTC

	def test_utc_offset():
		# Check that the correct UTC offsets are given for common timezones
		assert dates.get_utc_offset("US/Pacific", test_date) == timedelta(-1, 61200)
		assert dates.get_utc_offset("Europe/London", test_date) == timedelta(0, 3600)
		assert dates.get_utc_offset("Africa/Algiers", test_date) == timedelta(0, 3600)
		# TODO: Finish

		# Check that the correct UTC offsets are given for common timezones for today
		assert dates.get_utc_offset("US/Pacific", today) in {
				timedelta(-1, 57600),
				timedelta(-1, 61200),
				}
		assert dates.get_utc_offset("Europe/London", today) in {
				timedelta(0, 3600),  # BST
				timedelta(0, 0),
				}
		assert dates.get_utc_offset("Africa/Algiers", today) == timedelta(0, 3600)

		# Check that the correct UTC offsets are given for common timezones when ``date`` is not given
		assert dates.get_utc_offset("US/Pacific") in {
				timedelta(-1, 57600),
				timedelta(-1, 61200),
				}
		assert dates.get_utc_offset("Europe/London") in {
				timedelta(0, 3600),  # BST
				timedelta(0, 0),
				}
		assert dates.get_utc_offset("Africa/Algiers") == timedelta(0, 3600)

	def test_converting_timezone():
		# No matter what timezone we convert to the timestamp should be the same
		for tz in pytz.all_timezones:
			assert test_date.astimezone(dates.get_timezone(tz, test_date),
										).timestamp() == test_date.timestamp() == 845173200.0

			if dates.get_utc_offset(tz, test_date):  # otherwise the timezone stayed as UTC
				assert test_date.astimezone(dates.get_timezone(tz, test_date)).hour != test_date.hour

			# And again with today's date
			assert today.astimezone(dates.get_timezone(tz, today)).timestamp() == today.timestamp()
			if dates.get_utc_offset(tz, today):  # otherwise the timezone stayed as UTC
				assert today.astimezone(dates.get_timezone(tz, today)).hour != today.hour

	def test_utc_timestamp_to_datetime():
		# Going from a datetime object to timezone and back should give us the same object
		for tz in pytz.all_timezones:
			tzinfo = dates.get_timezone(tz, test_date)
			dt = test_date.astimezone(tzinfo)
			assert dates.utc_timestamp_to_datetime(dt.timestamp(), tzinfo) == dt

			# And again with today's date
			tzinfo = dates.get_timezone(tz, today)
			dt = today.astimezone(tzinfo)
			assert dates.utc_timestamp_to_datetime(dt.timestamp(), tzinfo) == dt

	@pytest.mark.xfail()
	def test_set_timezone():
		# Setting the timezone should change the timestamp
		for tz in pytz.all_timezones:

			if dates.get_utc_offset(tz, today):  # otherwise the timezone stayed as UTC
				# ensure timestamp did change
				target_tz = dates.get_timezone(tz, today)
				assert target_tz is not None

				assert dates.set_timezone(today, target_tz).timestamp() != today.timestamp()

				# Difference between "today" and the new timezone should be the timezone difference
				target_tz = dates.get_timezone(tz, today)
				assert target_tz is not None

				utc_offset = dates.get_utc_offset(tz, today)
				assert utc_offset is not None

				as_seconds = dates.set_timezone(today, target_tz).timestamp() + utc_offset.total_seconds()

				assert as_seconds == today.timestamp()

			if tz in {
					"America/Punta_Arenas",
					"America/Santiago",
					"Antarctica/Palmer",
					"Chile/Continental",
					"Chile/EasterIsland",
					"Pacific/Easter",
					}:
				continue

			if dates.get_utc_offset(tz, test_date):  # otherwise the timezone stayed as UTC
				# print(dates.set_timezone(test_date, get_timezone(tz, test_date)).timestamp())
				# print(repr(test_date))
				# print(get_utc_offset(tz, test_date).total_seconds())
				# print(test_date.timestamp())
				# print(repr(dates.set_timezone(test_date, get_timezone(tz, test_date))))
				# print(dates.set_timezone(test_date, get_timezone(tz, test_date)).timestamp())
				# print(dates.set_timezone(test_date, get_timezone(tz, test_date)).timestamp() + get_utc_offset(tz, test_date).total_seconds())
				# print(get_utc_offset(tz, test_date).total_seconds())
				# print(
				# 		dates.set_timezone(test_date, get_timezone(tz, test_date)).timestamp() +
				# 		get_utc_offset(tz, test_date).total_seconds()
				#
				# 		)
				target_tz = dates.get_timezone(tz, test_date)
				assert target_tz is not None

				offset = dates.get_utc_offset(tz, test_date)
				assert offset is not None

				as_seconds = dates.set_timezone(test_date, target_tz).timestamp() + offset.total_seconds()
				assert as_seconds == test_date.timestamp()

except ImportError:

	def test_utc_offset_no_pytz():
		with pytest.raises(
				ImportError,
				match=r"'get_utc_offset' requires pytz \(.*\), but it could not be imported",
				):
			dates.get_utc_offset  # pylint: disable=pointless-statement

		with pytest.raises(
				ImportError,
				match=r"'get_utc_offset' requires pytz \(.*\), but it could not be imported",
				):

			# this package
			from domdf_python_tools.dates import get_utc_offset  # noqa: F401


# TODO: Finish

# import sys
# from importlib.abc import MetaPathFinder
#
# class NoPytzPath(MetaPathFinder):
#
# 	def find_spec(self, fullname, path, target=None):
# 		if fullname == "pytz":
# 			raise ModuleNotFoundError(f"No module named '{fullname}'")
#
#
# class TestDatesNoPytz:
#
# 	def test_import_pytz(self, fake_no_pytz):
# 		with pytest.raises(ImportError):
# 			import pytz
# 		# this package
# 		from domdf_python_tools import dates
#
# 		with pytest.raises(ImportError):
# 			# 3rd party
# 			import pytz
#
# 	def test_utc_offset_no_pytz(self, fake_no_pytz):
# 		# this package
# 		from domdf_python_tools import dates
#
# 		print(sys.modules.keys())
#
# 		with pytest.raises(
# 				ImportError,
# 				match=r"'get_utc_offset' requires pytz \(.*\), but it could not be imported",
# 				):
# 			dates.get_utc_offset  # pylint: disable=pointless-statement
#
# 		with pytest.raises(
# 				ImportError,
# 				match=r"'get_utc_offset' requires pytz \(.*\), but it could not be imported",
# 				):
#
# 			# this package
# 			from domdf_python_tools.dates import get_utc_offset


@pytest.mark.parametrize("month_idx, month", enumerate(dates.month_full_names))
def test_parse_month(month_idx: int, month: str):
	month_idx += 1  # to make 1-indexed

	for i in range(3, len(month)):
		assert dates.parse_month(month.lower()[:i]) == month
		assert dates.parse_month(month.upper()[:i]) == month
		assert dates.parse_month(month.capitalize()[:i]) == month

	assert dates.parse_month(month_idx) == month


def test_parse_month_errors():
	for value in ["abc", 0, '0', -1, "-1", 13, "13"]:
		with pytest.raises(ValueError, match=fr"The given month \({value!r}\) is not recognised."):
			dates.parse_month(value)  # type: ignore


@pytest.mark.parametrize("month_idx, month", enumerate(dates.month_full_names))
def test_get_month_number_from_name(month_idx: int, month: str):
	month_idx += 1  # to make 1-indexed

	for i in range(3, len(month)):
		assert dates.get_month_number(month.lower()[:i]) == month_idx
		assert dates.get_month_number(month.upper()[:i]) == month_idx
		assert dates.get_month_number(month.capitalize()[:i]) == month_idx

	assert dates.get_month_number(month) == month_idx


@count(13, 1)
def test_get_month_number_from_no(count: int):
	assert dates.get_month_number(count) == count


@pytest.mark.parametrize(
		"value, match",
		[
				(0, "The given month (0) is not recognised."),
				(-1, "The given month (-1) is not recognised."),
				(13, "The given month (13) is not recognised."),
				("abc", "The given month ('abc') is not recognised."),
				('0', "The given month ('0') is not recognised."),
				("-1", "The given month ('-1') is not recognised."),
				("13", "The given month ('13') is not recognised."),
				]
		)
def test_get_month_number_errors(value: Union[str, int], match: str):
	with pytest.raises(ValueError, match=re.escape(match)):
		dates.get_month_number(value)


def test_check_date():
	for month_idx, month in enumerate(dates.month_full_names):

		month_idx += 1  # to make 1-indexed

		if month_idx in {9, 4, 6, 11}:
			max_day = 30
		elif month_idx == 2:
			max_day = 28
		else:
			max_day = 31

		for day in range(-5, 36):
			if month_idx == 2 and day == 29:
				for i in range(3, len(month)):
					assert dates.check_date(month.lower()[:i], 29)
					assert dates.check_date(month.upper()[:i], 29)
					assert dates.check_date(month.capitalize()[:i], 29)

					assert not dates.check_date(month.lower()[:i], 29, False)
					assert not dates.check_date(month.upper()[:i], 29, False)
					assert not dates.check_date(month.capitalize()[:i], 29, False)

				assert dates.check_date(month, 29)
				assert not dates.check_date(month, 29, False)

			elif 0 < day <= max_day:
				for i in range(3, len(month)):
					assert dates.check_date(month.lower()[:i], day)
					assert dates.check_date(month.upper()[:i], day)
					assert dates.check_date(month.capitalize()[:i], day)

				assert dates.check_date(month, day)

			else:
				for i in range(3, len(month)):
					assert not dates.check_date(month.lower()[:i], day)
					assert not dates.check_date(month.upper()[:i], day)
					assert not dates.check_date(month.capitalize()[:i], day)

				assert not dates.check_date(month, day)


@pytest.mark.parametrize(
		"date",
		[
				date(2000, 4, 23),
				date(2001, 4, 15),
				date(2002, 3, 31),
				date(2003, 4, 20),
				date(2004, 4, 11),
				date(2005, 3, 27),
				date(2006, 4, 16),
				date(2007, 4, 8),
				date(2008, 3, 23),
				date(2009, 4, 12),
				date(2010, 4, 4),
				date(2011, 4, 24),
				date(2012, 4, 8),
				date(2013, 3, 31),
				date(2014, 4, 20),
				date(2015, 4, 5),
				date(2016, 3, 27),
				date(2017, 4, 16),
				date(2018, 4, 1),
				date(2019, 4, 21),
				date(2020, 4, 12),
				date(2021, 4, 4),
				]
		)
def test_calc_easter(date):
	assert dates.calc_easter(date.year) == date


@pytest.mark.parametrize(
		"the_date, result",
		[
				(date(month=3, day=2, year=2019), False),
				(date(month=4, day=7, year=2020), True),
				(date(month=8, day=17, year=2015), True),
				(date(month=12, day=25, year=2030), False),
				(date(month=3, day=29, year=2019), False),
				(date(month=3, day=30, year=2019), False),
				(date(month=3, day=31, year=2019), True),
				(date(month=4, day=1, year=2019), True),
				(date(month=10, day=25, year=2019), True),
				(date(month=10, day=26, year=2019), True),
				(date(month=10, day=27, year=2019), False),
				(date(month=10, day=28, year=2019), False),
				(date(month=3, day=27, year=2020), False),
				(date(month=3, day=28, year=2020), False),
				(date(month=3, day=29, year=2020), True),
				(date(month=3, day=30, year=2020), True),
				(date(month=10, day=23, year=2020), True),
				(date(month=10, day=24, year=2020), True),
				(date(month=10, day=25, year=2020), False),
				(date(month=10, day=26, year=2020), False),
				(date(month=3, day=26, year=2021), False),
				(date(month=3, day=27, year=2021), False),
				(date(month=3, day=28, year=2021), True),
				(date(month=3, day=29, year=2021), True),
				(date(month=10, day=29, year=2021), True),
				(date(month=10, day=30, year=2021), True),
				(date(month=10, day=31, year=2021), False),
				(date(month=11, day=1, year=2021), False),
				(date(month=3, day=25, year=2022), False),
				(date(month=3, day=26, year=2022), False),
				(date(month=3, day=27, year=2022), True),
				(date(month=3, day=28, year=2022), True),
				(date(month=10, day=28, year=2022), True),
				(date(month=10, day=29, year=2022), True),
				(date(month=10, day=30, year=2022), False),
				(date(month=10, day=31, year=2022), False),
				(date(month=3, day=24, year=2023), False),
				(date(month=3, day=25, year=2023), False),
				(date(month=3, day=26, year=2023), True),
				(date(month=3, day=27, year=2023), True),
				(date(month=10, day=27, year=2023), True),
				(date(month=10, day=28, year=2023), True),
				(date(month=10, day=29, year=2023), False),
				(date(month=10, day=30, year=2023), False),
				(date(month=3, day=29, year=2024), False),
				(date(month=3, day=30, year=2024), False),
				(date(month=3, day=31, year=2024), True),
				(date(month=4, day=1, year=2024), True),
				(date(month=10, day=25, year=2024), True),
				(date(month=10, day=26, year=2024), True),
				(date(month=10, day=27, year=2024), False),
				(date(month=10, day=28, year=2024), False),
				]
		)
def test_is_bst(the_date, result: bool):
	assert dates.is_bst(the_date) is result
