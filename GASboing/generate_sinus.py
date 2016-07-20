#!/usr/bin/env python3

"""generate_sinus.py

Generates a sine table for use in Jack. First 90 degrees as integer values
between 0 and 100 inclusive. i.e. 0 to 1 in two decimal place fixed point.

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

# Generate first 90 degrees
table = []
for i in range(0, 91):                                      # 0 to 90 inclusive.
    table.append( round(math.sin(math.radians(i))*100) )

# Pad to the nearest multiple of 8
table.extend([0] * (8-len(table)%8))

# Print sinus table as series of function calls.
print('        let i = 0;');
i = 0
while i < len(table):
    print('        let i = Sinus._push91(i,{0},{1},{2},{3},{4},{5},{6},{7});'.format(
        table[i], table[i+1], table[i+2], table[i+3],
        table[i+4], table[i+5], table[i+6], table[i+7]
        ))
    i = i + 8
