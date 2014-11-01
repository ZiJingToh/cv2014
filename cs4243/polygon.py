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
"""
from .inputmodehandler import InputModeHandler
import cv2


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
    
    normalise: #This Method normalises a Vector by its Magnitude.
    
    quatconj: This Method returns the Conjugate of the given Quaternion.
    
    point2quat: This Method converts an Input Vector to its Quaternion
    Representation.

    rot2quat: This Method calculates the Quaternion for the Rotation Angle
    Theta given the Rotation Axis specified by wx, wy and wz.

    quatmult: This Method performs the Quaternion Multiplications given 2 Input
    Quaternions which are essentially 2 4-Element Input Vectors.

    quat2rot: This Method returns the 3 x 3 Rotation Matrix parameterized with
    the Elements of a given Intput Quaternion.

    rotbyquatmult: This Method performs the Rotation of a Point using Quaternion
    Multiplications given the Coordinates of the Point, the Angle of Rotation
    and the Axis of Rotation through wx, wy and wz. For the specified number of
    iterations, it will perform the Rotation and return the results in n x 3
    Array where n is the total number of Rows affected by the number of
    iterations.

    rotbyrotmat: This Method performs the Rotation of the Camera Orientation at
    a given Frame provided in the form of a 3 x 3 Matrix. The Rotation Matrix of
    the Rotation Quarternion is used. For the specified number of iterations, it
    will perform the Rotation and return the results in n x 3 Array where n is
    the total number of Rows affected by the number of iterations.
    """
    
    #======================
    #Properties/Attributes.
    #======================
    intPolygons = None

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
        self._keyboardEvents = {chr(127):self._UIdeleteLastPoint, # delete key
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
                                "c":self._clearSetPoints}

        self.intPolygons = 1
        print "intPolygons initialised to: " + str(self.intPolygons)       

    def _clearSetPoints(self, key=None):
        """
        Clears point set, creates initial 4 corner points
        """
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

    def _UIdeleteLastPoint(self, key):
        if len(self._points) > 4:
            if self._selectedPoint == self._points.pop():
                self._imageObj.setZFor(0, *self._selectedPoint)
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
                self._imageObj.setZFor(int(self._depthStr), *self._selectedPoint)
                self._depthStr = ""
                self._selectedPoint = None
                self._imageObj.interpolateImagePoints(self._points)
                self._redrawView()

    def _hasPoint(self, x, y):
        radius = int(10 * (1.0/self._imageObj.getViewScale()))
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
        self._imageObj.interpolateImagePoints(self._points)
        self._redrawView()

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

    def cleanup(self):
        """
        Cleanup after exiting state
        """
        print "Cleaning up after Polygon..."

    def normalise(self, listInput):
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

    def quatconj(self, q):
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

    def point2quat(self, arrPointVector):
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

    def rot2quat(self, fltTheta, wx, wy, wz):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        import math as ma
        wx, wy, wz = self.normalise([wx, wy, wz])
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

    def quatmult(self, q1, q2):
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

    def quat2rot(self, q):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        Rq = np.zeros([3, 3])
        q = self.normalise(q)
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

    def rotbyquatmult(self, pt, fltTheta, wx, wy, wz, intIterations):
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
            sp, vp, p = self.point2quat(pt2rot)
            sq, vq, q = self.rot2quat(fltTheta, wx, wy, wz)
            q_conj = self.quatconj(q)
            qp = self.quatmult(q, p)
            p_rot = self.quatmult(qp, q_conj)

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

    def rotbyrotmat(self, matCamFr, fltTheta, wx, wy, wz, intIterations):
        #===============
        #Initialisation.
        #===============
        import numpy as np
        matCamFr = np.matrix(matCamFr)
        matCurrentCamFr = np.zeros([3, 3])

        #===============================
        #Obtain the Rotation Quaternion.
        #===============================
        s_qrot, v_qrot, q_rot = self.rot2quat(fltTheta, wx, wy, wz)
        matRot = np.matrix(self.quat2rot(q_rot))

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
