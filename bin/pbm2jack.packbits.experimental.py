#!/usr/bin/env python3

"""pgm2jack

EXPERIMENTAL - Testing PackBits compression. Still writes normal uncompressed
image, and prints possible saving if PackBits were used. - EXPERIMENTAL

Convert a P1 pbm (monochome ascii, a.k.a. "Plain PBM") file to a
jack array (nand2tetris).

One word is 16bits in jack, so image width must be a multiple!

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

# For PackBits
from __future__ import absolute_import, unicode_literals, division, print_function

import sys
import os
import re
import math

class Parser ():
    """P1 PBM parser."""

    def __init__ (self, filename):
        if not os.path.exists(filename):
            sys.exit('Parser Error: Input file not found: %s' % filename)

        self._fh = open(filename, mode='r')
        self._currentWord = 0
        self._currentBit = 0;
        self._nextLine = None
        self._nextBit = ''
        self._explodeLines = False

        self.hasMoreLines()
        search = re.search(r'^P1$', self._nextLine)
        if not search: sys.exit('Failed to identify P1 type pbm')

        self.hasMoreLines()
        search = re.search(r'^(\d+)\s+(\d+)$', self._nextLine)
        if not search: sys.exit('Failed to identify resolution')
        self.width = int(search.group(1))
        self.height = int(search.group(2))
        if self.width%16 != 0: sys.exit('Width is not a multiple of 16')
        self.width = self.width // 16

        self._explodeLines = True
        self.hasMoreLines()

    def close(self):
        """Close input file"""
        self._fh.close()

    def hasMoreLines (self) :
        # Find the next non-empty line if one exists.
        line = None
        for line in self._fh:
            line = re.sub(r'#.*$', '', line)        # Remove comments
            line = re.sub(r'^\s+', '', line)        # Remove leading whitespace
            line = re.sub(r'\s+$', '', line)        # Remove trailing whitespace
            if len(line): break                     # Break if line not empty

        if line:
            if self._explodeLines:
                self._nextLine = list(line)
            else:
                self._nextLine = line
            return True

        return False

    def hasMoreBits (self) :
        # Find the next bit.
        if not len(self._nextLine):
            if not self.hasMoreLines():
                return False

        # Shift first bit from string.
        self._currentBit = self._nextLine.pop(0)

        return True

    def buildWord (self) :
        """buildWord - build a 16-bit word MSB to LSB, left to right.

        Returns a string of 16 bits.

        """
        word = ''
        word = self._currentBit
        for i in range(1,16):
            if self.hasMoreBits():
                word = self._currentBit + word
            else:
                word = 0 + word

        return word

### Mit Licensed PackBits for python ###
# https://github.com/kmike/packbits
def decodePackBits(data):
    """
    Decodes a PackBit encoded data.
    """
    data = bytearray(data) # <- python 2/3 compatibility fix
    result = bytearray()
    pos = 0
    while pos < len(data):
        header_byte = data[pos]
        if header_byte > 127:
            header_byte -= 256
        pos += 1

        if 0 <= header_byte <= 127:
            result.extend(data[pos:pos+header_byte+1])
            pos += header_byte+1
        elif header_byte == -128:
            pass
        else:
            result.extend([data[pos]] * (1 - header_byte))
            pos += 1

    return bytes(result)


def encodePackBits(data):
    """
    Encodes data using PackBits encoding.
    """
    if len(data) == 0:
        return data

    if len(data) == 1:
        return b'\x00' + data

    data = bytearray(data)

    result = bytearray()
    buf = bytearray()
    pos = 0
    repeat_count = 0
    MAX_LENGTH = 127

    # we can safely start with RAW as empty RAW sequences
    # are handled by finish_raw()
    state = 'RAW'

    def finish_raw():
        if len(buf) == 0:
            return
        result.append(len(buf)-1)
        result.extend(buf)
        buf[:] = bytearray()

    def finish_rle():
        result.append(256-(repeat_count - 1))
        result.append(data[pos])

    while pos < len(data)-1:
        current_byte = data[pos]

        if data[pos] == data[pos+1]:
            if state == 'RAW':
                # end of RAW data
                finish_raw()
                state = 'RLE'
                repeat_count = 1
            elif state == 'RLE':
                if repeat_count == MAX_LENGTH:
                    # restart the encoding
                    finish_rle()
                    repeat_count = 0
                # move to next byte
                repeat_count += 1

        else:
            if state == 'RLE':
                repeat_count += 1
                finish_rle()
                state = 'RAW'
                repeat_count = 0
            elif state == 'RAW':
                if len(buf) == MAX_LENGTH:
                    # restart the encoding
                    finish_raw()

                buf.append(current_byte)

        pos += 1

    if state == 'RAW':
        buf.append(data[pos])
        finish_raw()
    else:
        repeat_count += 1
        finish_rle()

    return bytes(result)
### END PackBits ###

### Helper functions ###
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

def wordBitStrToUBytes (bits) :
    """Convert a word bitstring (16-bits) into two unsigned bytes.

    Returns a two byte tupple.

    """
    byteH = int(bits[0:8], base=2)
    byteL = int(bits[8:16], base=2)

    return (byteH, byteL)

def uBytesToWordBitStr (byteH, byteL) :
    """Convert two unsigned bytes into a word bitstring (16-bits)

    Returns a string of 16 bits.

    """
    val = (byteH << 8) + byteL

    return "{0:016b}".format(val)

### Main ###

if len(sys.argv) < 3:
    sys.exit('Usage: %s <class name> <file.pbm>' % sys.argv[0])

className = sys.argv[1]
infile = sys.argv[2]

filename, ext = os.path.splitext(infile)
if ext != '.pbm':
    sys.exit("Expected file extension .pbm")

outfile = className + '.jack'

outfh = open(outfile, 'w')
parser = Parser(infile)

# Initialise data array rounded up to nearest multiple of 16, since we push
# 16 words at a time into bitmap.
data = [0] * int(math.ceil(parser.width * parser.height / 16) * 16);

# Declare a dataBytes array for the same data in bytes, for working with
# PackBits compression.
dataBytes = bytearray()
packedBytes = bytearray()

### Class declaration
classHeader="""/**
 * Static Image factory class.
 *
 * Requires Image.jack
 *
 * Generated from "{filename}" by pbm2jack.py
 *
 * Copyright 2013 Gavin Stewart.
 */
class {cn} {{

    /**
     * newImage - returns an Image object containing bitmap data.
     */
    function Image newImage () {{
        var Image i;
        var int width, height;

        let width = {width};
        let height = {height};

        let i = Image.newBitmap(width, height);

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

index = 0
while parser.hasMoreBits():
    bitWord = parser.buildWord()
    # print(bitWord)        # Debug
    data[index] = formatWord(bitWord);

    # Save the same word to the bytearray for later PackBits
    dataBytes.extend(list(wordBitStrToUBytes(bitWord)))

    index += 1

index = 0
while index < len(data):
    outfh.write("        do i.push({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15});\n".
            format(
                    data[index],
                    data[index +  1],
                    data[index +  2],
                    data[index +  3],
                    data[index +  4],
                    data[index +  5],
                    data[index +  6],
                    data[index +  7],
                    data[index +  8],
                    data[index +  9],
                    data[index + 10],
                    data[index + 11],
                    data[index + 12],
                    data[index + 13],
                    data[index + 14],
                    data[index + 15],
            )
    )
    index += 16

outfh.write(classFooter.format())

parser.close()

outfh.close()

# PackBits testing.

def dumpBytes (array) :
    """Print bytes as nibbles, two bytes to a line."""
    index = 0
    byteCount = 0;
    bytesPerLine = 2;
    for byteVal in array :
        print('{0:04b} {1:04b} '. format( (byteVal & 0xf0) >> 4, byteVal & 0x0f ), end='')
        byteCount += 1
        if byteCount == bytesPerLine:
            print()
            byteCount = 0
    if(byteCount < bytesPerLine):
        print()

print('Uncompressed size (bytes): ', len(dataBytes))
#dumpBytes(dataBytes)

packedBytes = encodePackBits(dataBytes)

print('Compressed size (bytes): ', len(packedBytes))
#dumpBytes(packedBytes)

#print ('Check decompression:')
#dumpBytes(decodePackBits(packedBytes))
