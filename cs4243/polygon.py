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
1.0.0     26/10/2014   Dave Tan     Initial Version of Polygon Class
                                    incorporating the Methods: __init__,
                                    normalise, quatconj, point2quat, rot2quat,
                                    quatmult, quat2rot, rotbyquatmult,
                                    rotbyrotmat.
2.0.0     01/11/2014   Toh Zijing   Updated "__init__" Constructor Method and
                                    added new Methods: _clearSetPoints,
                                    _UImouseClickPoint, _UIdeleteLastPoint,
                                    _UIenterDepthValue, _hasPoint, _addPoint,
                                    _redrawView, cleanup.
          02/11/2014   Dave Tan     Renamed the Methods introduced in v1.0.0 to
                                    prepend "_" before the Method as well as
                                    changing to Camel Case. Updated all affected
                                    Methods to use the updated Method Names.
                                    Added the following new Method:
                                    _rotByImage.
2.0.1     04/11/2014   Dave Tan     Removed all Class Attributes and stick to
                                    Instance Attributes.
                                    Cleaned up Method _rotByImage.
3.5.0     15/11/2014   Toh ZiJing   Updated UI to be able to draw lines in
                                    addition to creating points
"""

#===============
#Initialisation.
#===============
#if __name__ == '__main__' and __package__ is None:
#    from os import sys, path
#    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from inputmodehandler import InputModeHandler
import numpy as np
import cv2
import os

# For saving/loading points.
SAVE_FILE = os.path.join(os.path.dirname(__file__), "polygon_points_save.txt")


class Polygon(InputModeHandler):
    """
    **************
    Class Polygon.
    **************
    =========
    Sypnosis.
    =========
    This is a Class representing the Polygon Object that is carved out from the
    User Interface, along with its associated Polygon Operations.

    ========
    Methods.
    ========
    __init__: This is the Constructor Method for Class Polygon.
    
    _normalise: #This Method normalises a Vector by its Magnitude.
    
    _quatConj: This Method returns the Conjugate of the given Quaternion.
    
    _point2Quat: This Method converts an Input Vector to its Quaternion
    Representation.

    _rot2Quat: This Method calculates the Quaternion for the Rotation Angle
    Theta given the Rotation Axis specified by wx, wy and wz.

    _quatMult: This Method performs the Quaternion Multiplications given 2 Input
    Quaternions which are essentially 2 4-Element Input Vectors.

    _quat2Rot: This Method returns the 3 x 3 Rotation Matrix parameterized with
    the Elements of a given Intput Quaternion.

    _rotByQuatMult: This Method performs the Rotation of a Point using Quaternion
    Multiplications given the Coordinates of the Point, the Angle of Rotation
    and the Axis of Rotation through wx, wy and wz. For the specified number of
    iterations, it will perform the Rotation and return the results in n x 3
    Array where n is the total number of Rows affected by the number of
    iterations.

    _rotByRotMat: This Method performs the Rotation of the Camera Orientation at
    a given Frame provided in the form of a 3 x 3 Matrix. The Rotation Matrix of
    the Rotation Quarternion is used. For the specified number of iterations, it
    will perform the Rotation and return the results in n x 3 Array where n is
    the total number of Rows affected by the number of iterations.
    """
    
    #========
    #Methods.
    #========
    def __init__(self, window, imageObj):
        #===================
        #Constructor Method.
        #===================
        super(Polygon, self).__init__()
        self._window = window
        self._imageObj = imageObj

        self._modeName = "Polygon"
        self._coordMode = "Z" # X, Y or Z

        # set to store clicked points
        self._last2SelectedPoints = []
        self._edges = set()
        self._points = []
        self._selectedPoint = None
        self._valueStr = ""
        self._clearSetPoints()

        # mouse event callback of the form
        # { (EVENT, FLAGS):callback(x, y) }
        self._mouseEvents = {(cv2.EVENT_LBUTTONUP, None,):self._UImouseClickPoint}

        # keyboard event callback of the form
        # { keychar:callback(key) }
        self._keyboardEvents = {chr(127):self._UIdeletePoint, # delete key
                                "0":self._UIenterValue,
                                "1":self._UIenterValue,
                                "2":self._UIenterValue,
                                "3":self._UIenterValue,
                                "4":self._UIenterValue,
                                "5":self._UIenterValue,
                                "6":self._UIenterValue,
                                "7":self._UIenterValue,
                                "8":self._UIenterValue,
                                "9":self._UIenterValue,
                                "q":self._UIsetCoordMode,
                                "w":self._UIsetCoordMode,
                                "e":self._UIsetCoordMode,
                                chr(13):self._UIenterValue, # enter key
                                "p":self._setEdge,
                                "o":self._disconnectEdges,
                                "c":self._clearSetPoints,
                                ",":self._selectPrevPoint,
                                ".":self._selectNextPoint,
                                "s":self._savePoints,
                                "l":self._loadPoints}

    def _UIsetCoordMode(self, key):
        if key == "q":
            self._coordMode = "X"
        elif key == "w":
            self._coordMode = "Y"
        elif key == "e":
            self._coordMode = "Z"
        print "Coord Mode: ", self._coordMode

    def _setEdge(self, key):
        if len(self._last2SelectedPoints) != 2:
            return
        self._edges.add(tuple(sorted(self._last2SelectedPoints)))
        self._last2SelectedPoints = []
        self._imageObj.interpolateImagePoints(self._points, self._edges)
        self._redrawView()

    def _disconnectEdges(self, key):
        for e in list(self._edges):
            if self._selectedPoint in e:
                self._edges.remove(e)
        self._imageObj.interpolateImagePoints(self._points, self._edges)
        self._redrawView()

    def _clearSetPoints(self, key=None):
        """
        Clears point set, creates initial 4 corner points
        """
        self._selectedPoint = None
        self._edges = set()
        self._last2SelectedPoints = []
        self._points = []
        self._points.append((0,0,))
        self._points.append((self._imageObj.getWidth()-1,0,))
        self._points.append((0,self._imageObj.getHeight()-1,))
        self._points.append((self._imageObj.getWidth()-1,
                             self._imageObj.getHeight()-1,))
        self._imageObj.resetImagePoints()
        self._redrawView()

    def _UImouseClickPoint(self, x, y):
        """
        Adds point to points list if point does not exist
        already, otherwise do selection of point
        """
        x, y = self._imageObj.convertToImageSpace(x, y)
        selected = self._hasPoint(x, y)
        if selected:
            if selected != self._selectedPoint:
                self._valueStr = ""
                self._last2SelectedPoints.append(selected)
                if len(self._last2SelectedPoints) > 2:
                    self._last2SelectedPoints = self._last2SelectedPoints[-2:len(self._last2SelectedPoints)]
            self._selectedPoint = selected
            print "=" * 80
            print "Selected point: ", self._selectedPoint
            print "Current point ", self._coordMode, ": ", self._imageObj.getCoordsFor(*self._selectedPoint)
            print "Enter selected point ", self._coordMode, ": ", self._valueStr
            print "=" * 80
        else:
            self._selectedPoint = None
            self._addPoint(x, y)
        self._redrawView()

    def _UIdeletePoint(self, key):
        if (len(self._points) > 4 and self._selectedPoint and
            not self._selectedPoint in self._points[:4]):
            print self._selectedPoint
            if self._selectedPoint in self._points:
                self._points.remove(self._selectedPoint)

                for e in list(self._edges):
                    if self._selectedPoint in e:
                        self._edges.remove(e)

                self._imageObj.interpolateImagePoints(self._points, self._edges)
                self._last2SelectedPoints = []
                self._selectedPoint = None
            self._redrawView()

    def _UIenterValue(self, key):
        if self._selectedPoint:
            if key.isdigit():
                self._valueStr = self._valueStr + key
                print "=" * 80
                print "Current point ", self._coordMode, ": ", self._imageObj.getCoordsFor(*self._selectedPoint)
                print "Enter selected point depth: ", self._valueStr
            elif key == chr(13):
                print "Point {0} set to {1}: {2}".format(self._selectedPoint,
                                                         self._coordMode,
                                                         self._valueStr)
                print "=" * 80
                if self._coordMode == "X":
                    self._imageObj.setXAt(int(self._valueStr), *self._selectedPoint)
                elif self._coordMode == "Y":
                    self._imageObj.setYAt(int(self._valueStr), *self._selectedPoint)
                elif self._coordMode == "Z":
                    self._imageObj.setZAt(int(self._valueStr), *self._selectedPoint)
                self._valueStr = ""
                self._imageObj.interpolateImagePoints(self._points, self._edges)
                self._redrawView()

    def _hasPoint(self, x, y):
        radius = int(15 * (1.0/self._imageObj.getViewScale()))

        if (x, y,) in self._points:
            return x, y

        for px, py in self._points:
            if (x >= px-radius and x <= px+radius and
                y >= py-radius and y <= py+radius):
                return px, py
        return None

    def _addPoint(self, x, y):
        print "=" * 80
        print "Adding point: ", (x, y, )
        print "=" * 80
        self._points.append((x, y,))
        self._redrawView()

    def _selectPrevPoint(self, key):
        if self._selectedPoint:
            index = self._points.index(self._selectedPoint)
            index -= 1
            index %= len(self._points)
            self._UImouseClickPoint(*self._imageObj.convertToViewSpace(
                *self._points[index]))
        else:
            self._UImouseClickPoint(0, 0)

    def _selectNextPoint(self, key):
        if self._selectedPoint:
            index = self._points.index(self._selectedPoint)
            index += 1
            index %= len(self._points)
            self._UImouseClickPoint(*self._imageObj.convertToViewSpace(
                *self._points[index]))
        else:
            self._UImouseClickPoint(0, 0)
        
    def _redrawView(self):
        view = self._imageObj.getView()
        # draw edges
        for e in self._edges:
            cv2.line(view,
                     self._imageObj.convertToViewSpace(*e[0]),
                     self._imageObj.convertToViewSpace(*e[1]),
                     (0,255,255),
                     2)
        # draw points
        for point in self._points:
            cpoint = self._imageObj.convertToViewSpace(*point)
            if point == self._selectedPoint:
                cv2.circle(view, cpoint, 5, (0,0,255,), 8)
                cv2.circle(view, cpoint, 5, (0,255,0,), 2)
            else:
                cv2.circle(view, cpoint, 5, (0,0,255,), 2)
        # display to window
        self._window.display(view)

    def _savePoints(self, key):
        print "Saving Points...."
        pointsStr = str(self._points)
        edgesStr = str(self._edges)
        xStr = str([self._imageObj.getXAt(*p) for p in self._points])
        yStr = str([self._imageObj.getYAt(*p) for p in self._points])
        zStr = str([self._imageObj.getZAt(*p) for p in self._points])

        fd = open(SAVE_FILE, "w+")
        fd.writelines([pointsStr, "\n",
                       edgesStr, "\n",
                       xStr, "\n",
                       yStr, "\n",
                       zStr, "\n"])
        fd.close()

    def _loadPoints(self, key):
        print "Loading Points..."
        if not os.path.exists:
            return

        self._clearSetPoints()

        fd = open(SAVE_FILE, "r")
        lines = fd.readlines()
        fd.close()

        self._points = eval(lines[0])
        self._edges = eval(lines[1])
        xValues = eval(lines[2])
        yValues = eval(lines[3])
        zValues = eval(lines[4])

        for index, point in enumerate(self._points):
            self._imageObj.setXAt(xValues[index], *point)
            self._imageObj.setYAt(yValues[index], *point)
            self._imageObj.setZAt(zValues[index], *point)

        self._imageObj.interpolateImagePoints(self._points, self._edges)

        self._redrawView()

    def cleanup(self):
        """
        Cleanup after exiting state
        """
        print "Cleaning up after Polygon..."
        self._imageObj.gridimage(self._points)

        # TESTING CODE - TO REMOVE!!
        #img = self._imageObj._image.copy()
        #for e in self._imageObj._tri.edges:
        #    cv2.line(img,
        #             tuple(self._imageObj._selected2DPoints[e[0]][:2]),
        #             tuple(self._imageObj._selected2DPoints[e[1]][:2]), (0,255,0))
        #img = self._imageObj.getResizedImage(img)
        #self._window.display(img)
        #cv2.waitKey(0)

        # TESTING CODE - TO REMOVE!!
        '''cam = [self._imageObj.getWidth()/2, self._imageObj.getHeight()/2, 300]
        orient = np.eye(3)
        for rot in xrange(0,61,20):
            orient = self._imageObj._rotByRotMat(np.eye(3), rot, 0, 1, 0, 1)
            newImage = self._imageObj.getImageFromCam(cam, orient, 500)
            self._window.display(self._imageObj.getResizedImage(newImage))
            #cv2.imwrite(str(rot)+".jpg", newImage)
            cv2.waitKey(0)'''
        


        
        
        

