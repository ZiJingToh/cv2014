
from .inputmodehandler import InputModeHandler


class Movie(InputModeHandler):
    def __init__(self, window, imageObj):
        super(Movie, self).__init__()
        self._window = window
        self._imageObj = imageObj

        self._modeName = "Movie"

        # mouse event callback of the form
        # { (EVENT, FLAGS):callback(x, y) }
        self._mouseEvents = {}

        # keyboard event callback of the form
        # { keychar:callback(key) }
        self._keyboardEvents = {"k":self._UIkeyframe}

    def _UIkeyframe(self, key):
        print "_UIkeyframe"

    def cleanup(self):
        """
        Cleanup after exiting state
        """
        print "Cleaning up after Movie..."
