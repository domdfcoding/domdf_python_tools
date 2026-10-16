"""
test_dates
~~~~~~~~~~~~~~~

Test functions in dates.py

"""

# stdlib
import io
import re
from datetime import date, datetime, time, timedelta, timezone
from typing import Any, Callable, Union

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


@pytest.mark.parametrize("month_idx, month", list(enumerate(dates.month_full_names)))
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
			dates.parse_month(value)  # type: ignore[arg-type]


@pytest.mark.parametrize("month_idx, month", list(enumerate(dates.month_full_names)))
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
				],
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
				],
		)
def test_calc_easter(date: date):
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
				],
		)
def test_is_bst(the_date: date, result: bool):
	assert dates.is_bst(the_date) is result


def test_time_from_isoformat():
	assert dates.time_from_isoformat("03:18:47.78") == time(3, 18, 47, 780000)


def test_datetime_from_isoformat():
	assert dates.datetime_from_isoformat("2026-10-15T03:18:47.78431+02:00") == datetime(
			2026,
			10,
			15,
			3,
			18,
			47,
			784310,
			tzinfo=timezone(timedelta(seconds=2 * 60 * 60)),
			)


def test_date_from_isoformat():
	# Test that isoformat() is reversible
	base_dates = [
			(1, 1, 1),
			(1000, 2, 14),
			(1900, 1, 1),
			(2000, 2, 29),
			(2004, 11, 12),
			(2004, 4, 3),
			(2017, 5, 30),
			]

	for dt_tuple in base_dates:
		dt = date(*dt_tuple)
		dt_rt = dates.date_from_isoformat(dt.isoformat())

		assert dt == dt_rt


def test_date_from_isoformat_date_examples():
	examples = [
			("00010101", date(1, 1, 1)),
			("20000101", date(2000, 1, 1)),
			("20250102", date(2025, 1, 2)),
			("99991231", date(9999, 12, 31)),
			("0001-01-01", date(1, 1, 1)),
			("2000-01-01", date(2000, 1, 1)),
			("2025-01-02", date(2025, 1, 2)),
			("9999-12-31", date(9999, 12, 31)),
			("2025W01", date(2024, 12, 30)),
			("2025-W01", date(2024, 12, 30)),
			("2025W014", date(2025, 1, 2)),
			("2025-W01-4", date(2025, 1, 2)),
			("2026W01", date(2025, 12, 29)),
			("2026-W01", date(2025, 12, 29)),
			("2026W013", date(2025, 12, 31)),
			("2026-W01-3", date(2025, 12, 31)),
			("2022W52", date(2022, 12, 26)),
			("2022-W52", date(2022, 12, 26)),
			("2022W527", date(2023, 1, 1)),
			("2022-W52-7", date(2023, 1, 1)),
			("2015W534", date(2015, 12, 31)),  # Has week 53
			("2015-W53-4", date(2015, 12, 31)),  # Has week 53
			("2015-W53-5", date(2016, 1, 1)),
			("2020W531", date(2020, 12, 28)),  # Leap year
			("2020-W53-1", date(2020, 12, 28)),  # Leap year
			("2020-W53-6", date(2021, 1, 2)),
			("2028-02-29", date(2028, 2, 29)),
			]

	for input_str, expected in examples:
		actual = dates.date_from_isoformat(input_str)
		assert actual == expected


def test_date_from_isoformat_fails():
	# Test that fromisoformat() fails on invalid values
	bad_strs = [
			'',  # Empty string
			'\ud800',  # bpo-34454: Surrogate code point
			"009-03-04",  # Not 10 characters
			"123456789",  # Not a date
			"200a-12-04",  # Invalid character in year
			"2009-1a-04",  # Invalid character in month
			"2009-12-0a",  # Invalid character in day
			"2009-01-32",  # Invalid day
			"2009-02-29",  # Invalid leap day
			"2019-W53-1",  # No week 53 in 2019
			"2020-W54-1",  # No week 54
			"0000-W25-1",  # Invalid year
			"10000-W25-1",  # Invalid year
			"2020-W25-0",  # Invalid day-of-week
			"2020-W25-8",  # Invalid day-of-week
			# gh-152204: each fixed-width field must be exactly N ASCII digits
			"2020+12",  # '+' in a basic-format field
			"2020 12",  # space in a basic-format field
			"+020-06-15",  # leading sign in the year
			"202012+9",  # '+' in the day field
			"2020-W 5",  # space in the week number
			"2020061",  # 7 chars: day slice reads a 1-character tail
			"2020-W2",  # 1-digit week number
			"٢025-03-09",  # Unicode characters
			"2009\ud80002\ud80028",  # Separators are surrogate codepoints
			]

	for bad_str in bad_strs:
		with pytest.raises(ValueError, match="^(Invalid isoformat string:|Argument must be an ASCII str)"):
			dates.date_from_isoformat(bad_str)


@pytest.mark.parametrize(
		"fn",
		[dates.datetime_from_isoformat, dates.time_from_isoformat, dates.date_from_isoformat],
		)
def test_from_isoformat_fails_typeerror(fn: Callable[[str], Any]):
	# Test that fromisoformat fails when passed the wrong type
	bad_types = [b'2009-03-01', None, io.StringIO("2009-03-01")]
	for bad_type in bad_types:
		with pytest.raises(TypeError, match="^fromisoformat: argument must be a str"):
			fn(bad_type)  # type: ignore[arg-type]


def test_datetime_from_isoformat_datetime():
	# Test that isoformat() is reversible
	base_dates = [
			(1, 1, 1),
			(1900, 1, 1),
			(2004, 11, 12),
			(2017, 5, 30),
			]

	base_times = [
			(0, 0, 0, 0),
			(0, 0, 0, 241000),
			(0, 0, 0, 234567),
			(12, 30, 45, 234567),
			]

	separators = [' ', 'T']

	tzinfos = [
			None,
			timezone.utc,
			timezone(timedelta(hours=-5)),
			timezone(timedelta(hours=2)),
			]

	dts = [
			datetime(*date_tuple, *time_tuple, tzinfo=tzi)
			for date_tuple in base_dates
			for time_tuple in base_times
			for tzi in tzinfos
			]

	for dt in dts:
		for sep in separators:
			dtstr = dt.isoformat(sep=sep)
			dt_rt = dates.datetime_from_isoformat(dtstr)
			assert dt == dt_rt


def test_datetime_from_isoformat_timezone():
	base_dt = datetime(2014, 12, 30, 12, 30, 45, 217456)

	tzoffsets = [
			timedelta(hours=5),
			timedelta(hours=2),
			timedelta(hours=6, minutes=27),
			timedelta(hours=12, minutes=32, seconds=30),
			timedelta(hours=2, minutes=4, seconds=9, microseconds=123456),
			]

	tzoffsets += [-1 * td for td in tzoffsets]

	tzinfos = [
			None,
			timezone.utc,
			timezone(timedelta(hours=0)),
			]

	tzinfos += [timezone(td) for td in tzoffsets]

	for tzi in tzinfos:
		dt = base_dt.replace(tzinfo=tzi)
		dtstr = dt.isoformat()
		dt_rt = dates.datetime_from_isoformat(dtstr)
		assert dt_rt == dt


def test_datetime_from_isoformat_separators():
	separators = [
			' ',
			'T',
			'\x7f',  # 1-bit widths
			'\x80',
			'ʁ',  # 2-bit widths
			'ᛇ',
			'時',  # 3-bit widths
			'🐍',  # 4-bit widths
			'\ud800',  # bpo-34454: Surrogate code point
			]

	for sep in separators:
		dt = datetime(2018, 1, 31, 23, 59, 47, 124789)
		dtstr = dt.isoformat(sep=sep)
		dt_rt = dates.datetime_from_isoformat(dtstr)
		assert dt == dt_rt


def test_datetime_from_isoformat_ambiguous():
	# Test strings like 2018-01-31+12:15 (where +12:15 is not a time zone)
	separators = ['+', '-']
	for sep in separators:
		dt = datetime(2018, 1, 31, 12, 15)
		dtstr = dt.isoformat(sep=sep)
		dt_rt = dates.datetime_from_isoformat(dtstr)
		assert dt == dt_rt


def test_datetime_from_isoformat_timespecs():
	datetime_bases = [
			(2009, 12, 4, 8, 17, 45, 123456),
			(2009, 12, 4, 8, 17, 45, 0),
			]

	tzinfos = [
			None,
			timezone.utc,
			timezone(timedelta(hours=-5)),
			timezone(timedelta(hours=2)),
			timezone(timedelta(hours=6, minutes=27)),
			]

	timespecs = [
			"hours",
			"minutes",
			"seconds",
			"milliseconds",
			"microseconds",
			]

	for ip, ts in enumerate(timespecs):
		for tzi in tzinfos:
			for dt_tuple in datetime_bases:
				if ts == "milliseconds":
					new_microseconds = 1000 * (dt_tuple[6] // 1000)
					dt_tuple = dt_tuple[0:6] + (new_microseconds, )

				dt = datetime(*(dt_tuple[0:(4 + ip)]), tzinfo=tzi)  # type: ignore[misc,arg-type]
				dtstr = dt.isoformat(timespec=ts)
				dt_rt = dates.datetime_from_isoformat(dtstr)
				assert dt == dt_rt


def test_datetime_from_isoformat_datetime_examples():
	UTC = timezone.utc
	BST = timezone(timedelta(hours=1), "BST")
	EST = timezone(timedelta(hours=-5), "EST")
	EDT = timezone(timedelta(hours=-4), "EDT")
	examples = [
			("2025-01-02", datetime(2025, 1, 2, 0, 0)),
			("2025-01-02T03", datetime(2025, 1, 2, 3, 0)),
			("2025-01-02T03:04", datetime(2025, 1, 2, 3, 4)),
			("2025-01-02T0304", datetime(2025, 1, 2, 3, 4)),
			("2025-01-02T03:04:05", datetime(2025, 1, 2, 3, 4, 5)),
			("2025-01-02T030405", datetime(2025, 1, 2, 3, 4, 5)),
			(
					"2025-01-02T03:04:05.6",
					datetime(2025, 1, 2, 3, 4, 5, 600000),
					),
			(
					"2025-01-02T03:04:05,6",
					datetime(2025, 1, 2, 3, 4, 5, 600000),
					),
			(
					"2025-01-02T03:04:05.678",
					datetime(2025, 1, 2, 3, 4, 5, 678000),
					),
			(
					"2025-01-02T03:04:05.678901",
					datetime(2025, 1, 2, 3, 4, 5, 678901),
					),
			(
					"2025-01-02T03:04:05,678901",
					datetime(2025, 1, 2, 3, 4, 5, 678901),
					),
			(
					"2025-01-02T030405.678901",
					datetime(2025, 1, 2, 3, 4, 5, 678901),
					),
			(
					"2025-01-02T030405,678901",
					datetime(2025, 1, 2, 3, 4, 5, 678901),
					),
			(
					"2025-01-02T03:04:05.6789010",
					datetime(2025, 1, 2, 3, 4, 5, 678901),
					),
			(
					"2009-04-19T03:15:45.2345",
					datetime(2009, 4, 19, 3, 15, 45, 234500),
					),
			(
					"2009-04-19T03:15:45.1234567",
					datetime(2009, 4, 19, 3, 15, 45, 123456),
					),
			(
					"2025-01-02T03:04:05,678",
					datetime(2025, 1, 2, 3, 4, 5, 678000),
					),
			("20250102", datetime(2025, 1, 2, 0, 0)),
			("20250102T03", datetime(2025, 1, 2, 3, 0)),
			("20250102T03:04", datetime(2025, 1, 2, 3, 4)),
			("20250102T03:04:05", datetime(2025, 1, 2, 3, 4, 5)),
			("20250102T030405", datetime(2025, 1, 2, 3, 4, 5)),
			(
					"20250102T03:04:05.6",
					datetime(2025, 1, 2, 3, 4, 5, 600000),
					),
			(
					"20250102T03:04:05,6",
					datetime(2025, 1, 2, 3, 4, 5, 600000),
					),
			(
					"20250102T03:04:05.678",
					datetime(2025, 1, 2, 3, 4, 5, 678000),
					),
			(
					"20250102T03:04:05,678",
					datetime(2025, 1, 2, 3, 4, 5, 678000),
					),
			(
					"20250102T03:04:05.678901",
					datetime(2025, 1, 2, 3, 4, 5, 678901),
					),
			(
					"20250102T030405.678901",
					datetime(2025, 1, 2, 3, 4, 5, 678901),
					),
			(
					"20250102T030405,678901",
					datetime(2025, 1, 2, 3, 4, 5, 678901),
					),
			(
					"20250102T030405.6789010",
					datetime(2025, 1, 2, 3, 4, 5, 678901),
					),
			("2022W01", datetime(2022, 1, 3)),
			("2022W52520", datetime(2022, 12, 26, 20, 0)),
			("2022W527520", datetime(2023, 1, 1, 20, 0)),
			("2026W01516", datetime(2025, 12, 29, 16, 0)),
			("2026W013516", datetime(2025, 12, 31, 16, 0)),
			("2025W01503", datetime(2024, 12, 30, 3, 0)),
			("2025W014503", datetime(2025, 1, 2, 3, 0)),
			("2025W01512", datetime(2024, 12, 30, 12, 0)),
			("2025W014512", datetime(2025, 1, 2, 12, 0)),
			("2025W014T121431", datetime(2025, 1, 2, 12, 14, 31)),
			("2026W013T162100", datetime(2025, 12, 31, 16, 21)),
			("2026W013 162100", datetime(2025, 12, 31, 16, 21)),
			("2022W527T202159", datetime(2023, 1, 1, 20, 21, 59)),
			("2022W527 202159", datetime(2023, 1, 1, 20, 21, 59)),
			("2025W014 121431", datetime(2025, 1, 2, 12, 14, 31)),
			("2025W014T030405", datetime(2025, 1, 2, 3, 4, 5)),
			("2025W014 030405", datetime(2025, 1, 2, 3, 4, 5)),
			("2020-W53-6T03:04:05", datetime(2021, 1, 2, 3, 4, 5)),
			("2020W537 03:04:05", datetime(2021, 1, 3, 3, 4, 5)),
			("2025-W01-4T03:04:05", datetime(2025, 1, 2, 3, 4, 5)),
			(
					"2025-W01-4T03:04:05.678901",
					datetime(2025, 1, 2, 3, 4, 5, 678901),
					),
			("2025-W01-4T12:14:31", datetime(2025, 1, 2, 12, 14, 31)),
			(
					"2025-W01-4T12:14:31.012345",
					datetime(2025, 1, 2, 12, 14, 31, 12345),
					),
			("2026-W01-3T16:21:00", datetime(2025, 12, 31, 16, 21)),
			("2026-W01-3T16:21:00.000000", datetime(2025, 12, 31, 16, 21)),
			(
					"2022-W52-7T20:21:59",
					datetime(2023, 1, 1, 20, 21, 59),
					),
			(
					"2022-W52-7T20:21:59.999999",
					datetime(2023, 1, 1, 20, 21, 59, 999999),
					),
			(
					"2025-W01003+00",
					datetime(2024, 12, 30, 3, 0, tzinfo=UTC),
					),
			(
					"2025-01-02T03:04:05+00",
					datetime(2025, 1, 2, 3, 4, 5, tzinfo=UTC),
					),
			(
					"2025-01-02T03:04:05Z",
					datetime(2025, 1, 2, 3, 4, 5, tzinfo=UTC),
					),
			(
					"2025-01-02003:04:05,6+00:00:00.00",
					datetime(2025, 1, 2, 3, 4, 5, 600000, tzinfo=UTC),
					),
			(
					"2000-01-01T00+21",
					datetime(2000, 1, 1, 0, 0, tzinfo=timezone(timedelta(hours=21))),
					),
			(
					"2025-01-02T03:05:06+0300",
					datetime(
							2025,
							1,
							2,
							3,
							5,
							6,
							tzinfo=timezone(timedelta(hours=3)),
							),
					),
			(
					"2025-01-02T03:05:06-0300",
					datetime(
							2025,
							1,
							2,
							3,
							5,
							6,
							tzinfo=timezone(timedelta(hours=-3)),
							),
					),
			(
					"2025-01-02T03:04:05+0000",
					datetime(2025, 1, 2, 3, 4, 5, tzinfo=UTC),
					),
			(
					"2025-01-02T03:05:06+03",
					datetime(
							2025,
							1,
							2,
							3,
							5,
							6,
							tzinfo=timezone(timedelta(hours=3)),
							),
					),
			(
					"2025-01-02T03:05:06-03",
					datetime(
							2025,
							1,
							2,
							3,
							5,
							6,
							tzinfo=timezone(timedelta(hours=-3)),
							),
					),
			(
					"2020-01-01T03:05:07.123457-05:00",
					datetime(2020, 1, 1, 3, 5, 7, 123457, tzinfo=EST),
					),
			(
					"2020-01-01T03:05:07.123457-0500",
					datetime(2020, 1, 1, 3, 5, 7, 123457, tzinfo=EST),
					),
			(
					"2020-06-01T04:05:06.111111-04:00",
					datetime(2020, 6, 1, 4, 5, 6, 111111, tzinfo=EDT),
					),
			(
					"2020-06-01T04:05:06.111111-0400",
					datetime(2020, 6, 1, 4, 5, 6, 111111, tzinfo=EDT),
					),
			(
					"2021-10-31T01:30:00.000000+01:00",
					datetime(2021, 10, 31, 1, 30, tzinfo=BST),
					),
			(
					"2021-10-31T01:30:00.000000+0100",
					datetime(2021, 10, 31, 1, 30, tzinfo=BST),
					),
			(
					"2025-01-02T03:04:05,6+000000.00",
					datetime(2025, 1, 2, 3, 4, 5, 600000, tzinfo=UTC),
					),
			(
					"2025-01-02T03:04:05,678+00:00:10",
					datetime(
							2025,
							1,
							2,
							3,
							4,
							5,
							678000,
							tzinfo=timezone(timedelta(seconds=10)),
							),
					),
			("2025-01-02T24:00:00", datetime(2025, 1, 3, 0, 0, 0)),
			("2025-01-31T24:00:00", datetime(2025, 2, 1, 0, 0, 0)),
			("2025-12-31T24:00:00", datetime(2026, 1, 1, 0, 0, 0)),
			]

	for input_str, expected in examples:
		actual = dates.datetime_from_isoformat(input_str)
		assert actual == expected


def test_datetime_from_isoformat_fails_datetime():
	# Test that fromisoformat() fails on invalid values
	bad_strs = [
			'',  # Empty string
			'\ud800',  # bpo-34454: Surrogate code point
			"2009.04-19T03",  # Wrong first separator
			"2009-04.19T03",  # Wrong second separator
			"2009-04-19T0a",  # Invalid hours
			"2009-04-19T03:1a:45",  # Invalid minutes
			"2009-04-19T03:15:4a",  # Invalid seconds
			"2009-04-19T03;15:45",  # Bad first time separator
			"2009-04-19T03:15;45",  # Bad second time separator
			"2009-04-19T03:15:4500:00",  # Bad time zone separator
			"2009-04-19T03:15:45.123456+24:30",  # Invalid time zone offset
			"2009-04-19T03:15:45.123456-24:30",  # Invalid negative offset
			"2009-04-10ᛇᛇᛇᛇᛇ12:15",  # Unicode chars
			"2009-04\ud80010T12:15",  # Surrogate char in date
			"2009-04-10T12\ud80015",  # Surrogate char in time
			"2009-04-19T1",  # Incomplete hours
			"2009-04-19T12:3",  # Incomplete minutes
			"2009-04-19T12:30:4",  # Incomplete seconds
			"2009-04-19T12:",  # Ends with time separator
			"2009-04-19T12:30:",  # Ends with time separator
			"2009-04-19T12:30:45.",  # Ends with time separator
			"2009-04-19T12:30:45.123456+",  # Ends with timezone separator
			"2009-04-19T12:30:45.123456-",  # Ends with timezone separator
			"2009-04-19T12:30:45.123456-05:00a",  # Extra text
			"2009-04-19T12:30:45.123-05:00a",  # Extra text
			"2009-04-19T12:30:45-05:00a",  # Extra text
			"2009-04-19T24:00:00.000001",  # Has non-zero microseconds on 24:00
			"2009-04-19T24:00:01.000000",  # Has non-zero seconds on 24:00
			"2009-04-19T24:01:00.000000",  # Has non-zero minutes on 24:00
			"2009-04-32T24:00:00.000000",  # Day is invalid before wrapping due to 24:00
			"2009-13-01T24:00:00.000000",  # Month is invalid before wrapping due to 24:00
			"9999-12-31T24:00:00.000000",  # Year is invalid after wrapping due to 24:00
			"2009-04-19T12:30Z12:00",  # Extra time zone info after Z
			"2009-04-19T12:30:45:334034",  # Invalid microsecond separator
			"2009-04-19T12:30:45.400 +02:30",  # Space between ms and timezone (gh-130959)
			"2009-04-19T12:30:45.400 ",  # Trailing space (gh-130959)
			"2009-04-19T12:30:45. 400",  # Space before fraction (gh-130959)
			"2009-04-19T12:30:45+00:90:00",  # Time zone field out from range
			"2009-04-19T12:30:45+00:00:90",  # Time zone field out from range
			"2009-04-19T12:30:45-00:90:00",  # Time zone field out from range
			"2009-04-19T12:30:45-00:00:90",  # Time zone field out from range
			"2020-2020",  # Ambiguous 9-char date portion
			# gh-152204: each time field must be exactly N ASCII digits
			"2020-12-12T0٥:02:03",  # Unicode digit in the hour
			"2020-12-12T01:0٥:03",  # Unicode digit in the minute
			"2020-12-12T01:02:0٥",  # Unicode digit in the second
			"2020-12-12T01:02:03.٥",  # Unicode digit in the fraction
			"2020-12-12T01:02:03.4_6",  # underscore in the fraction
			"2020-12-12T01:02:03+0٥:00",  # Unicode digit in the tz hour
			"2020-12-12T01:02:03+01:0٥",  # Unicode digit in the tz minute
			"20201212T0102٣٤",  # Unicode digits in the basic-format time
			"2009-04-19T12:30:45.+05:00",  # Empty fraction before offset
			"2009-04-19T12:30:45.-05:00",  # Empty fraction before offset
			"2009-04-19T12:30:45.Z",  # Empty fraction before Z
			"2009-04-19T12:30:45,+05:00",  # Empty fraction (comma) before offset
			]

	for bad_str in bad_strs:
		with pytest.raises(ValueError):  # noqa: PT011
			dates.datetime_from_isoformat(bad_str)


def test_datetime_from_isoformat_fails_datetime_valueerror():
	pattern = r"(year|month|day|hour|minute|second) (must be in \d+\.\.\d+|\d+ is out of range)"
	bad_strs = [
			"2009-04-01T12:30:90",  # Second out of range
			"2009-04-01T12:90:45",  # Minute out of range
			"2009-04-01T25:30:45",  # Hour out of range
			"2009-00-01T24:00:00",  # Month below range
			"2009-13-01T24:00:00",  # Month out of range
			"9999-12-31T24:00:00",  # Year out of range
			]

	for bad_str in bad_strs:
		with pytest.raises(ValueError, match=pattern):
			dates.datetime_from_isoformat(bad_str)

	# days out of range have their own error message, see issue 70647
	with pytest.raises(ValueError, match="^day is out of range for month"):
		dates.datetime_from_isoformat("2009-04-32T24:00:00")


def test_datetime_from_isoformat_fails_surrogate():
	# Test that when fromisoformat() fails with a surrogate character as
	# the separator, the error message contains the original string
	dtstr = "2018-01-03\ud80001:0113"

	with pytest.raises(ValueError, match=re.escape(repr(dtstr))):
		dates.datetime_from_isoformat(dtstr)


def test_datetime_from_isoformat_utc():
	dt_str = "2014-04-19T13:21:13+00:00"
	dt = dates.datetime_from_isoformat(dt_str)

	assert dt.tzinfo is timezone.utc


def test_datetime_from_isoformat_utc_subsecond_offset():
	# A UTC offset whose whole-second part is zero but with a non-zero
	# microsecond part must be preserved, not collapsed to UTC.
	for us in (1, -1, 999999, -999999):
		tz = timezone(timedelta(microseconds=us))
		dt = datetime(2020, 6, 15, 12, 34, 56, tzinfo=tz)
		rt = dates.datetime_from_isoformat(dt.isoformat())
		assert rt.utcoffset() == timedelta(microseconds=us)
		assert rt == dt
		assert rt.tzinfo is not timezone.utc

	tz = timezone(timedelta(
			hours=5,
			minutes=30,
			seconds=15,
			microseconds=123456,
			))
	dt = datetime(2020, 6, 15, 12, 34, 56, tzinfo=tz)
	rt = dates.datetime_from_isoformat(dt.isoformat())
	assert rt.utcoffset() == tz.utcoffset(None)
	assert rt == dt

	for tstr in (
			"2020-06-15T12:34:56+00:00",
			"2020-06-15T12:34:56+00:00:00.000000",
			"2020-06-15T12:34:56Z",
			):
		assert dates.datetime_from_isoformat(tstr).tzinfo is timezone.utc
