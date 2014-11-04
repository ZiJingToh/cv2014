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
from inputmodehandler import InputModeHandler


class Movie(InputModeHandler):
    #========
    #Methods.
    #========
    def __init__(self, window, imageObj):
        #===================
        #Constructor Method.
        #===================
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
