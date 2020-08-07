"""
test_dates
~~~~~~~~~~~~~~~

Test functions in dates.py

"""

# stdlib
import datetime

# 3rd party
import pytest
import pytz

# this package
from domdf_python_tools import dates

test_date = datetime.datetime(1996, 10, 13, 2, 20).replace(tzinfo=pytz.utc)
today = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)  # make sure UTC

# TODO: travis matrix to test without pytz installed
# TODO: test get_timezone


def test_utc_offset():
	# Check that the correct UTC offsets are given for common timezones
	assert dates.get_utc_offset("US/Pacific", test_date) == datetime.timedelta(-1, 61200)
	assert dates.get_utc_offset("Europe/London", test_date) == datetime.timedelta(0, 3600)
	assert dates.get_utc_offset("Africa/Algiers", test_date) == datetime.timedelta(0, 3600)
	# TODO: Finish

	# Check that the correct UTC offsets are given for common timezones for today
	assert dates.get_utc_offset("US/Pacific", today) == datetime.timedelta(-1, 61200)
	assert dates.get_utc_offset("Europe/London", today) == datetime.timedelta(0, 3600)
	assert dates.get_utc_offset("Africa/Algiers", today) == datetime.timedelta(0, 3600)

	# Check that the correct UTC offsets are given for common timezones when ``date`` is not given
	assert dates.get_utc_offset("US/Pacific") == datetime.timedelta(-1, 61200)
	assert dates.get_utc_offset("Europe/London") == datetime.timedelta(0, 3600)
	assert dates.get_utc_offset("Africa/Algiers") == datetime.timedelta(0, 3600)


# TODO: Finish


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


months = [
		"January",
		"February",
		"March",
		"April",
		"May",
		"June",
		"July",
		"August",
		"September",
		"October",
		"November",
		"December",
		]


def test_parse_month():
	for month_idx, month in enumerate(months):

		month_idx += 1  # to make 1-indexed

		for i in range(3, len(month)):
			assert dates.parse_month(month.lower()[:i]) == month
			assert dates.parse_month(month.upper()[:i]) == month
			assert dates.parse_month(month.capitalize()[:i]) == month

		assert dates.parse_month(month_idx) == month

	for value in ["abc", 0, '0', -1, "-1", 13, "13"]:
		with pytest.raises(ValueError, match="Unrecognised month value"):
			dates.parse_month(value)  # type: ignore


@pytest.mark.parametrize("month_idx, month", enumerate(months))
def test_get_month_number_from_name(month_idx, month):
	month_idx += 1  # to make 1-indexed

	for i in range(3, len(month)):
		assert dates.get_month_number(month.lower()[:i]) == month_idx
		assert dates.get_month_number(month.upper()[:i]) == month_idx
		assert dates.get_month_number(month.capitalize()[:i]) == month_idx

	assert dates.get_month_number(month) == month_idx


@pytest.mark.parametrize("month_idx", range(1, 13))
def test_get_month_number_from_no(month_idx):
	for month_idx in range(1, 13):
		assert dates.get_month_number(month_idx) == month_idx


@pytest.mark.parametrize(
		"value, match",
		[
				(0, "The given month is not recognised."),
				(-1, "The given month is not recognised."),
				(13, "The given month is not recognised."),
				("abc", "Unrecognised month value"),
				('0', "Unrecognised month value"),
				("-1", "Unrecognised month value"),
				("13", "Unrecognised month value"),
				]
		)
def test_get_month_number_errors(value, match):
	with pytest.raises(ValueError, match=match):
		dates.get_month_number(value)


def test_check_date():
	for month_idx, month in enumerate(months):

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
