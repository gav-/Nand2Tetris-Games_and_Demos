#!/usr/bin/env python3

"""pgm2jack

Convert a P2 pgm (monochome ascii, a.k.a. "Plain PGM") file to a
jack array (nand2tetris).

Image width must be a multiple of four. Pixels are rendered with a 4x4
dither matrix, so four pixels x4 = 16bit word.

Ideally input is a PGM posterised to 17 shades (equidistant). If not
posterisation will be applied.

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

import sys
import os
import re
import math

class Parser ():
    """P2 PGM parser."""

    def __init__ (self, filename):
        if not os.path.exists(filename):
            sys.exit('Parser Error: Input file not found: %s' % filename)

        # Public properties
        self.width = 0
        self.height = 0
        self.maxColour = 0
        self.currentToken = ''

        # Private properties
        self._fh = open(filename, mode='r')
        self._currentLine = []

        # Initialise from first tokens in file.
        self.hasMoreTokens()
        search = re.search(r'^P2$', self.currentToken)
        if not search: sys.exit('Failed to identify P2 type pgm.')

        self.hasMoreTokens()
        search = re.search(r'^(\d+)$', self.currentToken)
        if not search: sys.exit('Failed to identify X resolution.')
        self.width = int(search.group(1))

        self.hasMoreTokens()
        search = re.search(r'^(\d+)$', self.currentToken)
        if not search: sys.exit('Failed to identify Y resolution.')
        self.height = int(search.group(1))

        if self.width%4 != 0: sys.exit('Width is not a multiple of 4.')

        self.hasMoreTokens()
        search = re.search(r'^(\d+)$', self.currentToken)
        if not search: sys.exit('Failed to identify max colour value.')
        self.maxColour = int(search.group(1))

    def close(self):
        """Close input file"""
        self._fh.close()

    def hasMoreTokens (self) :
        # Find the next token.
        if not len(self._currentLine):
            if not self.hasMoreLines():
                return False

        # Shift next token from line.
        self.currentToken = self._currentLine.pop(0)

        return True

    def hasMoreLines (self) :
        # Find the next non-empty line if one exists.
        line = None
        for line in self._fh:
            line = re.sub(r'#.*$', '', line)        # Remove comments
            line = re.sub(r'^\s+', '', line)        # Remove leading whitespace
            line = re.sub(r'\s+$', '', line)        # Remove trailing whitespace
            if len(line): break                     # Break if line not empty

        if line:
            self._currentLine = line.split()
            return True

        return False

    def buildWord (self) :
        """buildWord - build a 16bit word MSB to LSB, left to right.

        Returns a string of 16 bits.

        """
        word = ''
        word = self._currentBit
        for i in range(1,16):
            if self.hasMoreBits():
                word = self._currentBit + word
            else:
                word = '0' + word

        return word


def formatWord (bits) :
    """Format input bit string as a 16bit 2s complement Jack word.

    Returns formatted string suitable for use as a literal value in Jack.

    """
    val = int(bits, base=2)

    if val > (2**15)-1 :                # Ensure 2s complement 16bit int.
        val = -(2**15 - (val - 2**15))  # e.g.  65528: 1111111111111000
                                        # 32768-(65528-32768) == 8
                                        # which we negate: -8

    if val == -32768:
        # A limitation in the Jack compiler prevents the maximum negative number
        # as a literal, so we have to add an operation to get the value.
        return "-32767-1"
    else:
        return "{0}".format(val)

def remapNM (N, M, array) :
    """Remap range of values in array from a max value of N to M.

    Returns the a remapped array.
    """
    scale = M / N
    newArray = []
    for val in array:
        newArray.append(round(val * scale))

    return newArray

def formatNArgs (N, index, array) :
    """Format N arguments from array, starting at position index.

    If len(array) - index < N, then the result is zero padded out to N
    arguments.

    Returns formatted string suitable as arguments to a Jack function.

    """

    # Determine if we have less than N values remaining, and pad accordingly.
    if (len(array) - index < N):            # Not N values remaining in array.
        data = array[index:]                # Copy last values
        index = 0                           # Index now goes to the start
        data.extend([0] * (N - len(data)))  # Pad out to N values.
    else:
        data = array


    # Convert values to a list of strings.
    args = []
    for i in range(index, index + N):
        args.append('{0}'.format(data[i]))

    # Return a comma delimited list of args.
    return ','.join(args)

### Main ###

if len(sys.argv) < 3:
    sys.exit('Usage: %s <class name> <file.pgm>' % sys.argv[0])

className = sys.argv[1]
infile = sys.argv[2]

filename, ext = os.path.splitext(infile)
if ext != '.pgm':
    sys.exit("Expected file extension .pgm")

outfile = className + '.jack'

outfh = open(outfile, 'w')
parser = Parser(infile)

### Class declaration
classHeader="""/**
 * Static ChunkyImage factory class.
 *
 * Requires ChunkyImage.jack
 *
 * Generated from "{filename}" by pgm2jack.py
 *
 * Copyright 2013 Gavin Stewart.
 */
class {cn} {{

    /**
     * newChunkyImage - returns a ChunkyImage object containing bitmap data.
     */
    function ChunkyImage newChunkyImage () {{
        var ChunkyImage i;
        var int width, height;

        let width = {width};
        let height = {height};

        let i = ChunkyImage.newBitmap(width, height);

"""
classFooter="""
        return i;
    }}
}}
"""

outfh.write(classHeader.format(filename = os.path.basename(infile),
                               cn = className,
                               width = parser.width,
                               height = parser.height))

data = []
index = 0
while parser.hasMoreTokens():
    data.append(int(parser.currentToken))

data = remapNM(parser.maxColour, 16, data)

index = 0
while index < len(data):
    outfh.write("        do i.push(" + formatNArgs(16, index, data) + ");\n")
    index += 16

outfh.write(classFooter.format())

parser.close()

outfh.close()
