"""
Base class for state classes to have custom mouse/keyboard callbacks for the
main loop to access as a standard interface.

Classes inheriting must implement their own 
`handleKeyboardEvents` / `handleMouseEvents` OR use the included helper
dictionaries _mouseEvents` / `_keyboardEvents` to specify events and callbacks.
"""

class InputModeHandler(object):
    def __init__(self):
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
