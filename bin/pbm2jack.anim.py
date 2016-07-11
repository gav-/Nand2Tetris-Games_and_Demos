#!/usr/bin/env python3

"""pgm2jack.anim

Convert a sequence of P1 pbm (monochome ascii, a.k.a. "Plain PBM") files to an
Anim Jack class (nand2tetris).

One word is 16bits in jack, so image width must be a multiple!

Currently delta frames must be 16 words (256 pixels) or less in width. Although
the base/initial image (first frame) may be larger.

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
import getopt

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

class Frame () :
    """Contains all information relating to a single frame"""

    def __init__ (self, filename):
        parser = Parser(filename)
        self.filename = filename
        self.width = parser.width
        self.height = parser.height
        self.bitmap = []    # Expressed as 16bit signed integers.

        self.delta =[]
        self.deltaXOffset = 0
        self.deltaYOffset = 0
        self.deltaWidth = 0
        self.deltaHeight = 0

        # Load bitmap data through parser.
        while parser.hasMoreBits():
            bitWord = parser.buildWord()
            self.bitmap.append(formatWord(bitWord))
        parser.close()

    def findDelta (self, diffFrame):
        """Identifies the differences between this frame and the provided one.

        """

        # Debug
        #data = []
        #for i in range(len(self.bitmap)):
        #    if self.bitmap[i] != diffFrame.bitmap[i]:
        #        data.append(self.bitmap[i])
        #print(data)


        # - Step through words looking for differences
        #   - Remember min x,y (offset) and max x,y (minus offset is size)
        # - Build list of mask word + data words for 16 consecutive words
        #   - First 16bit word is a mask bitmap. Following words are data values
        #     corresponding to set bits in mask. May be 0 to 16 data words.

        xMin = 999999       # Smallest x where words differ
        yMin = 999999       #    "     y   "     "     "
        xMax = -1           # Largest x where words differ
        yMax = -1           #    "    y  "      "     "

        # Step through words,  find min/max x/y for differences.
        x = 0
        y = 0
        for i in range(len(self.bitmap)):
            if self.bitmap[i] != diffFrame.bitmap[i]:
                # Note min and max x and y values.
                if x < xMin:
                    xMin = x
                if y < yMin:
                    yMin = y
                if x > xMax:
                    xMax = x
                if y > yMax:
                    yMax = y

            x = x + 1
            if x >= self.width:
                y = y + 1
                x = 0

        # Ensure x size <= 16   - GAV not needed now.
        #if xMax - xMin > 16:
        #    sys.exit('Calculated delta width ({0} words) must be <= 16 words for: {1}'.format(xMax - xMin, self.filename))

        # Calculate bit masks and delta words from min and max area.
        bitMask = ''           # 16 character bit string mask.
        bitMaskDelta = []      # Up to 16 delta words for mask set bits.

        delta = []             # Final encoded delta.

        x = 0
        y = 0
        for i in range(len(self.bitmap)):
            if x >= xMin and x <= xMax and y >= yMin and y <= yMax:
                if self.bitmap[i] != diffFrame.bitmap[i]:
                    bitMask = '1' + bitMask
                    bitMaskDelta.append(self.bitmap[i])
                else:
                    bitMask = '0' + bitMask

            if len(bitMask) == 16:                  # Completed 16 bit mask
                delta.append(formatWord(bitMask))   # Store mask (2's compl.)
                delta.extend(bitMaskDelta)          # Store delta data for mask
                bitMask = ''                        # Reset mask
                bitMaskDelta = []                   # Reset delta data

            x = x + 1
            if x >= self.width:
                y = y + 1
                x = 0

        # Store any remaining mask+words
        if len(bitMask) > 0:
            delta.append(formatWord(bitMask))
            delta.extend(bitMaskDelta)

        # Debug
        #print(delta)
        #sys.exit()

        self.delta = delta
        self.deltaXOffset = xMin
        self.deltaYOffset = yMin
        self.deltaWidth = xMax - xMin + 1
        self.deltaHeight = yMax - yMin + 1

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

def usage () :
    print("""
Usage: %s [-l] <class name> <file1.pbm> <file2.pbm> ...
    -l      : Anim is a loop, an extra delta is produced between last and
              first frames.
""" % os.path.basename(sys.argv[0]))

### Main ###

# Parse command line arguments
try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], 'lh')
except getopt.GetoptError as err:
    print(err)
    usage()
    sys.exit(2)

loop = False
for o, a in opts:
    if o == '-h':
        usage()
        sys.exit()
    elif o == '-l':
        loop = True
    else:
        assert False, "unhandled option"

if len(args) < 3:
    usage()
    sys.exit(2)

className = args[0]
infiles = args[1:]

outfile = className + '.jack'

outfh = open(outfile, 'w')

### Class declaration
classHeader="""/**
 * Static Anim factory class.
 *
 * Requires Anim.jack
 *
 * Generated from "{filename}" by pbm2jack.anim.py
 *
 * Copyright 2013 Gavin Stewart.
 */
class {cn} {{

    /**
     * newAnim - returns an Anim object.
     */
    function Anim newAnim () {{
        var Anim anim;
        var Image bf;               // Base Frame
        var Image df;               // Delta Frame

        let anim = Anim.new({loop}, {numFrames});
"""
classBaseFrame="""
        let bf = anim.newBaseFrame({width}, {height});
"""
classDeltaFrame="""
        let df = anim.newDeltaFrame({size}, {xOff}, {yOff}, {dWidth}, {dHeight});
"""
classFooter="""
        return anim;
    }}
}}
"""

# Write class header
numFrames = len(infiles)
if (loop) :
    numFrames += 1
outfh.write(classHeader.format(filename = os.path.basename(infiles[0]),
                               cn = className,
                               loop = 'true' if loop == True else 'false',
                               numFrames = numFrames ))

frames = []     # List of frames.

# Load all frame data.
for infile in infiles:
    filename, ext = os.path.splitext(infile)
    if ext != '.pbm':
        sys.exit("Expected file extension .pbm for %s" % infile)

    frame = Frame(infile)
    frames.append(frame)

# Write base frame data to class file.
outfh.write(classBaseFrame.format(width = frames[0].width,
                                  height = frames[0].height))

index = 0
while index < len(frames[0].bitmap):
    outfh.write("        do bf.push(" + formatNArgs(16, index, frames[0].bitmap) + ");\n")
    index += 16

# If we are looping, we calculate a delta between the first and last frames,
# so we never use the base frame again after the intitial rendering.
# This first delta is then actually redundant on the very first loop of the
# animation.
# !!! FIXME: This frame should be appended to the end of the animation,
#            makeing it _not_ redundant, and the anim just loops back to
#            frame 1 (not zero).
if (loop):
    frames[0].findDelta(frames[-1])
    outfh.write(classDeltaFrame.format(size = len(frames[0].delta),
                                       xOff = frames[0].deltaXOffset,
                                       yOff = frames[0].deltaYOffset,
                                       dWidth = frames[0].deltaWidth,
                                       dHeight = frames[0].deltaHeight))

    index = 0
    while index < len(frames[0].delta):
        outfh.write("        do df.push(" + formatNArgs(16, index, frames[0].delta) + ");\n")
        index += 16

# Write delta frames to class file.
for frameNumber in range(1, len(frames)):

    frame = frames[frameNumber]
    frame.findDelta(frames[frameNumber-1])

    outfh.write(classDeltaFrame.format(size = len(frame.delta),
                                       xOff = frame.deltaXOffset,
                                       yOff = frame.deltaYOffset,
                                       dWidth = frame.deltaWidth,
                                       dHeight = frame.deltaHeight))

    index = 0
    while index < len(frame.delta):
        outfh.write("        do df.push(" + formatNArgs(16, index, frame.delta) + ");\n")
        index += 16

# Write class footer and close file
outfh.write(classFooter.format())
outfh.close()
