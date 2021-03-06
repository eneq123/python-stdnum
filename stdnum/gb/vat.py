# vat.py - functions for handling United Kingdom VAT numbers
#
# Copyright (C) 2012, 2013 Arthur de Jong
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

"""VAT (United Kingdom (and Isle of Man) VAT registration number).

The VAT number can either be a 9-digit standard number, a 12-digit standard
number followed by a 3-digit branch identifier, a 5-digit number for
government departments (first two digits are GD) or a 5-digit number for
health authorities (first two digits are HA). The 9-digit variants use a
weighted checksum.

>>> validate('GB 980 7806 84')
'980780684'
>>> validate('802311781')  # invalid check digit
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> format('980780684')
'980 7806 84'
"""

from stdnum.util import clean
from stdnum.exceptions import *


def compact(number):
    """Convert the number to the minimal representation. This strips the
    number of any valid separators and removes surrounding whitespace."""
    number = clean(number, ' -.').upper().strip()
    if number.startswith('GB'):
        number = number[2:]
    return number


def checksum(number):
    """Calculate the checksum. The checksum is only used for the 9 digits
    of the number and the result can either be 0 or 42."""
    weights = (8, 7, 6, 5, 4, 3, 2, 10, 1)
    return sum(weights[i] * int(n) for i, n in enumerate(number)) % 97


def validate(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    number = compact(number)
    if len(number) == 5:
        if not number[2:].isdigit():
            raise InvalidFormat()
        if number.startswith('GD') and int(number[2:]) < 500:
            # government department
            pass
        elif number.startswith('HA') and int(number[2:]) >= 500:
            # health authority
            pass
        else:
            raise InvalidComponent()
    elif len(number) in (9, 12):
        if not number.isdigit():
            raise InvalidFormat()
        # standard number: nnn nnnn nn
        # branch trader: nnn nnnn nn nnn (ignore the last thee digits)
        if checksum(number[:9]) not in (0, 42):
            raise InvalidChecksum()
    else:
        raise InvalidLength()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid VAT number. This
    checks the length, formatting and check digit."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False


def format(number):
    """Reformat the passed number to the standard format."""
    number = compact(number)
    if len(number) == 5:
        # government department or health authority
        return number
    if len(number) == 12:
        # includes branch number
        return number[:3] + ' ' + number[3:7] + ' ' + number[7:9] + ' ' + number[9:]
    # standard number: nnn nnnn nn
    return number[:3] + ' ' + number[3:7] + ' ' + number[7:]
