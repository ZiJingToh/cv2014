"""
=======================================================
Course: CS4243.
Course Title: Computer Vision & Pattern Recognition.
Project: CS4243 Project on 3D Walk-through of 2D Image.
Group Members: Dave Tan Woo Hong (A0106505R)
               Desmond Lim Hock Yeam (A0106477B)
               Toh Zijing (A0123506R)
               Darren Boo Kuok Liang (A0087547N)
=======================================================
=======   ==========   ===========  ============================================
Version      Date      Modified By                    Details
=======   ==========   ===========  ============================================
1.0.0     01/11/2014   ???          Initial Version of ProjectWindow Class
                                    incorporating the Methods: __init__,
                                    display, _mainLoop, _nextState, run.
"""

#===============
#Initialisation.
#===============
#if __name__ == '__main__' and __package__ is None:
#    from os import sys, path
#    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import cv2

from image import Image
from polygon import Polygon
from movie import Movie

STATES = [Polygon, Movie]

class ProjectWindow(object):
    """
    General Keys:
    Esc : Quit program
    F12 : Move to next state/mode

    States:

    1 - Polygon/Points mode
        User driven selection/creation of points,
        assignment of Z values to points
        Has inputs from user.

    2 - Free look mode, movie generation
        Has inputs from user to move camera around.
"""

    def __init__(self):
        #===================
        #Constructor Method.
        #===================
        self._viewport = "image"
        self._state = -1
        self._stateObj = None
        self._imageObj = None

    def display(self, view):
        cv2.imshow(self._viewport, view)

    def _mainLoop(self):
        # main loop
        while(1):
            key = cv2.waitKey(1) & 0xFF
            # Esc - quit program
            if key == 27:
                break
            # m - next state/mode
            if key == 109:
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
            self._stateObj = STATES[self._state](self, self._imageObj)
            # callback to handle mouse events
            cv2.setMouseCallback(self._viewport,
                                 self._stateObj.handleMouseEvents)
        else:
            self._stateObj = None

    def run(self, imagePath):
        # main view
        cv2.namedWindow(self._viewport, cv2.WINDOW_AUTOSIZE)

        # Initialise image object
        self._imageObj = Image(self, imagePath)

        # setup initial state
        self._nextState()

        # Initial display
        #self.display(self._imageObj.getView())

        self._mainLoop()

        cv2.destroyAllWindows()
