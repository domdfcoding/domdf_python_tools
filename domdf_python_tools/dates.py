#  !/usr/bin/env python
#   -*- coding: utf-8 -*-
#
#  dates.py
"""
Utilities for working with dates and times
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Parts of the docstrings based on the Python 3.8.2 Documentation
#  Licensed under the Python Software Foundation License Version 2.
#  Copyright © 2001-2020 Python Software Foundation. All rights reserved.
#  Copyright © 2000 BeOpen.com . All rights reserved.
#  Copyright © 1995-2000 Corporation for National Research Initiatives . All rights reserved.
#  Copyright © 1991-1995 Stichting Mathematisch Centrum . All rights reserved.
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

# stdlib
import datetime
from collections import OrderedDict
from typing import Optional, Union

try:
	import pytz

	def get_utc_offset(tz, date: datetime.datetime = None) -> Optional[datetime.timedelta]:
		"""
		Returns the offset between UTC and the requested timezone on the given date.
		If ``date`` is ``None`` then the current date is used.

		:param tz: ``pytz.timezone`` or a string representing the timezone
		:type tz:
		:param date: The date to obtain the UTC offset for
		:type date: python:datetime.datetime, optional

		:return:
		:rtype: datetime.timedelta or None
		"""

		if date is None:
			date = datetime.datetime.utcnow()

		if isinstance(tz, str):
			tz = get_timezone(tz, date)

		return date.replace(tzinfo=pytz.utc).astimezone(tz).utcoffset()

	def get_timezone(tz: str, date: datetime.datetime = None) -> Optional[datetime.tzinfo]:
		"""
		Returns a localized :class:`pytz.timezone` object for the given date.
		If ``date`` is ``None`` then the current date is used.

		:param tz: A string representing a pytz timezone
		:type tz: str
		:param date: The date to obtain the timezone for
		:type date: datetime.datetime, optional

		:return:
		:rtype: datetime.tzinfo or None
		"""

		if date is None:
			date = datetime.datetime.utcnow()

		d = date.replace(tzinfo=None)

		return pytz.timezone(tz).localize(d).tzinfo

	def current_tzinfo():
		"""
		Returns a tzinfo object for the current timezone

		:rtype: :class:`python:datetime.tzinfo`
		"""

		return datetime.datetime.now().astimezone().tzinfo

	#
	# def datetime_to_utc_timestamp(datetime, current_tzinfo=None):
	# 	"""
	# 	Convert a :class:`datetime.datetime` object to seconds since UNIX epoch, in UTC time
	#
	# 	:param datetime:
	# 	:type datetime: :class:`datetime.datetime`
	# 	:param current_tzinfo: A tzinfo object representing the current timezone.
	# 		If None it will be inferred.
	# 	:type current_tzinfo: :class:`~python:datetime.tzinfo`
	#
	# 	:return: Timestamp in UTC timezone
	# 	:rtype: float
	# 	"""
	#
	# 	return datetime.astimezone(current_tzinfo).timestamp()
	#

	def set_timezone(obj, tzinfo):
		"""
		Sets the timezone / tzinfo of the given :class:`datetime.datetime` object.
		This will not convert the time (i.e. the hours will stay the same).
		Use :meth:`python:datetime.datetime.astimezone` to accomplish that.

		:param obj:
		:type obj:
		:param tzinfo:
		:type tzinfo:

		:return:
		:rtype:
		"""

		return obj.replace(tzinfo=tzinfo)

	def utc_timestamp_to_datetime(
			utc_timestamp: Union[float, int], output_tz: datetime.tzinfo = None
			) -> datetime.datetime:
		"""
		Convert UTC timestamp (seconds from UNIX epoch) to a :class:`datetime.datetime` object

		If ``output_tz`` is None the timestamp is converted to the platform’s local date and time,
		and the local timezone is inferred and set for the object.

		If ``output_tz`` is not None, it must be an instance of a :class:`~python:datetime.tzinfo` subclass,
		and the timestamp is converted to ``output_tz``’s time zone.


		:param utc_timestamp: The timestamp to convert to a datetime object
		:type utc_timestamp: float, int
		:param output_tz: The timezone to output the datetime object for.
			If None it will be inferred.
		:type output_tz: datetime.tzinfo

		:return: The timestamp as a datetime object.
		:rtype: datetime.datetime

		:raises: :class:`~python:OverflowError` if the timestamp is out of the range
			of values supported by the platform C localtime() or gmtime() functions,
			and OSError on localtime() or gmtime() failure. It’s common for this to
			be restricted to years in 1970 through 2038.
		"""

		new_datetime = datetime.datetime.fromtimestamp(utc_timestamp, output_tz)
		return new_datetime.astimezone(output_tz)

	# List of months and their 3-character shortcodes.
	months = OrderedDict(
			Jan="January",
			Feb="February",
			Mar="March",
			Apr="April",
			May="May",
			Jun="June",
			Jul="July",
			Aug="August",
			Sep="September",
			Oct="October",
			Nov="November",
			Dec="December",
			)

	def parse_month(month: Union[str, int]) -> str:
		"""
		Converts an integer or shorthand month into the full month name

		:param month: The month number or shorthand name
		:type month: str or int

		:return: The full name of the month
		:rtype: str
		"""

		try:
			month = int(month)
		except ValueError:
			try:
				return months[month.capitalize()[:3]]  # type: ignore
			except KeyError:
				raise ValueError("Unrecognised month value")

		# Only get here if first try succeeded
		if 0 < month <= 12:
			return list(months.values())[month - 1]
		else:
			raise ValueError("Unrecognised month value")

	def get_month_number(month: Union[str, int]) -> int:
		"""
		Returns the number of the given month. If ``month`` is already a
		number between 1 and 12 it will be returned immediately.

		:param month: The month to convert to a number
		:type month: str or int

		:return: The number of the month
		:rtype: int
		"""

		if isinstance(month, int):
			if 0 < month <= 12:
				return month
			else:
				raise ValueError("The given month is not recognised.")
		else:
			month = parse_month(month)
			return list(months.values()).index(month) + 1

	def check_date(month: Union[str, int], day: int, leap_year: bool = True) -> bool:
		"""
		Returns ``True`` if the day number is valid for the given month.
		Note that this will return ``True`` for the 29th Feb. If you don't
		want this behaviour set ``leap_year`` to ``False``.

		:param month: The month to test
		:type month: str, int
		:param day: The day number to test
		:type day: int
		:param leap_year: Whether to return ``True`` for 29th Feb. Default ``True``
		:type leap_year: bool, optional

		:return: ``True`` if the date is valid
		:rtype: bool
		"""

		# Ensure day is an integer
		day = int(day)
		month = get_month_number(month)
		year = 2020 if leap_year else 2019

		try:
			datetime.date(year, month, day)
			return True
		except ValueError:
			return False

except ImportError:
	import warnings
	warnings.warn(
			"'domdf_python_tools.dates' requires pytz (https://pypi.org/project/pytz/), but it is not installed."
			)
