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

# 3rd party
try:
	import pytz
	
	def current_tzinfo():
		"""
		Returns a tzinfo object for the current timezone
		
		:rtype: :class:`~python:datetime.tzinfo`
		"""
		
		return datetime.datetime.now().astimezone().tzinfo
	
	
	def datetime_to_utc_timestamp(datetime, current_tzinfo=None):
		"""
		Convert a :class:`datetime.datetime` object to seconds since UNIX epoch, in UTC time
		
		:param datetime:
		:type datetime: :class:`datetime.datetime`
		:param current_tzinfo: A tzinfo object representing the current timezone.
			If None it will be inferred.
		:type current_tzinfo: :class:`~python:datetime.tzinfo`
		
		:return: Timestamp in UTC timezone
		:rtype: float
		"""
		
		return datetime.astimezone(current_tzinfo).replace(tzinfo=pytz.UTC).timestamp()
	
	
	def utc_timestamp_to_datetime(utc_timestamp, output_tz=None):
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
		:type output_tz: :class:`~python:datetime.tzinfo`
		
		:return: The timestamp as a datetime object.
		:rtype: :class:`datetime.datetime`
		
		:raises: :class:`~python:OverflowError` if the timestamp is out of the range
			of values supported by the platform C localtime() or gmtime() functions,
			and OSError on localtime() or gmtime() failure. It’s common for this to
			be restricted to years in 1970 through 2038.
		"""
		
		new_datetime = datetime.datetime.fromtimestamp(utc_timestamp, output_tz)
		
		if output_tz is None:
			return new_datetime.astimezone()
		else:
			return new_datetime

except ImportError:
	import warnings
	warnings.warn("'domdf_python_tools.dates' requires pytz (https://pypi.org/project/pytz/), but it is not installed.")
