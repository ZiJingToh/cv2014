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
1.0.0     01/11/2014   Toh Zijing   Added new Class InputModeHandler.
"""

#===============
#Initialisation.
#===============
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

class InputModeHandler(object):
    """
    ***********************
    Class InputModeHandler.
    ***********************
    =========
    Sypnosis.
    =========
    Base class for state classes to have custom mouse/keyboard callbacks for the
    main loop to access as a standard interface.

    Classes inheriting must implement their own
    `handleKeyboardEvents` / `handleMouseEvents` OR use the included helper
    dictionaries _mouseEvents` / `_keyboardEvents` to specify events and
    callbacks.
    """

class InputModeHandler(object):
    #======================
    #Properties/Attributes.
    #======================
    _modeName = None
    _mouseEvents = None
    _keyboardEvents = None

    #========
    #Methods.
    #========
    def __init__(self):
        #===================
        #Constructor Method.
        #===================
        self._modeName = None

        # mouse event callback of the form
        # { (EVENT, FLAGS):callback(x, y) }
        self._mouseEvents = {}

        # keyboard event callback of the form
        # { keychar:callback() }
        self._keyboardEvents = {}

    def handleKeyboardEvents(self, key):
        key = chr(key)
        if self._keyboardEvents.has_key(key):
            self._keyboardEvents[key](key)

    def handleMouseEvents(self, event, x, y, flags, param):
        if self._mouseEvents.has_key((event, flags,)):
            self._mouseEvents[(event, flags,)](x, y)

        elif self._mouseEvents.has_key((event, None,)):
            self._mouseEvents[(event, None,)](x, y)

        elif self._mouseEvents.has_key((None, flags,)):
            self._mouseEvents[(None, flags,)](x, y)
