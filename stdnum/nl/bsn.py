# bsn.py - functions for handling BSNs
#
# Copyright (C) 2010, 2011, 2012, 2013 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""BSN (Burgerservicenummer, Dutch national identification number).

The BSN is a number with up to 9 digits (the leading 0's are commonly left
out) which is used as the Dutch national identification number.

>>> validate('1112.22.333')
'111222333'
>>> validate('1112.52.333')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('1112223334')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> format('111222333')
'1112.22.333'
"""

from stdnum.exceptions import *
from stdnum.util import clean


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').strip()
    # pad with leading zeroes
    return (9 - len(number)) * '0' + number


def checksum(number):
    """Calculate the checksum over the number. A valid number should have
    a check digit of 0."""
    return (sum((9 - i) * int(n) for i, n in enumerate(number[:-1])) -
            int(number[-1])) % 11


def validate(number):
    """Checks to see if the number provided is a valid BSN. This checks
    the length and whether the check digit is correct."""
    number = compact(number)
    if not number.isdigit() or int(number) <= 0:
        raise InvalidFormat()
    if len(number) != 9:
        raise InvalidLength()
    if checksum(number) != 0:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid BSN. This checks
    the length and whether the check digit is correct."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    return number[:4] + '.' + number[4:6] + '.' + number[6:]
