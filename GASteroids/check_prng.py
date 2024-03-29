#!/usr/bin/env python3

"""Integer maths PRNG test.

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

seed = 931

M = 32749
A = 219
Q = M // A
R = M % A

def randInt ():
    global seed

    x_new = (A * (seed % Q)) - (R * (seed // Q))

    if x_new > 0:
        seed = x_new
    else:
        seed = x_new + M

    return seed;

def myrand (randMax):
    randMax += 1
    return ((randInt() - 1) // (M // randMax))

def main ():
    for i in range(0, 500):
        #print(myrand(32000))
        #print(randInt())
        print(myrand(1))

if __name__ == "__main__":
    main()
