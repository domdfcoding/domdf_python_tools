# -*- coding: utf-8 -*-
"""
test_dates
~~~~~~~~~~~~~~~

Test functions in dates.py

"""

# stdlib
import datetime

# 3rd party
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
		assert test_date.astimezone(dates.get_timezone(tz, test_date)).timestamp() == test_date.timestamp() == 845173200.0

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
			assert dates.set_timezone(today, dates.get_timezone(tz, today)).timestamp() != today.timestamp()
			
			# Difference between "today" and the new timezone should be the timezone difference
			assert \
				dates.set_timezone(today, dates.get_timezone(tz, today)).timestamp() +\
				dates.get_utc_offset(tz, today).total_seconds() \
				== today.timestamp()
		
		if tz in {
				"America/Punta_Arenas", "America/Santiago", 'Antarctica/Palmer',
				'Chile/Continental', 'Chile/EasterIsland', 'Pacific/Easter',
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
			assert \
				dates.set_timezone(test_date, dates.get_timezone(tz, test_date)).timestamp() +\
				dates.get_utc_offset(tz, test_date).total_seconds() \
				== test_date.timestamp()
