# Nand2Tetris Games and Demos
A collection of my Nand2Tetris (Elements of Computing) games and demos.
Nand2Tetris is the Elements of Computing course:
http://www.nand2tetris.org/

## General execution instructions
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

## GASchunky
Real-time Plasma and Rotozoom.

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

## Copyright
All programs and files are Copyright 2013-2016 Gavin Stewart.

You are required to give attribution to the author (Gavin Stewart) for any
use of these programs (GPLv3 Section 7b).

Trying to pass off my code as your own in your Elements of Computing classes
will result in a cursed life of forever buggy software.

## Licence
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
