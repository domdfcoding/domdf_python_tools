#  Backported from https://github.com/python/cpython/blob/master/Lib/_pydatetime.py
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2026 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com. All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives. All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum. All rights reserved.

# stdlib
from datetime import date, datetime, time, timedelta, timezone
from operator import index as _index
from typing import List, Optional, Tuple

# this package
from domdf_python_tools.words import removeprefix

__all__ = ["date_from_isoformat", "datetime_from_isoformat", "time_from_isoformat"]

MINYEAR = 1
MAXYEAR = 9999

# Utility functions, adapted from Python's Demo/classes/Dates.py, which
# also assumes the current Gregorian calendar indefinitely extended in
# both directions.  Difference:  Dates.py calls January 1 of year 0 day
# number 1.  The code here calls January 1 of year 1 day number 1.  This is
# to match the definition of the "proleptic Gregorian" calendar in Dershowitz
# and Reingold's "Calendrical Calculations", where it's the base calendar
# for all computations.  See the book for algorithms for converting between
# proleptic Gregorian ordinals and many other calendar systems.

# -1 is a placeholder for indexing purposes.
_DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

_DAYS_BEFORE_MONTH = [-1]  # -1 is a placeholder for indexing purposes.
dbm = 0
for dim in _DAYS_IN_MONTH[1:]:
	_DAYS_BEFORE_MONTH.append(dbm)
	dbm += dim
del dbm, dim


def _is_leap(year: int) -> bool:
	# year -> 1 if leap year, else 0.
	return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_before_year(year: int) -> int:
	# year -> number of days before January 1st of year.
	y = year - 1
	return y * 365 + y // 4 - y // 100 + y // 400


def _days_in_month(year: int, month: int) -> int:
	# year, month -> number of days in that month in that year.
	assert 1 <= month <= 12, f"month must be in 1..12, not {month}"
	if month == 2 and _is_leap(year):
		return 29
	return _DAYS_IN_MONTH[month]


def _days_before_month(year: int, month: int) -> int:
	# year, month -> number of days in year preceding first day of month.
	assert 1 <= month <= 12, f"month must be in 1..12, not {month}"
	return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))


def _ymd2ord(year: int, month: int, day: int) -> int:
	# year, month, day -> ordinal, considering 01-Jan-0001 as day 1.
	assert 1 <= month <= 12, f"month must be in 1..12, not {month}"
	dim = _days_in_month(year, month)
	assert 1 <= day <= dim, f"day must be in 1..{dim}, not {day}"
	return (_days_before_year(year) + _days_before_month(year, month) + day)


_DI400Y = _days_before_year(401)  # number of days in 400 years
_DI100Y = _days_before_year(101)  # number of days in 100 years
_DI4Y = _days_before_year(5)  # number of days in 4 years

# A 4-year cycle has an extra leap day over what we'd get from pasting
# together 4 single years.
assert _DI4Y == 4 * 365 + 1

# Similarly, a 400-year cycle has an extra leap day over what we'd get from
# pasting together 4 100-year cycles.
assert _DI400Y == 4 * _DI100Y + 1

# OTOH, a 100-year cycle has one fewer leap day than we'd get from
# pasting together 25 4-year cycles.
assert _DI100Y == 25 * _DI4Y - 1


def _ord2ymd(n: int) -> Tuple[int, int, int]:
	# "ordinal -> (year, month, day), considering 01-Jan-0001 as day 1.

	# n is a 1-based index, starting at 1-Jan-1.  The pattern of leap years
	# repeats exactly every 400 years.  The basic strategy is to find the
	# closest 400-year boundary at or before n, then work with the offset
	# from that boundary to n.  Life is much clearer if we subtract 1 from
	# n first -- then the values of n at 400-year boundaries are exactly
	# those divisible by _DI400Y:
	#
	#     D  M   Y            n              n-1
	#     -- --- ----        ----------     ----------------
	#     31 Dec -400        -_DI400Y       -_DI400Y -1
	#      1 Jan -399         -_DI400Y +1   -_DI400Y      400-year boundary
	#     ...
	#     30 Dec  000        -1             -2
	#     31 Dec  000         0             -1
	#      1 Jan  001         1              0            400-year boundary
	#      2 Jan  001         2              1
	#      3 Jan  001         3              2
	#     ...
	#     31 Dec  400         _DI400Y        _DI400Y -1
	#      1 Jan  401         _DI400Y +1     _DI400Y      400-year boundary
	n -= 1
	n400, n = divmod(n, _DI400Y)
	year = n400 * 400 + 1  # ..., -399, 1, 401, ...

	# Now n is the (non-negative) offset, in days, from January 1 of year, to
	# the desired date.  Now compute how many 100-year cycles precede n.
	# Note that it's possible for n100 to equal 4!  In that case 4 full
	# 100-year cycles precede the desired day, which implies the desired
	# day is December 31 at the end of a 400-year cycle.
	n100, n = divmod(n, _DI100Y)

	# Now compute how many 4-year cycles precede it.
	n4, n = divmod(n, _DI4Y)

	# And now how many single years.  Again n1 can be 4, and again meaning
	# that the desired day is December 31 at the end of the 4-year cycle.
	n1, n = divmod(n, 365)

	year += n100 * 100 + n4 * 4 + n1
	if n1 == 4 or n100 == 4:
		assert n == 0
		return year - 1, 12, 31

	# Now the year is correct, and n is the offset from January 1.  We find
	# the month via an estimate that's either exact or one too large.
	leapyear = n1 == 3 and (n4 != 24 or n100 == 3)
	assert leapyear == _is_leap(year)
	month = (n + 50) >> 5
	preceding = _DAYS_BEFORE_MONTH[month] + (month > 2 and leapyear)
	if preceding > n:  # estimate is too large
		month -= 1
		preceding -= _DAYS_IN_MONTH[month] + (month == 2 and leapyear)
	n -= preceding
	assert 0 <= n < _days_in_month(year, month)

	# Now the year and month are correct, and n is the offset from the
	# start of that month:  we're done!
	return year, month, n + 1


# Helpers for parsing the result of isoformat()
def _is_ascii_digit(c: str) -> bool:
	return c in "0123456789"


def _find_isoformat_datetime_separator(dtstr: str) -> int:
	# See the comment in _datetimemodule.c:_find_isoformat_datetime_separator
	len_dtstr = len(dtstr)
	if len_dtstr == 7:
		return 7

	assert len_dtstr > 7
	date_separator = '-'
	week_indicator = 'W'

	if dtstr[4] == date_separator:
		if dtstr[5] == week_indicator:
			if len_dtstr < 8:
				raise ValueError("Invalid ISO string")
			if len_dtstr > 8 and dtstr[8] == date_separator:
				if len_dtstr == 9:
					raise ValueError("Invalid ISO string")
				if len_dtstr > 10 and _is_ascii_digit(dtstr[10]):
					# This is as far as we need to resolve the ambiguity for
					# the moment - if we have YYYY-Www-##, the separator is
					# either a hyphen at 8 or a number at 10.
					#
					# We'll assume it's a hyphen at 8 because it's way more
					# likely that someone will use a hyphen as a separator than
					# a number, but at this point it's really best effort
					# because this is an extension of the spec anyway.
					# TODO(pganssle): Document this
					return 8
				return 10
			else:
				# YYYY-Www (8)
				return 8
		else:
			# YYYY-MM-DD (10)
			return 10
	else:
		if dtstr[4] == week_indicator:
			# YYYYWww (7) or YYYYWwwd (8)
			idx = 7
			while idx < len_dtstr:
				if not _is_ascii_digit(dtstr[idx]):
					break
				idx += 1

			if idx < 9:
				return idx

			if idx % 2 == 0:
				# If the index of the last number is even, it's YYYYWwwd
				return 7
			else:
				return 8
		else:
			# YYYYMMDD (8)
			return 8


def _read_isoformat_component(s: str, n: int) -> int:
	# The caller has verified the string is ASCII, so isdigit() matches only
	# the ASCII digits accepted by the C parser.
	if len(s) != n or not s.isdigit():
		raise ValueError("Invalid isoformat string")
	return int(s)


def _parse_isoformat_date(dtstr: str) -> Tuple[int, int, int]:
	# It is assumed that this is an ASCII-only string of lengths 7, 8 or 10,
	# see the comment on Modules/_datetimemodule.c:_find_isoformat_datetime_separator
	if len(dtstr) not in (7, 8, 10):
		raise ValueError("Invalid isoformat string")
	if not dtstr.isascii():
		raise ValueError("Invalid isoformat string")

	year = _read_isoformat_component(dtstr[0:4], 4)
	has_sep = dtstr[4] == '-'

	pos = 4 + has_sep
	if dtstr[pos:pos + 1] == 'W':
		# YYYY-?Www-?D?
		pos += 1
		weekno = _read_isoformat_component(dtstr[pos:pos + 2], 2)
		pos += 2

		dayno = 1
		if len(dtstr) > pos:
			if (dtstr[pos:pos + 1] == '-') != has_sep:
				raise ValueError("Inconsistent use of dash separator")

			pos += has_sep

			dayno = _read_isoformat_component(dtstr[pos:pos + 1], 1)

		return _isoweek_to_gregorian(year, weekno, dayno)
	else:
		month = _read_isoformat_component(dtstr[pos:pos + 2], 2)
		pos += 2
		if (dtstr[pos:pos + 1] == '-') != has_sep:
			raise ValueError("Inconsistent use of dash separator")

		pos += has_sep
		day = _read_isoformat_component(dtstr[pos:pos + 2], 2)

		return year, month, day


_FRACTION_CORRECTION = [100000, 10000, 1000, 100, 10]


def _parse_hh_mm_ss_ff(tstr: str) -> List[int]:
	# Parses things of the form HH[:?MM[:?SS[{.,}fff[fff]]]]
	len_str = len(tstr)

	time_comps = [0, 0, 0, 0]
	pos = 0
	for comp in range(0, 3):
		time_comps[comp] = _read_isoformat_component(tstr[pos:pos + 2], 2)

		pos += 2
		next_char = tstr[pos:pos + 1]

		if comp == 0:
			has_sep = next_char == ':'

		if not next_char or comp >= 2:
			break

		if has_sep and next_char != ':':
			raise ValueError("Invalid time separator: %c" % next_char)

		pos += has_sep

	if pos < len_str:
		if tstr[pos] not in ".,":
			raise ValueError("Invalid microsecond separator")
		else:
			pos += 1
			if not tstr[pos:].isdigit():
				raise ValueError("Non-digit values in fraction")

			len_remainder = len_str - pos

			if len_remainder >= 6:
				to_parse = 6
			else:
				to_parse = len_remainder

			time_comps[3] = int(tstr[pos:(pos + to_parse)])
			if to_parse < 6:
				time_comps[3] *= _FRACTION_CORRECTION[to_parse - 1]

	return time_comps


def _parse_isoformat_time(
		tstr: str,
		) -> Tuple[Tuple[int, int, int, int, Optional[timezone]], bool, bool, Optional[ValueError]]:
	# Format supported is HH[:MM[:SS[.fff[fff]]]][+HH:MM[:SS[.ffffff]]]
	len_str = len(tstr)
	if len_str < 2:
		raise ValueError("Isoformat time too short")
	if not tstr.isascii():
		raise ValueError("Invalid isoformat string")

	# This is equivalent to re.search('[+-Z]', tstr), but faster
	tz_pos = (tstr.find('-') + 1 or tstr.find('+') + 1 or tstr.find('Z') + 1)
	timestr = tstr[:tz_pos - 1] if tz_pos > 0 else tstr

	_time_comps = _parse_hh_mm_ss_ff(timestr)

	hour, minute, second, microsecond = _time_comps
	became_next_day = False
	error_from_components = False
	error_from_tz = None
	if (hour == 24):
		if all(time_comp == 0 for time_comp in _time_comps[1:]):
			hour = 0
			became_next_day = True
		else:
			error_from_components = True

	tzi = None
	if tz_pos == len_str and tstr[-1] == 'Z':
		tzi = timezone.utc
	elif tz_pos > 0:
		tzstr = tstr[tz_pos:]

		# Valid time zone strings are:
		# HH                  len: 2
		# HHMM                len: 4
		# HH:MM               len: 5
		# HHMMSS              len: 6
		# HHMMSS.f+           len: 7+
		# HH:MM:SS            len: 8
		# HH:MM:SS.f+         len: 10+

		if len(tzstr) in (0, 1, 3) or tstr[tz_pos - 1] == 'Z':
			raise ValueError("Malformed time zone string")

		tz_comps = _parse_hh_mm_ss_ff(tzstr)

		if all(x == 0 for x in tz_comps):
			tzi = timezone.utc
		else:
			tzsign = -1 if tstr[tz_pos - 1] == '-' else 1

			try:
				# This function is intended to validate datetimes, but because
				# we restrict time zones to ±24h, it serves here as well.
				_check_time_fields(
						hour=tz_comps[0],
						minute=tz_comps[1],
						second=tz_comps[2],
						microsecond=tz_comps[3],
						fold=0,
						)
			except ValueError as e:
				error_from_tz = e
			else:
				td = timedelta(
						hours=tz_comps[0],
						minutes=tz_comps[1],
						seconds=tz_comps[2],
						microseconds=tz_comps[3],
						)
				tzi = timezone(tzsign * td)

	time_comps = (hour, minute, second, microsecond, tzi)

	return time_comps, became_next_day, error_from_components, error_from_tz


# tuple[int, int, int] -> tuple[int, int, int] version of date.fromisocalendar
def _isoweek_to_gregorian(year: int, week: int, day: int) -> Tuple[int, int, int]:
	# Year is bounded this way because 9999-12-31 is (9999, 52, 5)
	if not MINYEAR <= year <= MAXYEAR:
		raise ValueError(f"year must be in {MINYEAR}..{MAXYEAR}, not {year}")

	if not 0 < week < 53:
		out_of_range = True

		if week == 53:
			# ISO years have 53 weeks in them on years starting with a
			# Thursday and leap years starting on a Wednesday
			first_weekday = _ymd2ord(year, 1, 1) % 7
			if (first_weekday == 4 or (first_weekday == 3 and _is_leap(year))):
				out_of_range = False

		if out_of_range:
			raise ValueError(f"Invalid week: {week}")

	if not 0 < day < 8:
		raise ValueError(f"Invalid weekday: {day} (range is [1, 7])")

	# Now compute the offset from (Y, 1, 1) in days:
	day_offset = (week - 1) * 7 + (day - 1)

	# Calculate the ordinal day for monday, week 1
	day_1 = _isoweek1monday(year)
	ord_day = day_1 + day_offset

	return _ord2ymd(ord_day)


def _check_time_fields(
		hour: int,
		minute: int,
		second: int,
		microsecond: int,
		fold: int,
		) -> Tuple[int, int, int, int, int]:
	hour = _index(hour)
	minute = _index(minute)
	second = _index(second)
	microsecond = _index(microsecond)
	if not 0 <= hour <= 23:
		raise ValueError(f"hour must be in 0..23, not {hour}")
	if not 0 <= minute <= 59:
		raise ValueError(f"minute must be in 0..59, not {minute}")
	if not 0 <= second <= 59:
		raise ValueError(f"second must be in 0..59, not {second}")
	if not 0 <= microsecond <= 999999:
		raise ValueError(f"microsecond must be in 0..999999, not {microsecond}")
	if fold not in (0, 1):
		raise ValueError(f"fold must be either 0 or 1, not {fold}")
	return hour, minute, second, microsecond, fold


def date_from_isoformat(date_string: str) -> date:
	"""
	Construct a date from a string in ISO 8601 format.

	.. versionadded:: 3.11.0

	:param date_string:
	"""

	if not isinstance(date_string, str):
		raise TypeError("fromisoformat: argument must be a str")

	if not date_string.isascii():
		raise ValueError("Argument must be an ASCII str")

	if len(date_string) not in (7, 8, 10):
		raise ValueError(f'Invalid isoformat string: {date_string!r}')

	try:
		return date(*_parse_isoformat_date(date_string))
	except Exception:
		raise ValueError(f'Invalid isoformat string: {date_string!r}')


def time_from_isoformat(time_string: str) -> time:
	"""
	Construct a time from a string in one of the ISO 8601 formats.

	.. versionadded:: 3.11.0

	:param time_string:
	"""

	if not isinstance(time_string, str):
		raise TypeError("fromisoformat: argument must be a str")

	# The spec actually requires that time-only ISO 8601 strings start with
	# T, but the extended format allows this to be omitted as long as there
	# is no ambiguity with date strings.
	time_string = removeprefix(time_string, 'T')

	try:
		time_components, _, error_from_components, error_from_tz = (_parse_isoformat_time(time_string))
	except ValueError:
		raise ValueError(f'Invalid isoformat string: {time_string!r}') from None
	else:
		if error_from_tz:
			raise error_from_tz
		if error_from_components:
			raise ValueError("Minute, second, and microsecond must be 0 when hour is 24")

		return time(*time_components)


def datetime_from_isoformat(date_string: str) -> datetime:
	"""
	Construct a datetime from a string in one of the ISO 8601 formats.

	.. versionadded:: 3.11.0

	:param date_string:
	"""

	if not isinstance(date_string, str):
		raise TypeError("fromisoformat: argument must be a str")

	if len(date_string) < 7:
		raise ValueError(f'Invalid isoformat string: {date_string!r}')

	# Split this at the separator
	try:
		separator_location = _find_isoformat_datetime_separator(date_string)
		dstr = date_string[0:separator_location]
		tstr = date_string[(separator_location + 1):]

		date_components = _parse_isoformat_date(dstr)
	except ValueError:
		raise ValueError(f'Invalid isoformat string: {date_string!r}') from None

	if tstr:
		try:
			(
					time_components,
					became_next_day,
					error_from_components,
					error_from_tz,
					) = _parse_isoformat_time(tstr)
		except ValueError:
			raise ValueError(f'Invalid isoformat string: {date_string!r}') from None
		else:
			if error_from_tz:
				raise error_from_tz
			if error_from_components:
				raise ValueError("minute, second, and microsecond must be 0 when hour is 24")

			if became_next_day:
				year, month, day = date_components
				# Only wrap day/month when it was previously valid
				if 1 <= month <= 12:
					days_in_month = _days_in_month(year, month)
					if day <= days_in_month:
						# Calculate midnight of the next day
						day += 1
						if day > days_in_month:
							day = 1
							month += 1
							if month > 12:
								month = 1
								year += 1
						date_components = (year, month, day)
	else:
		time_components = (0, 0, 0, 0, None)

	return datetime(*(date_components + time_components))


def _isoweek1monday(year: int) -> int:
	# Helper to calculate the day number of the Monday starting week 1
	THURSDAY = 3
	firstday = _ymd2ord(year, 1, 1)
	firstweekday = (firstday + 6) % 7  # See weekday() above
	week1monday = firstday - firstweekday
	if firstweekday > THURSDAY:
		week1monday += 7
	return week1monday
