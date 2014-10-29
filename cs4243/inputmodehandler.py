
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
            print self._modeName + " handleKeyboardEvents:", key
            self._keyboardEvents[key]()

    def handleMouseEvents(self, event, x, y, flags, param):
        if self._mouseEvents.has_key((event, flags,)):
            print self._modeName + " handleMouseEvents:", event, x, y, flags, param
            self._mouseEvents[(event, flags,)](x, y)

        elif self._mouseEvents.has_key((event, None,)):
            print self._modeName + " handleMouseEvents:", event, x, y, flags, param
            self._mouseEvents[(event, None,)](x, y)

        elif self._mouseEvents.has_key((None, flags,)):
            print self._modeName + " handleMouseEvents:", event, x, y, flags, param
            self._mouseEvents[(None, flags,)](x, y)
