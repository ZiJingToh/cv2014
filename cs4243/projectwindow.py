#!/usr/bin/env python

"""
States:

1 - Polygon/Points mode
    User driven selection/creation of polygons/points.
    Has inputs from user.

2 - Projection resolution
    No inputs from user.

3 - Free look mode, movie generation
    Has inputs from user to move camera around.

"""

import cv2

from .image import Image
from .polygon import Polygon
from .movie import Movie


STATES = [Polygon, Movie]


class ProjectWindow(object):
    def __init__(self):
        self._viewport = "image"
        self._state = -1
        self._stateObj = None
        self._imageObj = None

    def display(self):
        cv2.imshow(self._viewport, self._imageObj.getView())

    def _mainLoop(self):
        # main loop
        while(1):
            # global keyboard events
            # esc - quit program
            # F12 - next state/step
            key = cv2.waitKey(1) & 0xFF
            if key == 27:
                break
            if key == 15:
                # exit if no more states
                self._nextState()
                if not self._stateObj:
                    break
            self._stateObj.handleKeyboardEvents(key)

    def _nextState(self):
        if self._stateObj:
            self._stateObj.cleanup()
        self._state += 1
        if self._state < len(STATES):
            self._stateObj = STATES[self._state](self._imageObj)
            # callback to handle mouse events
            cv2.setMouseCallback(self._viewport, self._stateObj.handleMouseEvents)
        else:
            self._stateObj = None

    def run(self, imagePath):
        # main view
        cv2.namedWindow(self._viewport, cv2.WINDOW_NORMAL)

        # Initialise image object
        self._imageObj = Image(self, imagePath)

        # setup initial state
        self._nextState()

        # Initial display
        self.display()

        self._mainLoop()

        cv2.destroyAllWindows()
