# Nand2Tetris Games and Demos
A collection of my Nand2Tetris (Elements of Computing) games and demos.
Nand2Tetris is the Elements of Computing course:
http://www.nand2tetris.org/

Table of Contents
=================

  * [Nand2Tetris Games and Demos](#nand2tetris-games-and-demos)
  * [Table of Contents](#table-of-contents)
  * [General execution instructions](#general-execution-instructions)
  * [Games and Demos](#games-and-demos)
    * [GASchunky: Real-time Plasma and Rotozoom.](#gaschunky-real-time-plasma-and-rotozoom)
    * [GASscroller: Sinus text scroller](#gasscroller-sinus-text-scroller)
  * [Copyright](#copyright)
  * [Licence](#licence)

# General execution instructions
These programs are already compiled with the JackCompiler into vm code, they
just need to be loaded into the VMEmulator and executed as follows:

 - Download and install the Nand2testris Software Suite (http://www.nand2tetris.org/software.php)
 - Start the VMEmulator.
 - Using File -> Load Program, select the application's directory 
   (e.g. GASchunky) and click the "Load Program" button.
 - Click the "Yes" button to the Confirmation Message popup.
 - Set the Animate: dropdown to "No animation".
 - Set the speed slider to "Fast" (not necessary for all demos).
 - Press "F5" to run.

# Games and Demos
## GASchunky: Real-time Plasma and Rotozoom.

![Alt text](GASchunky/screenshots/screenshot1.png?raw=true "Insert Work Bench")
![Alt text](GASchunky/screenshots/screenshot2.png?raw=true "Plasma")
![Alt text](GASchunky/screenshots/screenshot3.png?raw=true "Rotozoom")

[Watch the YouTube video](https://www.youtube.com/watch?v=yGV4t_94TiI)

This is the most CPU intensive Nand2Tetris demo I have done so far. 'Fast' 
mode is required in the VMEmulator on an Intel i5 2500K CPU running Linux 
Mint with OpenJDK 1.7.0_25. All code is written in pure Jack and compiled 
with the provided complier running on the provided VMEmulator. 

Conversion from a chunky bitmap to planar architecture is done on-the-fly 
with 17 greyscale shades. Each shade in the chunky source image is converted 
to a 4x4 pixel block in the final output through an ordered dither table.
http://en.wikipedia.org/wiki/Ordered_dithering

The monitor image is an adaptation of 'Amiga Lagoon' artwork by the famous 
Amiga artist James "Jim" Sachs.
http://www.palmerfamily.name/sachs.html
http://www.youtube.com/user/JDSachs

The demon head was adapted from the fantastic Second Reality PC demo by Future 
Crew.
http://www.youtube.com/watch?v=rFv7mHTf0nA

## GASscroller: Sinus text scroller
![Alt text](GASscroller/screenshots/screenshot1.png?raw=true "Sinus text scroller")

This is a classic scrolling text demo!

The font is actually from the one embedded into the VMEmulator as at this
stage in the course you won't have made your own yet. It is rendered to screen
a character at a time and saved into an array during the program initialisation.

The text is scrolled from right to left in steps of 2 pixels.

The comments at the top of GASscroller.jack describe how the magic of
updating ring buffers can reduce the number of calculations required to do
this. Normally I keep references to any research I have done, and I don't see
one here, but I do recall that I used some article about scrolling on the
Commodore 64 for this one.

# Copyright
All programs and files are Copyright 2013-2016 Gavin Stewart.

You are required to give attribution to the author (Gavin Stewart) for any
use of these programs (GPLv3 Section 7b).

Trying to pass off my code as your own in your Elements of Computing classes
will result in a cursed life of forever buggy software.

# Licence
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
