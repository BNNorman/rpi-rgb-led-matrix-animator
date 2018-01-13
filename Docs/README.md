# README

This program provides a means to display simultaneous graphics,text and image animations on a LED RGB Matrix panel. It was started by a request, from a lorry/truck driver, to produce something more entertaining than the static LED logos you see in the back of many lorry/truck cabins.

My first, prototype, animated DAF truck logo was created using a hand soldered 180 LED panel driven by an Arduino Nano with animations inspired by the Arduino ALA library and is currently languishing in the cabin of a DAF truck.

I decided to try to use the cheap Chinese HUB75 RGB video panels as an alternative to all that soldering and to 
enable me to produce ANY animation of ANY logo. This would mean I could make a more robust unit which could be 
programmed rather than having custom PCB boards made. However, the cost of the RGB matrix panels soon mounts up, if you want high resolution, and may exceed the cost of creating a custom pcb populated with WS2812 leds by the pcb fabricator.

I also wanted to use a Raspberry Pi 3 to drive the LED panels since the memory available on a Pi exceeds that of the cheaper Arduino. Using python made it easier to create working code. On the Pi it is possible to play a pre-scaled video on the LED panel but playing sound at the same time is difficult - something to ponder on.

## Legal

Copyright (C) 2017 Brian Norman, brian.n.norman@gmail.com

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied 
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

https://www.gnu.org/licenses/gpl-3.0.en.html

YOU are solely responsible for using the software as intended. Anything which breaks the law is your liability.

## Bugs, errata and improvements

I'm always willing to hear of any bugs. You will need to let me have your main.py and any supporting documents 
(images etc). If you have modified my code I will need your version.

If you spot any documentation errors or any missing comments do let me know.

## Documentation

All python code has doc strings - my apologies if any need correcting or if some are missing.

In addition the Docs folder contains some more wordy explanations - again I apologise if there are errors or topics 
missing.

## Coding Inconsistencies

Sometimes we all do things the wrong way - for example directly accessing the attributes of an object with dot 
notation when adding a method would isolate against future code changes. I'm sure you will find many cases of this. 
I'm not sure what impact doing stuff the right way will have on the overall speed of the animator.

I have done my best to be consistent.

Having said that, you are at liberty to change the code as you see fit.