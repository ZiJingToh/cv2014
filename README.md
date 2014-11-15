CS4243 Project (2014)
=====================

This program is split up into 2 modes, with useful information echoed' out to the terminal:

Drawing Mode
------------
In this mode the idea is to be able to create/select/delete points, and be able to set x, y, z world coordinate values.
Any 2 points can also be linked together as a line to represent an explicit interpolation between the 2 points.

Keys:
 - Mouse left click     : create/select point
 - delete key           : delete point, and any lines connected to it
 - q,w,e                : set current coordinate edit  mode to x/y/z respectively
 - numeric keys + enter : set x/y/z value for selected point
 - p                    : create a line between 2 consecutively selected points
 - o                    : delete lines connected to selected point
 - m                    : move to next mode (movie mode)
 - esc                  : quit program

Movie Mode
----------
In this mode a perspective projection of the points will be shown. The user can then move the camera around, setting keyframes and then be able to generate a movie with the keyframes interpolated.

Keys:
 - w,s,a,d              : move camera forward, back, left, right respectively
 - q,r                  : rotate camera left, right respectively
 - enter                : save position as a keyframe
 - o                    : save out movie from keyframes
 - p                    : toggle display mode (normal, wireframe, points)
 - m/esc                : quit program


Running the program
===================
From the root of the project run:
> python run

That should launch the program showing the image.
