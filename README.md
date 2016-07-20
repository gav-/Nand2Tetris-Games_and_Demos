# Nand2Tetris Games and Demos
A collection of my Nand2Tetris games and demos. Nand2Tetris is an online,
self-teachable course on Building a Modern Computer from First Principles: 
http://www.nand2tetris.org/

Table of Contents
=================

  * [Nand2Tetris Games and Demos](#nand2tetris-games-and-demos)
  * [Table of Contents](#table-of-contents)
  * [General execution instructions](#general-execution-instructions)
  * [Games and Demos](#games-and-demos)
    * [GASchunky: Real-time Plasma and Rotozoom.](#gaschunky-real-time-plasma-and-rotozoom)
    * [GASboing: Bouncing boing ball](#gasboing-bouncing-boing-ball)
    * [GASscroller: Sinus text scroller](#gasscroller-sinus-text-scroller)
  * [Copyright](#copyright)
  * [Licence](#licence)

# General execution instructions
These programs are already compiled with the JackCompiler into vm code, they
just need to be loaded into the VMEmulator and executed as follows:

 - Download and install the Nand2tetris Software Suite (http://www.nand2tetris.org/software.php)
 - Start the VMEmulator.
 - Using File -> Load Program, select the application's directory 
   (e.g. GASchunky) and click the "Load Program" button.
 - Click the "Yes" button to the Confirmation Message pop-up.
 - Set the Animate: drop-down to "No animation".
 - Set the speed slider to "Fast" (not necessary for all demos).
 - Press "F5" to run.

# Games and Demos
## GASchunky: Real-time Plasma and Rotozoom.

![Alt text](GASchunky/screenshots/screenshot1.png?raw=true "Insert Work Bench")
![Alt text](GASchunky/screenshots/screenshot2.png?raw=true "Plasma")
![Alt text](GASchunky/screenshots/screenshot3.png?raw=true "Rotozoom")

[![YouTube Video: Real-time Plasma and Rotozoom Demo](https://s.ytimg.com/yts/img/favicon_48-vfl1s0rGh.png)<br>Watch the YouTube video](http://www.youtube.com/watch?v=yGV4t_94TiI)

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

## GASboing: Bouncing boing ball
![Alt text](GASboing/screenshots/screenshot1.png?raw=true "Bouncing boing ball")

[![YouTube Video: Bouncing Ball Demo](https://s.ytimg.com/yts/img/favicon_48-vfl1s0rGh.png)<br>Watch the YouTube video](http://www.youtube.com/watch?v=L_uQlRq6BhI)

A classic bouncing boing ball demo that originated on the Amiga and has since
been duplicated on many other systems.

This version was inspired by the bouncing ball segment in this ZX81 Demo 
"25thanni": https://youtu.be/sKj6TaADFWo?t=90

The change in direction of the ball's rotation on rebounding was the give away 
on how to achieve this effect cheaply. The original Amiga Boing Ball demo 
(https://youtu.be/-ga41edXw3A?t=27) used palette cycling to give the impression
of rotation, we don't have that option on the Hack machine. I had already done
significant experimentation with bitmap animations on Hack. The solution was to
blit a sequence of pre-shifted bitmaps to screen giving the illusion of 
rotation AND horizontal movement. On rebounding, the sequence is simply
reversed, changing the direction of rotation and horizontal motion.

Pre-calculation of expensive arithmetic is key to high performance animation.
Copying a 16-bit word (16 consecutive pixels) to screen memory is cheap,
calculating a bit shift for the next animation frame would be very expensive.
I started with eight frames of the Boing Ball rotating, rendered with Blender.

The frames were scaled, cropped, quantised to two colours, shifted by two
pixels, and padded to an image that was a multiple of 16 pixels in width
(using Gimp). This GIF shows the eight frames played back in sequence. Note
that each frame is the same size, overlaid on the previous, in the same
location! Only the contents of each frame gives the illusion of motion:
![Alt text](GASboing/assets/amiga-ball.64.gif?raw=true "Bouncing boing ball")

Each frame was saved out, and converted into a Jack object via a Python script.

When playing back, the eight frames are blitted to the same location in screen
memory. On completion of the eighth frame, the memory location is incremented
by one word, and the sequence is repeated. The sequence was designed with
enough background coloured border to ensure that the consecutive blitted frame
would erase the trail of the previous, so no flickering occurs from blanking
(at least for horizontal motion).

The vertical motion of the ball is from a pre-calculated sine table. There is
also some blanking required to erase the remainder of the previous frame above
(or below) the current one.

## GASscroller: Sinus text scroller
![Alt text](GASscroller/screenshots/screenshot1.png?raw=true "Sinus text scroller")

This is a classic scrolling text demo!

The font is actually from the one embedded into the VMEmulator (as at this
stage in the course we hadn't made our own yet). It is printed to screen
and read back into an array one character at a time during the program 
initialisation.

The text is scrolled smoothly from right to left in steps of 2 pixels per
frame, with each word (16 horizontal pixels) offset vertically based on a 
value from a precalculated sine table.

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
