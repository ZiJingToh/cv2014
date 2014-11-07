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
        self._view = self._imageObj.getView()

        self._modeName = "Polygon"

        # set to store clicked points
        self._points = []
        self._selectedPoint = None
        self._depthStr = ""
        self._clearSetPoints()

        # mouse event callback of the form
        # { (EVENT, FLAGS):callback(x, y) }
        self._mouseEvents = {(cv2.EVENT_LBUTTONUP, None,):self._UImouseClickPoint}

        # keyboard event callback of the form
        # { keychar:callback(key) }
        self._keyboardEvents = {chr(127):self._UIdeletePoint, # delete key
                                "0":self._UIenterDepthValue,
                                "1":self._UIenterDepthValue,
                                "2":self._UIenterDepthValue,
                                "3":self._UIenterDepthValue,
                                "4":self._UIenterDepthValue,
                                "5":self._UIenterDepthValue,
                                "6":self._UIenterDepthValue,
                                "7":self._UIenterDepthValue,
                                "8":self._UIenterDepthValue,
                                "9":self._UIenterDepthValue,
                                chr(13):self._UIenterDepthValue, # enter key
                                "c":self._clearSetPoints,
                                ",":self._selectPrevPoint,
                                ".":self._selectNextPoint,
                                "s":self._savePoints,
                                "l":self._loadPoints}

    def _clearSetPoints(self, key=None):
        """
        Clears point set, creates initial 4 corner points
        """
        self._selectedPoint = None
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
                self._depthStr = ""
            self._selectedPoint = selected
            print "=" * 80
            print "Selected point: ", self._selectedPoint
            print "Current point depth: ", self._imageObj.getCoordsFor(*self._selectedPoint)[-1]
            print "Enter selected point depth: ", self._depthStr
            print "=" * 80
        else:
            self._selectedPoint = None
            self._addPoint(x, y)
        self._redrawView()

    def _UIdeletePoint(self, key):
        if (len(self._points) > 4 and self._selectedPoint and
            not self._selectedPoint in self._points[:4]):
            if self._points.remove(self._selectedPoint):
                self._imageObj.setZAt([0,0,0], *self._selectedPoint)
                self._selectedPoint = None
            self._redrawView()

    def _UIenterDepthValue(self, key):
        if self._selectedPoint:
            if key.isdigit():
                self._depthStr = self._depthStr + key
                print "=" * 80
                print "Current point depth: ", self._imageObj.getCoordsFor(*self._selectedPoint)[-1]
                print "Enter selected point depth: ", self._depthStr
            elif key == chr(13):
                print "Point {0} set to depth: {1}".format(self._selectedPoint,
                                                           self._depthStr)
                print "=" * 80
                self._imageObj.setZAt(int(self._depthStr), *self._selectedPoint)
                self._depthStr = ""
                self._imageObj.interpolateImagePoints(self._points)
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
        self._view = self._imageObj.getView()
        for point in self._points:
            cpoint = self._imageObj.convertToViewSpace(*point)
            if point == self._selectedPoint:
                cv2.circle(self._view, cpoint, 5, (0,0,255,), 8)
                cv2.circle(self._view, cpoint, 5, (0,255,0,), 2)
            else:
                cv2.circle(self._view, cpoint, 5, (0,0,255,), 2)
        self._window.display(self._view)

    def _savePoints(self, key):
        pointsStr = str(self._points)
        zStr = str([self._imageObj.getZAt(*p) for p in self._points])

        fd = open(SAVE_FILE, "w+")
        fd.writelines([pointsStr, "\n",
                       zStr, "\n"])
        fd.close()

    def _loadPoints(self, key):
        if not os.path.exists:
            return

        self._clearSetPoints()

        fd = open(SAVE_FILE, "r")
        lines = fd.readlines()
        fd.close()

        self._points = eval(lines[0])
        zValues = eval(lines[1])

        for index, point in enumerate(self._points):
            self._imageObj.setZAt(zValues[index], *point)

        self._imageObj.interpolateImagePoints(self._points)

        self._redrawView()

    def cleanup(self):
        """
        Cleanup after exiting state
        """
        print "Cleaning up after Polygon..."
        points = np.array([(p[0],
                            p[1],
                            self._imageObj.getZAt(*p)) for p in self._points])
        self._imageObj.triangulate(points)

        # TESTING CODE
        cam = [self._imageObj.getWidth()/2, self._imageObj.getHeight()/2, -500]
        orient = np.eye(3)
        for rot in xrange(0,61,20):
            orient = self._rotByRotMat(np.eye(3), rot, 0, 1, 0, 1)
            newImage = self._imageObj.getImageFromCam(cam, orient, np.abs(cam[-1]))
            self._window.display(self._imageObj.getResizedImage(newImage))
            cv2.waitKey(0)

    def _normalise(self, listInput):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        import math as ma
        intLength = len(listInput)
        listInput_normalised = np.zeros(intLength)
        listInput_mag_square = \
                             sum(fltElement * fltElement\
                                 for fltElement in listInput)
        listInput_mag = ma.sqrt(listInput_mag_square)

        #==========================
        #Perform the Normalisation.
        #==========================
        for intIndex in range(0, intLength, 1):
            listInput_normalised[intIndex] = listInput[intIndex] / listInput_mag

        #=============================
        #Return the Normalised Vector.
        #=============================
        return(listInput_normalised)

    def _quatConj(self, q):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        sq = q[0]
        vq = [0, 0, 0]
        neg_vq = [0, 0, 0]
        vq[0] = q[1]
        vq[1] = q[2]
        vq[2] = q[3]
        neg_vq[0] = -1 * vq[0]
        neg_vq[1] = -1 * vq[1]
        neg_vq[2] = -1 * vq[2]

        #======================
        #Compute the Conjugate.
        #======================
        q_conj = np.append(sq, neg_vq)

        #=======================================
        #Return the Conjugate of the Quaternion.
        #=======================================
        return(q_conj)

    def _point2Quat(self, arrPointVector):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        sq = 0
        vq = arrPointVector

        #======================================
        #Compose the Quaternion Representation.
        #======================================
        q = np.append(sq, vq)
        vq = q[1:]

        #===================
        #Return the Outputs.
        #===================
        return(sq, vq, q)

    def _rot2Quat(self, fltTheta, wx, wy, wz):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        import math as ma
        wx, wy, wz = self._normalise([wx, wy, wz])
        vq = np.zeros([1, 3])
        fltTheta_radians = ma.radians(fltTheta)

        #=============================
        #Compute the Scalar Component.
        #=============================
        sq = ma.cos(fltTheta_radians / 2)

        #=============================
        #Compute the Vector Component.
        #=============================
        vq[0, 0] = ma.sin(fltTheta_radians / 2) * wx
        vq[0, 1] = ma.sin(fltTheta_radians / 2) * wy
        vq[0, 2] = ma.sin(fltTheta_radians / 2) * wz

        #========================================================
        #Construct the Quaternion Representation of the Rotation.
        #========================================================
        q = np.append(sq, vq)

        #===============================================================
        #Return the Quarternion Representation of the Rotation provided.
        #===============================================================
        return(sq, vq, q)

    def _quatMult(self, q1, q2):
        #===============
        #Initialisation.
        #===============
        out = [0, 0, 0, 0]
        q1_0 = q1[0]
        q1_1 = q1[1]
        q1_2 = q1[2]
        q1_3 = q1[3]
        q2_0 = q2[0]
        q2_1 = q2[1]
        q2_2 = q2[2]
        q2_3 = q2[3]

        #======================================
        #Perform the Quaternion Multiplication.
        #======================================
        out[0] = (q1_0 * q2_0) - (q1_1 * q2_1) - (q1_2 * q2_2) - (q1_3 * q2_3)
        out[1] = (q1_0 * q2_1) + (q1_1 * q2_0) + (q1_2 * q2_3) - (q1_3 * q2_2)
        out[2] = (q1_0 * q2_2) - (q1_1 * q2_3) + (q1_2 * q2_0) + (q1_3 * q2_1)
        out[3] = (q1_0 * q2_3) + (q1_1 * q2_2) - (q1_2 * q2_1) + (q1_3 * q2_0)

        #==================
        #Return the Result.
        #==================
        return out

    def _quat2Rot(self, q):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        Rq = np.zeros([3, 3])
        q = self._normalise(q)
        q_0 = q[0]
        q_1 = q[1]
        q_2 = q[2]
        q_3 = q[3]

        #============================
        #Compute the Rotation Matrix.
        #============================
        Rq[0, 0] = (q_0 * q_0) + (q_1 * q_1) - (q_2 * q_2) - (q_3 * q_3)
        Rq[0, 1] = 2 * ((q_1 * q_2) - (q_0 * q_3))
        Rq[0, 2] = 2 * ((q_1 * q_3) + (q_0 * q_2))
        Rq[1, 0] = 2 * ((q_1 * q_2) + (q_0 * q_3))
        Rq[1, 1] = (q_0 * q_0) + (q_2 * q_2) - (q_1 * q_1) - (q_3 * q_3)
        Rq[1, 2] = 2 * ((q_2 * q_3) - (q_0 * q_1))
        Rq[2, 0] = 2 * ((q_1 * q_3) - (q_0 * q_2))
        Rq[2, 1] = 2 * ((q_2 * q_3) + (q_0 * q_1))
        Rq[2, 2] = (q_0 * q_0) + (q_3 * q_3) - (q_1 * q_1) - (q_2 * q_2)

        #===========================
        #Return the Rotation Matrix.
        #===========================
        return Rq

    def _rotByQuatMult(self, pt, fltTheta, wx, wy, wz, intIterations):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        matRotatedPoints = np.zeros([1, 3])
        pt2rot = pt

        #===================================================================
        #Perform the Rotation using Quaternion Multiplications and store the
        #Rotated Points in an Array containing the Rotated Points.
        #===================================================================
        for intIndex in range(0, intIterations, 1):
            #======================================================
            #Perform the Rotation using Quaternion Multiplications.
            #======================================================
            sp, vp, p = self._point2Quat(pt2rot)
            sq, vq, q = self._rot2Quat(fltTheta, wx, wy, wz)
            q_conj = self._quatConj(q)
            qp = self._quatMult(q, p)
            p_rot = self._quatMult(qp, q_conj)

            #============================================================
            #Store the Rotated Point, discard the Scalar Portion of qpq*.
            #============================================================
            if(intIndex == 0):
                #====================
                #First Rotated Point.
                #====================
                matRotatedPoints[0, 0] = p_rot[1]
                matRotatedPoints[0, 1] = p_rot[2]
                matRotatedPoints[0, 2] = p_rot[3]
            else:
                #=========================
                #Subsequent Rotated Point.
                #=========================
                arrayTemp = [0, 0, 0]
                arrayTemp[0] = p_rot[1]
                arrayTemp[1] = p_rot[2]
                arrayTemp[2] = p_rot[3]
                matRotatedPoints = np.append([matRotatedPoints], [arrayTemp])

            #==================================
            #Change Starting Point of Rotation.
            #==================================
            pt2rot = [p_rot[1], p_rot[2], p_rot[3]]
            arrayTemp = np.zeros([1, 3])

        #===============================================
        #Return the Array containing the Rotated Points.
        #===============================================
        matRotatedPoints = np.matrix(matRotatedPoints)
        intRows = matRotatedPoints.shape[0]
        intColumns = matRotatedPoints.shape[1]
        intElements = intRows * intColumns
        intNewRows = int(intElements / 3)
        matRotatedPoints = np.reshape(matRotatedPoints, (intNewRows, 3))
        return(matRotatedPoints)

    def _rotByRotMat(self, matCamFr, fltTheta, wx, wy, wz, intIterations):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        matCamFr = np.matrix(matCamFr)
        matCurrentCamFr = np.zeros([3, 3])

        #===============================
        #Obtain the Rotation Quaternion.
        #===============================
        s_qrot, v_qrot, q_rot = self._rot2Quat(fltTheta, wx, wy, wz)
        matRot = np.matrix(self._quat2Rot(q_rot))

        #=======================================================================
        #Perform the Rotation using Matrix Multiplications and store the Rotated
        #Camera Orientations in an n x 3 Array containing the Rotated Points.
        #=======================================================================
        for intIndex in range(0, intIterations, 1):
            #==================================================================
            #Perform the Matrix Multiplication utilisating the Rotation Matrix.
            #==================================================================
            for intSquareIndex in range(0, 3, 1):
                listPt = matCamFr[intSquareIndex, :]
                matNewCamPt = matRot * np.transpose(listPt)
                matCurrentCamFr[intSquareIndex, :] = np.transpose(matNewCamPt)

                #===============================================
                #Store the Rotated Camera Orientation of Points.
                #===============================================
                if(intIndex == 0):
                    #===========================================
                    #First Rotated Camera Orientation of Points.
                    #===========================================
                    matRotatedPoints = matCurrentCamFr
                else:
                    #================================================
                    #Subsequent Rotated Camera Orientation of Points.
                    #================================================
                    matRotatedPoints = np.append([matRotatedPoints],
                                                 matCurrentCamFr)

            #==================================
            #Change Starting Point of Rotation.
            #==================================
            matCamFr = matCurrentCamFr

        #===============================================
        #Return the Array containing the Rotated Points.
        #===============================================
        matRotatedPoints = np.matrix(matRotatedPoints)
        intRows = matRotatedPoints.shape[0]
        intColumns = matRotatedPoints.shape[1]
        intElements = intRows * intColumns
        intNewRows = int(intElements / 3)
        matRotatedPoints = np.reshape(matRotatedPoints, (intNewRows, 3))
        return(matRotatedPoints)

    def _rotByImage(self, objImage3D, fltTheta, wx, wy, wz, intIterations = 1):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        listRotated3DScene = objImage3D._flat_3dpoints

        #===============================
        #Obtain the Rotation Quaternion.
        #===============================
        s_qrot, v_qrot, q_rot = self._rot2Quat(fltTheta, wx, wy, wz)
        matRot = np.matrix(self._quat2Rot(q_rot))

        #===========================================
        #Perform the Rotation using Rotation Matrix.
        #===========================================
        listRotated3DScene = matRot * np.transpose(listRotated3DScene)

        #==========================
        #Return the Rotated Points.
        #==========================
        return(np.transpose(listRotated3DScene))
        


        
        
        

