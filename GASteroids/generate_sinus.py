#!/usr/bin/env python3

"""generate_sinus.py

Generates a sine table as used in GASteroids.

Copyright 2013-2016 Gavin Stewart.

You are required to give attribution to the author (Gavin Stewart) for any
use of this program (GPLv3 Section 7b).

Trying to pass off my code as your own in your Elements of Computing classes
will result in a cursed life of forever buggy software.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import math

for i in range(0, 91):
    out = round(math.sin(math.radians(i))*100)
    print('        let table[', i, '] = ', out, ';', sep='')
